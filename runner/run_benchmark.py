"""
OpenLLMWorks Runner

Phase:
Runner v0 - Validated Submission Package

Purpose:
Verify the benchmark environment, collect required hardware
evidence, execute three Open LLM Benchmark Database (OLBD)
Protocol v1.0
runs, create a submission.json manifest, validate the completed
submission workspace, and build an upload-ready ZIP package.

The submission workspace contains:

- cpu.txt
- memory.txt
- system.txt
- windows.txt
- nvidia-smi.txt
- benchmark-v1.0-p512-run1.txt
- benchmark-v1.0-p512-run2.txt
- benchmark-v1.0-p512-run3.txt
- submission.json

The completed workspace is validated using the canonical
OpenLLMWorks submission validation path.

A ZIP package is created only when validation passes.

This phase does not modify the canonical Open LLM Benchmark Database.
"""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
import json
import os
import re
import socket
import subprocess
import sys
import zipfile


# ------------------------------------------------------------
# Repository import path
# ------------------------------------------------------------

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(REPOSITORY_ROOT),
    )


from parser.submission import (
    Submission,
)

from parser.validate import (
    print_preflight_result,
)

from runner.provisioning import (
    download_verified_file,
    inspect_model,
    inspect_runtime,
    load_asset_manifest,
    provision_model_from_artifact,
    provision_runtime_from_sources,
)

from runner.submission_client import (
    offer_direct_submission,
)


# ------------------------------------------------------------
# Runner configuration
# ------------------------------------------------------------

RUNNER_VERSION = "0.4.0-beta.1"
PROTOCOL_VERSION = "v1.0"


def get_resource_root() -> Path:
    """
    Return the root containing packaged Runner resources.

    Source execution uses the repository root. A PyInstaller
    build uses its temporary extraction directory.
    """

    if (
        getattr(sys, "frozen", False)
        and hasattr(sys, "_MEIPASS")
    ):
        return Path(
            sys._MEIPASS
        )

    return REPOSITORY_ROOT


def get_local_app_data() -> Path:
    """
    Return the Windows Local AppData directory.

    OpenLLMWorks stores managed runtime assets and benchmark results
    outside the application and repository so the standalone Runner
    can operate without a development checkout.
    """

    local_app_data = os.environ.get(
        "LOCALAPPDATA"
    )

    if not local_app_data:
        raise RuntimeError(
            "LOCALAPPDATA is not available "
            "in the current environment."
        )

    return Path(
        local_app_data
    )


LOCAL_APP_DATA_ROOT = (
    get_local_app_data()
)

OPENLLMWORKS_ROOT = (
    LOCAL_APP_DATA_ROOT
    / "OpenLLMWorks"
)

LEGACY_OPENLLMBENCH_ROOT = (
    LOCAL_APP_DATA_ROOT
    / "OpenLLMBench"
)


def get_managed_root() -> Path:
    """
    Resolve the managed OpenLLMWorks application directory.

    New installations use:

        %LOCALAPPDATA%\\OpenLLMWorks

    Existing installations created before the OpenLLMWorks rebrand
    may already contain verified protocol assets under:

        %LOCALAPPDATA%\\OpenLLMBench

    When the new OpenLLMWorks directory does not yet exist, an
    existing legacy OpenLLMBench directory is reused in place.

    This preserves already-downloaded and verified benchmark assets,
    avoids unnecessary large downloads, and keeps the rebrand
    backward-compatible without moving or deleting user data.
    """

    if OPENLLMWORKS_ROOT.exists():
        return OPENLLMWORKS_ROOT

    if LEGACY_OPENLLMBENCH_ROOT.exists():
        return LEGACY_OPENLLMBENCH_ROOT

    return OPENLLMWORKS_ROOT


MANAGED_ROOT = (
    get_managed_root()
)

PROTOCOL_ROOT = (
    MANAGED_ROOT
    / "protocols"
    / PROTOCOL_VERSION
)

MODEL_FILE = (
    PROTOCOL_ROOT
    / "models"
    / "Qwen3-4B-Q4_K_M.gguf"
)

LLAMA_BENCH_FILE = (
    PROTOCOL_ROOT
    / "runtime"
    / "llama-bench.exe"
)

RESULTS_ROOT = (
    OPENLLMWORKS_ROOT
    / "results"
)

ARTIFACTS_ROOT = (
    MANAGED_ROOT
    / "artifacts"
)

RESOURCE_ROOT = (
    get_resource_root()
)

ASSET_MANIFEST_FILE = (
    RESOURCE_ROOT
    / "runner"
    / "assets.json"
)

EXPECTED_MODEL_SHA256 = (
    "7485FE6F11AF29433BC51CAB58009521"
    "F205840F5B4AE3A32FA7F92E8534FDF5"
)

EXPECTED_LLAMA_BENCH_SHA256 = (
    "060112797BC888544883C793300FA9EB"
    "45F7583E7128A1BE81C8BB24A6799C64"
)

PROMPT_TOKENS = 512
GENERATION_TOKENS = 128
REQUIRED_RUNS = 3
GPU_LAYERS = -1

SUBMISSION_SCHEMA_VERSION = "1.0"
SUBMISSION_MANIFEST_FILE = "submission.json"


# ------------------------------------------------------------
# General helpers
# ------------------------------------------------------------

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_CYAN = "\033[96m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_RED = "\033[91m"


def console_supports_color() -> bool:
    """
    Return True when contributor-facing ANSI color is appropriate.

    Color is cosmetic only. The Runner remains fully functional
    when output is redirected or the terminal does not support it.
    """

    return (
        sys.stdout.isatty()
        and os.environ.get("TERM") != "dumb"
        and os.environ.get("NO_COLOR") is None
    )


def color_text(
    text: str,
    color: str,
    *,
    bold: bool = False,
) -> str:
    """
    Apply ANSI presentation styling when supported.
    """

    if not console_supports_color():
        return text

    prefix = color

    if bold:
        prefix = ANSI_BOLD + prefix

    return (
        prefix
        + text
        + ANSI_RESET
    )


def style_console_line(line: str) -> str:
    """
    Add contributor-facing color to known Runner status markers
    and major workflow headings.

    The underlying message text remains unchanged.
    """

    stripped = line.strip()

    if stripped.startswith(
        ("[PASS]", "[OK]", "[SUCCESS]")
    ):
        return color_text(
            line,
            ANSI_GREEN,
            bold=stripped.startswith("[SUCCESS]"),
        )

    if stripped.startswith(
        ("[WARN]", "[WARNING]", "[INFO]")
    ):
        return color_text(
            line,
            ANSI_YELLOW,
        )

    if stripped.startswith("[FAIL]"):
        return color_text(
            line,
            ANSI_RED,
            bold=True,
        )

    if stripped.startswith("[INTERRUPTED]"):
        return color_text(
            line,
            ANSI_YELLOW,
            bold=True,
        )

    if (
        stripped.startswith("[1/4]")
        or stripped.startswith("[2/4]")
        or stripped.startswith("[3/4]")
        or stripped.startswith("[4/4]")
        or stripped in {
            "BENCHMARK RESULTS",
            "PACKAGING RESULTS",
            "BENCHMARK COMPLETE",
            "RESULT PREPARATION FAILED",
        }
    ):
        return color_text(
            line,
            ANSI_CYAN,
            bold=True,
        )

    return line


def ui_print(
    *values: object,
    sep: str = " ",
    end: str = "\n",
) -> None:
    """
    Print one Runner UI line with optional presentation styling.
    """

    line = sep.join(
        str(value)
        for value in values
    )

    print(
        style_console_line(line),
        end=end,
    )


def print_header() -> None:
    """
    Print the runner startup banner.
    """

    ui_print()
    ui_print("=" * 60)
    ui_print("OpenLLMWorks Runner")
    ui_print(f"Version: {RUNNER_VERSION}")
    ui_print("=" * 60)
    ui_print()


def pause_before_exit() -> None:
    """
    Keep the packaged Windows console visible so contributors can
    read the final success, failure, or cancellation message.

    Source/developer execution remains non-interactive.
    """

    if not getattr(sys, "frozen", False):
        return

    ui_print()
    try:
        input("Press Enter to close OpenLLMWorks Runner...")
    except (EOFError, KeyboardInterrupt):
        pass


def utc_timestamp() -> str:
    """
    Return a normalized UTC ISO-8601 timestamp ending in Z.
    """

    return (
        datetime.now(UTC)
        .isoformat()
        .replace("+00:00", "Z")
    )


def calculate_sha256(
    file_path: Path,
) -> str:
    """
    Calculate the SHA-256 digest for one file.
    """

    digest = sha256()

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(
                1024 * 1024
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest().upper()


# ------------------------------------------------------------
# Managed model provisioning
# ------------------------------------------------------------

def ensure_model_ready() -> bool:
    """
    Verify or automatically acquire and provision the Protocol
    v1.0 benchmark model.
    """

    ui_print("Benchmark Model")
    ui_print("-" * 60)

    try:
        manifest = load_asset_manifest(
            ASSET_MANIFEST_FILE
        )

    except RuntimeError as error:
        ui_print(
            f"[FAIL] {error}"
        )
        ui_print()
        return False

    manifest_protocol = manifest.get(
        "protocol_version"
    )

    if manifest_protocol != PROTOCOL_VERSION:
        ui_print(
            "[FAIL] Asset manifest protocol version "
            "does not match the Runner."
        )
        ui_print(
            f"Runner:   {PROTOCOL_VERSION}"
        )
        ui_print(
            f"Manifest: {manifest_protocol}"
        )
        ui_print()
        return False

    model_ok, model_message = (
        inspect_model(
            protocol_root=PROTOCOL_ROOT,
            manifest=manifest,
        )
    )

    if model_ok:
        ui_print(
            "[OK] "
            f"{model_message}"
        )
        ui_print()
        return True

    ui_print(
        "[INFO] "
        f"{model_message}"
    )
    ui_print(
        "Model provisioning is required."
    )

    model = manifest["assets"]["model"]

    filename = model.get(
        "filename"
    )

    size_bytes = model.get(
        "size_bytes"
    )

    expected_sha256 = model.get(
        "sha256"
    )

    source = model.get(
        "source"
    )

    if not filename:
        ui_print(
            "[FAIL] Model manifest does not define "
            "filename."
        )
        ui_print()
        return False

    if size_bytes is None:
        ui_print(
            "[FAIL] Model manifest does not define "
            "size_bytes."
        )
        ui_print()
        return False

    if not expected_sha256:
        ui_print(
            "[FAIL] Model manifest does not define "
            "sha256."
        )
        ui_print()
        return False

    if not isinstance(
        source,
        dict,
    ):
        ui_print(
            "[FAIL] Model manifest does not define "
            "a source."
        )
        ui_print()
        return False

    url = source.get(
        "url"
    )

    if not url:
        ui_print(
            "[FAIL] Model source does not define url."
        )
        ui_print()
        return False

    artifact_path = (
        ARTIFACTS_ROOT
        / filename
    )

    ui_print(
        f"Artifact: {artifact_path}"
    )

    acquired_ok, acquired_message = (
        download_verified_file(
            url=str(url),
            destination=artifact_path,
            expected_size=int(size_bytes),
            expected_sha256=str(
                expected_sha256
            ),
            label="Benchmark model artifact",
        )
    )

    if not acquired_ok:
        ui_print(
            "[FAIL] "
            f"{acquired_message}"
        )
        ui_print()
        return False

    ui_print(
        "[OK] "
        f"{acquired_message}"
    )

    provisioned_ok, provisioned_message = (
        provision_model_from_artifact(
            protocol_root=PROTOCOL_ROOT,
            artifact_path=artifact_path,
            manifest=manifest,
        )
    )

    if not provisioned_ok:
        ui_print(
            "[FAIL] "
            f"{provisioned_message}"
        )
        ui_print()
        return False

    ui_print(
        "[OK] "
        f"{provisioned_message}"
    )
    ui_print()

    return True


# ------------------------------------------------------------
# Managed runtime provisioning
# ------------------------------------------------------------

def ensure_runtime_ready() -> bool:
    """
    Verify or automatically acquire and provision the frozen
    Protocol v1.0 llama.cpp Windows NVIDIA runtime.
    """

    ui_print("Benchmark Runtime")
    ui_print("-" * 60)

    try:
        manifest = load_asset_manifest(
            ASSET_MANIFEST_FILE
        )

    except RuntimeError as error:
        ui_print(
            f"[FAIL] {error}"
        )
        ui_print()
        return False

    manifest_protocol = manifest.get(
        "protocol_version"
    )

    if manifest_protocol != PROTOCOL_VERSION:
        ui_print(
            "[FAIL] Asset manifest protocol version "
            "does not match the Runner."
        )
        ui_print(
            f"Runner:   {PROTOCOL_VERSION}"
        )
        ui_print(
            f"Manifest: {manifest_protocol}"
        )
        ui_print()
        return False

    runtime_ok, runtime_message = (
        inspect_runtime(
            protocol_root=PROTOCOL_ROOT,
            manifest=manifest,
        )
    )

    if runtime_ok:
        ui_print(
            "[OK] "
            f"{runtime_message}"
        )
        ui_print()
        return True

    ui_print(
        "[INFO] "
        f"{runtime_message}"
    )
    ui_print(
        "Runtime provisioning is required."
    )

    runtime = manifest["assets"]["runtime"]

    sources = runtime.get(
        "sources"
    )

    if not isinstance(
        sources,
        list,
    ) or not sources:
        ui_print(
            "[FAIL] Runtime manifest does not define "
            "sources."
        )
        ui_print()
        return False

    artifact_paths: dict[str, Path] = {}

    for source in sources:
        source_id = source.get(
            "id"
        )

        filename = source.get(
            "filename"
        )

        size_bytes = source.get(
            "size_bytes"
        )

        expected_sha256 = source.get(
            "sha256"
        )

        url = source.get(
            "url"
        )

        if not source_id:
            ui_print(
                "[FAIL] Runtime source does not define id."
            )
            ui_print()
            return False

        if not filename:
            ui_print(
                "[FAIL] Runtime source does not define "
                f"filename: {source_id}"
            )
            ui_print()
            return False

        if size_bytes is None:
            ui_print(
                "[FAIL] Runtime source does not define "
                f"size_bytes: {source_id}"
            )
            ui_print()
            return False

        if not expected_sha256:
            ui_print(
                "[FAIL] Runtime source does not define "
                f"sha256: {source_id}"
            )
            ui_print()
            return False

        if not url:
            ui_print(
                "[FAIL] Runtime source does not define "
                f"url: {source_id}"
            )
            ui_print()
            return False

        artifact_path = (
            ARTIFACTS_ROOT
            / filename
        )

        ui_print(
            f"Artifact: {artifact_path}"
        )

        acquired_ok, acquired_message = (
            download_verified_file(
                url=str(url),
                destination=artifact_path,
                expected_size=int(size_bytes),
                expected_sha256=str(
                    expected_sha256
                ),
                label=(
                    "Runtime source "
                    f"{source_id}"
                ),
            )
        )

        if not acquired_ok:
            ui_print(
                "[FAIL] "
                f"{acquired_message}"
            )
            ui_print()
            return False

        ui_print(
            "[OK] "
            f"{acquired_message}"
        )

        artifact_paths[
            str(source_id)
        ] = artifact_path

    provisioned_ok, provisioned_message = (
        provision_runtime_from_sources(
            protocol_root=PROTOCOL_ROOT,
            artifact_paths=artifact_paths,
            manifest=manifest,
        )
    )

    if not provisioned_ok:
        ui_print(
            "[FAIL] "
            f"{provisioned_message}"
        )
        ui_print()
        return False

    ui_print(
        "[OK] "
        f"{provisioned_message}"
    )
    ui_print()

    return True


# ------------------------------------------------------------
# NVIDIA environment
# ------------------------------------------------------------

def run_nvidia_smi() -> str:
    """
    Execute nvidia-smi and return its text output.
    """

    try:
        completed = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            check=False,
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "nvidia-smi was not found. "
            "Install the NVIDIA driver before benchmarking."
        ) from error

    if completed.returncode != 0:
        raise RuntimeError(
            "nvidia-smi returned an error.\n"
            f"{completed.stderr.strip()}"
        )

    return completed.stdout


def parse_nvidia_smi(
    text: str,
) -> dict:
    """
    Extract basic NVIDIA GPU information.
    """

    gpu_match = re.search(
        r"\|\s*0\s+(.+?)\s{2,}(WDDM|TCC)\s+\|",
        text,
    )

    version_match = re.search(
        r"NVIDIA-SMI\s+([0-9.]+).*?"
        r"(?:Driver Version|KMD Version):\s*([0-9.]+).*?"
        r"(?:CUDA Version|CUDA UMD Version):\s*([0-9.]+)",
        text,
        flags=re.DOTALL,
    )

    memory_match = re.search(
        r"(\d+)\s*MiB\s*/\s*(\d+)\s*MiB",
        text,
    )

    if gpu_match is None:
        raise RuntimeError(
            "Unable to parse the NVIDIA GPU "
            "from nvidia-smi."
        )

    gpu_model = " ".join(
        gpu_match.group(1).split()
    )

    total_vram_mib = None

    if memory_match is not None:
        total_vram_mib = int(
            memory_match.group(2)
        )

    return {
        "gpu_model": gpu_model,
        "driver_model": gpu_match.group(2),
        "nvidia_smi_version": (
            version_match.group(1)
            if version_match
            else None
        ),
        "driver_version": (
            version_match.group(2)
            if version_match
            else None
        ),
        "cuda_version": (
            version_match.group(3)
            if version_match
            else None
        ),
        "vram_mib": total_vram_mib,
    }


def sanitize_name(
    value: str,
) -> str:
    """
    Convert a hardware name into a safe folder-name fragment.
    """

    cleaned = re.sub(
        r"[^A-Za-z0-9]+",
        "-",
        value,
    )

    return cleaned.strip("-")


def check_file(
    *,
    label: str,
    file_path: Path,
    expected_sha256: str,
) -> bool:
    """
    Verify one required benchmark file.
    """

    ui_print(label)
    ui_print(f"Path: {file_path}")

    if not file_path.is_file():
        ui_print("[FAIL] File not found.")
        ui_print()
        return False

    ui_print("[OK] File found.")
    ui_print("Calculating SHA-256...")

    actual_sha256 = calculate_sha256(
        file_path
    )

    ui_print(
        f"Expected: {expected_sha256}"
    )

    ui_print(
        f"Actual:   {actual_sha256}"
    )

    if actual_sha256 != expected_sha256:
        ui_print("[FAIL] SHA-256 does not match.")
        ui_print()
        return False

    ui_print("[OK] SHA-256 verified.")
    ui_print()

    return True


def check_gpu() -> tuple[
    bool,
    dict | None,
    str | None,
]:
    """
    Verify NVIDIA GPU and driver availability.
    """

    ui_print("NVIDIA GPU")
    ui_print("-" * 60)

    try:
        raw_output = run_nvidia_smi()

        gpu = parse_nvidia_smi(
            raw_output
        )

    except RuntimeError as error:
        ui_print(f"[FAIL] {error}")
        ui_print()

        return False, None, None

    ui_print(
        f"GPU: {gpu['gpu_model']}"
    )

    if gpu["vram_mib"] is not None:
        ui_print(
            f"VRAM: {gpu['vram_mib']} MiB"
        )

    ui_print(
        "Driver model: "
        f"{gpu['driver_model']}"
    )

    ui_print(
        "NVIDIA-SMI: "
        f"{gpu['nvidia_smi_version'] or 'Unknown'}"
    )

    ui_print(
        "Driver: "
        f"{gpu['driver_version'] or 'Unknown'}"
    )

    ui_print(
        "CUDA reported: "
        f"{gpu['cuda_version'] or 'Unknown'}"
    )

    ui_print(
        "[OK] NVIDIA environment detected."
    )

    ui_print()

    return True, gpu, raw_output


# ------------------------------------------------------------
# Hardware evidence
# ------------------------------------------------------------

def run_powershell_to_file(
    *,
    command: str,
    output_file: Path,
) -> None:
    """
    Execute one PowerShell command and save stdout.
    """

    completed = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            command,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        raise RuntimeError(
            "PowerShell evidence command failed:\n"
            f"{command}\n\n"
            f"{completed.stderr.strip()}"
        )

    output_file.write_text(
        completed.stdout,
        encoding="utf-8",
    )


def capture_hardware_evidence(
    *,
    result_path: Path,
    nvidia_smi_output: str,
) -> None:
    """
    Capture required OpenLLMWorks hardware evidence files.
    """

    ui_print("=" * 60)
    ui_print("Hardware Evidence")
    ui_print("=" * 60)
    ui_print()

    evidence_commands = {
        "cpu.txt": (
            "Get-CimInstance Win32_Processor | "
            "Select-Object "
            "Name,NumberOfCores,"
            "NumberOfLogicalProcessors | "
            "Format-Table -AutoSize | "
            "Out-String -Width 240"
        ),
        "memory.txt": (
            "$systemMemory = Get-CimInstance "
            "Win32_ComputerSystem | "
            "Select-Object TotalPhysicalMemory; "
            "$physicalMemory = Get-CimInstance "
            "Win32_PhysicalMemory | "
            "Select-Object "
            "BankLabel,DeviceLocator,"
            "Manufacturer,PartNumber,Capacity,"
            "Speed,ConfiguredClockSpeed,"
            "SMBIOSMemoryType,FormFactor; "
            "'SYSTEM MEMORY'; "
            "$systemMemory | Format-List | "
            "Out-String -Width 240; "
            "'PHYSICAL MEMORY MODULES'; "
            "$physicalMemory | Format-List | "
            "Out-String -Width 240"
        ),
        "system.txt": (
            "$computerSystem = Get-CimInstance "
            "Win32_ComputerSystem | "
            "Select-Object Manufacturer,Model; "
            "$baseBoard = Get-CimInstance "
            "Win32_BaseBoard | "
            "Select-Object Manufacturer,Product,Version; "
            "$videoControllers = Get-CimInstance "
            "Win32_VideoController | "
            "Select-Object "
            "Name,PNPDeviceID,AdapterRAM,"
            "DriverVersion,VideoProcessor; "
            "'COMPUTER SYSTEM'; "
            "$computerSystem | Format-List | "
            "Out-String -Width 240; "
            "'BASEBOARD'; "
            "$baseBoard | Format-List | "
            "Out-String -Width 240; "
            "'VIDEO CONTROLLERS'; "
            "$videoControllers | Format-List | "
            "Out-String -Width 240"
        ),
        "windows.txt": (
            "Get-ComputerInfo | "
            "Select-Object "
            "WindowsProductName,"
            "WindowsVersion,"
            "OsBuildNumber | "
            "Format-Table -AutoSize | "
            "Out-String -Width 240"
        ),
    }

    for file_name, command in (
        evidence_commands.items()
    ):
        output_file = (
            result_path
            / file_name
        )

        run_powershell_to_file(
            command=command,
            output_file=output_file,
        )

        ui_print(
            f"[OK] {file_name}"
        )

    nvidia_file = (
        result_path
        / "nvidia-smi.txt"
    )

    nvidia_file.write_text(
        nvidia_smi_output,
        encoding="utf-8",
    )

    ui_print("[OK] nvidia-smi.txt")
    ui_print()


# ------------------------------------------------------------
# Benchmark execution
# ------------------------------------------------------------

def build_benchmark_command() -> list[str]:
    """
    Build the frozen Benchmark Protocol v1.0 command.
    """

    return [
        str(LLAMA_BENCH_FILE),
        "-m",
        str(MODEL_FILE),
        "-p",
        str(PROMPT_TOKENS),
        "-n",
        str(GENERATION_TOKENS),
        "-r",
        "1",
        "-ngl",
        str(GPU_LAYERS),
        "-o",
        "md",
    ]


def execute_benchmark_run(
    *,
    run_number: int,
    result_path: Path,
) -> Path:
    """
    Execute one independent benchmark run.

    Both stderr diagnostics and stdout benchmark output are
    preserved in the raw benchmark evidence file.
    """

    output_file = (
        result_path
        / (
            "benchmark-v1.0-p512-"
            f"run{run_number}.txt"
        )
    )

    command = build_benchmark_command()

    ui_print(
        f"Running benchmark "
        f"{run_number}/{REQUIRED_RUNS}..."
    )

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        cwd=str(
            LLAMA_BENCH_FILE.parent
        ),
    )

    combined_output = ""

    if completed.stderr:
        combined_output += (
            completed.stderr.rstrip()
            + "\n"
        )

    if completed.stdout:
        combined_output += (
            completed.stdout.rstrip()
            + "\n"
        )

    output_file.write_text(
        combined_output,
        encoding="utf-8",
    )

    if completed.returncode != 0:
        raise RuntimeError(
            "Benchmark run failed with exit code "
            f"{completed.returncode}. "
            "Raw output was preserved at "
            f"{output_file}"
        )

    ui_print(
        f"[OK] Run {run_number} completed."
    )

    return output_file


# ------------------------------------------------------------
# Benchmark result parsing
# ------------------------------------------------------------

def extract_benchmark_result(
    file_path: Path,
) -> dict:
    """
    Extract pp512 and tg128 from one raw benchmark file.

    The parser intentionally ignores the displayed plus/minus
    separator because Windows text encoding may render it as
    mojibake in preserved output files.
    """

    text = file_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    pp_match = re.search(
        r"\|\s*pp512\s*\|\s*([0-9.]+)",
        text,
    )

    tg_match = re.search(
        r"\|\s*tg128\s*\|\s*([0-9.]+)",
        text,
    )

    build_match = re.search(
        r"build:\s*([0-9a-fA-F]+)"
        r"\s*\((\d+)\)",
        text,
    )

    if pp_match is None:
        raise RuntimeError(
            f"Could not find pp512 in {file_path.name}"
        )

    if tg_match is None:
        raise RuntimeError(
            f"Could not find tg128 in {file_path.name}"
        )

    return {
        "pp512": float(
            pp_match.group(1)
        ),
        "tg128": float(
            tg_match.group(1)
        ),
        "commit": (
            build_match.group(1)
            if build_match
            else None
        ),
        "build": (
            int(build_match.group(2))
            if build_match
            else None
        ),
    }


def print_results_summary(
    benchmark_files: list[Path],
) -> bool:
    """
    Print benchmark results and verify all three runs parsed.
    """

    ui_print()
    ui_print("=" * 60)
    ui_print("BENCHMARK RESULTS")
    ui_print("=" * 60)
    ui_print()

    parsed_results = []

    for index, file_path in enumerate(
        benchmark_files,
        start=1,
    ):
        try:
            result = extract_benchmark_result(
                file_path
            )

        except RuntimeError as error:
            ui_print(f"[FAIL] {error}")
            return False

        parsed_results.append(
            result
        )

        ui_print(
            f"Run {index}: "
            f"pp512 {result['pp512']:.2f} t/s | "
            f"tg128 {result['tg128']:.2f} t/s"
        )

    pp_average = sum(
        item["pp512"]
        for item in parsed_results
    ) / len(parsed_results)

    tg_average = sum(
        item["tg128"]
        for item in parsed_results
    ) / len(parsed_results)

    ui_print()

    ui_print(
        "Average: "
        f"pp512 {pp_average:.2f} t/s | "
        f"tg128 {tg_average:.2f} t/s"
    )

    commits = {
        item["commit"]
        for item in parsed_results
    }

    builds = {
        item["build"]
        for item in parsed_results
    }

    if len(commits) == 1:
        ui_print(
            f"llama.cpp commit: "
            f"{next(iter(commits))}"
        )

    if len(builds) == 1:
        ui_print(
            f"llama.cpp build: "
            f"{next(iter(builds))}"
        )

    ui_print()
    ui_print(
        "[PASS] Three benchmark runs parsed successfully."
    )

    return True


# ------------------------------------------------------------
# Submission manifest
# ------------------------------------------------------------

def create_submission_manifest(
    *,
    result_path: Path,
    submission_name: str,
    benchmark_timestamp: str,
) -> Path:
    """
    Create the canonical OpenLLMWorks submission.json manifest.
    """

    submitted_at = utc_timestamp()

    manifest = {
        "schema_version": (
            SUBMISSION_SCHEMA_VERSION
        ),
        "submission_name": (
            submission_name
        ),
        "submitted_at": (
            submitted_at
        ),
        "benchmark_timestamp": (
            benchmark_timestamp
        ),
    }

    manifest_path = (
        result_path
        / SUBMISSION_MANIFEST_FILE
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return manifest_path


# ------------------------------------------------------------
# Submission validation
# ------------------------------------------------------------

def validate_submission_workspace(
    result_path: Path,
) -> bool:
    """
    Validate a completed runner workspace using the canonical
    OpenLLMWorks submission validation path.
    """

    ui_print()
    ui_print("=" * 60)
    ui_print("Submission Validation")
    ui_print("=" * 60)

    try:
        submission = Submission.from_path(
            result_path
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        ui_print()
        ui_print(
            f"[FAIL] Could not load submission: "
            f"{error}"
        )
        ui_print()

        return False

    try:
        valid = print_preflight_result(
            submission
        )

    except Exception as error:
        ui_print()
        ui_print(
            "[FAIL] Submission validation "
            f"raised an unexpected error: {error}"
        )
        ui_print()

        return False

    return valid


# ------------------------------------------------------------
# ZIP packaging
# ------------------------------------------------------------

def build_submission_zip(
    result_path: Path,
) -> Path:
    """
    Build an upload-ready ZIP containing the validated
    submission workspace.

    The ZIP contains one top-level directory named after the
    submission workspace. This allows standard extraction tools
    to recreate a validator-ready submission directory without
    requiring the user or maintainer to create one manually.
    """

    if not result_path.is_dir():
        raise RuntimeError(
            "Cannot package submission because the "
            f"workspace does not exist: {result_path}"
        )

    zip_path = (
        result_path.parent
        / f"{result_path.name}.zip"
    )

    if zip_path.exists():
        zip_path.unlink()

    files = sorted(
        path
        for path in result_path.rglob("*")
        if path.is_file()
    )

    if not files:
        raise RuntimeError(
            "Cannot package submission because the "
            "workspace contains no files."
        )

    try:
        with zipfile.ZipFile(
            zip_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:
            for file_path in files:
                relative_path = (
                    file_path.relative_to(
                        result_path
                    )
                )

                archive_name = (
                    Path(result_path.name)
                    / relative_path
                )

                archive.write(
                    file_path,
                    arcname=str(
                        archive_name
                    ),
                )

    except OSError as error:
        if zip_path.exists():
            zip_path.unlink()

        raise RuntimeError(
            f"Could not create submission ZIP: {error}"
        ) from error

    return zip_path


# ------------------------------------------------------------
# Main runner
# ------------------------------------------------------------

ACTIVE_RESULT_PATH: Path | None = None


def run_main_workflow() -> int:
    """
    Run the OpenLLMWorks benchmark workflow.
    """

    global ACTIVE_RESULT_PATH

    print_header()

    gpu_ok, gpu, nvidia_output = (
        check_gpu()
    )

    model_ready = ensure_model_ready()

    if model_ready:
        model_ok = check_file(
            label="Qwen3-4B-Q4_K_M.gguf",
            file_path=MODEL_FILE,
            expected_sha256=(
                EXPECTED_MODEL_SHA256
            ),
        )
    else:
        model_ok = False
        ui_print(
            "[FAIL] Benchmark model is not ready."
        )
        ui_print()

    runtime_ok = ensure_runtime_ready()

    ui_print("Benchmark Engine")
    ui_print("-" * 60)

    if runtime_ok:
        engine_ok = check_file(
            label="llama-bench.exe",
            file_path=LLAMA_BENCH_FILE,
            expected_sha256=(
                EXPECTED_LLAMA_BENCH_SHA256
            ),
        )
    else:
        engine_ok = False
        ui_print(
            "[FAIL] Benchmark runtime is not ready."
        )
        ui_print()

    ui_print("=" * 60)
    ui_print("[1/4] CHECKING YOUR SYSTEM")
    ui_print("=" * 60)

    ui_print(
        "[PASS] NVIDIA GPU"
        if gpu_ok
        else "[FAIL] NVIDIA GPU"
    )

    ui_print(
        "[PASS] Benchmark model"
        if model_ok
        else "[FAIL] Benchmark model"
    )

    ui_print(
        "[PASS] Benchmark runtime"
        if runtime_ok
        else "[FAIL] Benchmark runtime"
    )

    ui_print(
        "[PASS] Benchmark engine"
        if engine_ok
        else "[FAIL] Benchmark engine"
    )

    ui_print()

    if not (
        gpu_ok
        and model_ok
        and runtime_ok
        and engine_ok
    ):
        ui_print(
            "Environment verification FAILED."
        )
        ui_print()
        ui_print(
            "Benchmarking did not start."
        )
        ui_print(
            "Correct the failed checks above, "
            "then run the Runner again."
        )
        ui_print()

        return 1

    ui_print(
        "Environment verification PASSED."
    )

    ui_print()

    assert gpu is not None
    assert nvidia_output is not None

    machine_name = sanitize_name(
        socket.gethostname()
    )

    gpu_name = sanitize_name(
        gpu["gpu_model"]
    )

    local_timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )

    submission_name = (
        f"{machine_name}-{gpu_name}-{local_timestamp}"
    )

    result_path = (
        RESULTS_ROOT
        / submission_name
    )

    result_path.mkdir(
        parents=True,
        exist_ok=False,
    )

    ACTIVE_RESULT_PATH = result_path

    ui_print("=" * 60)
    ui_print("Benchmark Workspace")
    ui_print("=" * 60)

    ui_print(
        f"Submission: {submission_name}"
    )

    ui_print(
        f"Path: {result_path}"
    )

    ui_print()

    try:
        capture_hardware_evidence(
            result_path=result_path,
            nvidia_smi_output=(
                nvidia_output
            ),
        )

        ui_print("=" * 60)
        ui_print("[2/4] PREPARING BENCHMARK")
        ui_print("=" * 60)
        ui_print()
        ui_print("For best consistency:")
        ui_print(
            "- Allow the system to reach a normal idle state."
        )
        ui_print(
            "- Close unnecessary heavy applications or workloads."
        )
        ui_print(
            "- Avoid changing GPU clocks or power settings "
            "during the run."
        )
        ui_print()
        ui_print(
            "Benchmark Protocol v1.0 does not require "
            "a fixed cooldown period."
        )
        ui_print(
            "Benchmarking will begin automatically."
        )
        ui_print()

        ui_print("=" * 60)
        ui_print("[3/4] RUNNING BENCHMARK")
        ui_print("=" * 60)
        ui_print()

        benchmark_timestamp = utc_timestamp()

        benchmark_files = []

        for run_number in range(
            1,
            REQUIRED_RUNS + 1,
        ):
            benchmark_file = (
                execute_benchmark_run(
                    run_number=run_number,
                    result_path=result_path,
                )
            )

            benchmark_files.append(
                benchmark_file
            )

        results_ok = (
            print_results_summary(
                benchmark_files
            )
        )

    except RuntimeError as error:
        ui_print()
        ui_print(f"[FAIL] {error}")
        ui_print()
        ui_print(
            "Runner stopped. Partial evidence "
            "has been preserved at:"
        )

        ui_print(result_path)

        return 1

    if not results_ok:
        ui_print()
        ui_print(
            "Runner stopped because benchmark results "
            "could not be parsed."
        )
        ui_print()
        ui_print(
            "Benchmark evidence has been preserved at:"
        )
        ui_print(result_path)
        ui_print()

        return 1

    ui_print()
    ui_print("=" * 60)
    ui_print("[4/4] PREPARING RESULTS")
    ui_print("=" * 60)
    ui_print()

    try:
        manifest_path = (
            create_submission_manifest(
                result_path=result_path,
                submission_name=(
                    submission_name
                ),
                benchmark_timestamp=(
                    benchmark_timestamp
                ),
            )
        )

    except OSError as error:
        ui_print(
            f"[FAIL] Could not create "
            f"{SUBMISSION_MANIFEST_FILE}: "
            f"{error}"
        )

        return 1

    ui_print(
        f"[OK] {SUBMISSION_MANIFEST_FILE} created."
    )
    ui_print()
    ui_print(
        f"Path: {manifest_path}"
    )

    validation_ok = (
        validate_submission_workspace(
            result_path
        )
    )

    if not validation_ok:
        ui_print()
        ui_print("=" * 60)
        ui_print("RESULT PREPARATION FAILED")
        ui_print("=" * 60)
        ui_print()
        ui_print(
            "Benchmark evidence and manifest "
            "were created, but submission "
            "validation failed."
        )
        ui_print()
        ui_print(
            "No ZIP package was created."
        )
        ui_print()
        ui_print(
            "Workspace preserved at:"
        )
        ui_print(result_path)
        ui_print()

        return 1

    ui_print()
    ui_print("=" * 60)
    ui_print("PACKAGING RESULTS")
    ui_print("=" * 60)
    ui_print()

    try:
        zip_path = build_submission_zip(
            result_path
        )

    except RuntimeError as error:
        ui_print(
            f"[FAIL] {error}"
        )
        ui_print()
        ui_print(
            "Validated workspace preserved at:"
        )
        ui_print(result_path)
        ui_print()

        return 1

    ui_print(
        "[OK] Submission ZIP created."
    )
    ui_print()
    ui_print(
        f"Path: {zip_path}"
    )

    ui_print()
    ui_print("=" * 60)
    ui_print("BENCHMARK COMPLETE")
    ui_print("=" * 60)
    ui_print()

    ui_print(
        "[PASS] Benchmark evidence created."
    )

    ui_print(
        "[PASS] Submission manifest created."
    )

    ui_print(
        "[PASS] Submission validation passed."
    )

    ui_print(
        "[PASS] Submission ZIP created."
    )

    ui_print()

    ui_print(
        "Validated submission workspace:"
    )
    ui_print(result_path)
    ui_print()

    ui_print(
        "Upload-ready submission package:"
    )
    ui_print(zip_path)
    ui_print()

    success_message = (
        "[SUCCESS] OpenLLMWorks Runner completed successfully!"
    )

    ui_print(success_message)
    ui_print()

    offer_direct_submission(
        zip_path=zip_path,
        submission_name=submission_name,
        gpu_name=gpu["gpu_model"],
    )

    return 0


def main() -> int:
    """
    Run the workflow with contributor-facing cancellation handling.
    """

    global ACTIVE_RESULT_PATH

    ACTIVE_RESULT_PATH = None

    try:
        return run_main_workflow()

    except KeyboardInterrupt:
        ui_print()
        ui_print()
        ui_print("=" * 60)
        ui_print("[INTERRUPTED] OpenLLMWorks Runner")
        ui_print("=" * 60)
        ui_print()
        ui_print(
            "The Runner was interrupted by the user."
        )
        ui_print()
        ui_print(
            "No valid submission ZIP was created "
            "by this interrupted run."
        )

        if ACTIVE_RESULT_PATH is not None:
            ui_print()
            ui_print(
                "Partial benchmark workspace preserved at:"
            )
            ui_print(ACTIVE_RESULT_PATH)

        ui_print()
        ui_print(
            "You can safely run OpenLLMWorks Runner again."
        )
        ui_print()

        return 130


if __name__ == "__main__":
    exit_code = main()
    pause_before_exit()
    sys.exit(exit_code)
