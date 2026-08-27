"""
OpenLLMBench Runner

Phase:
Runner v0 - Validated Submission Package

Purpose:
Verify the benchmark environment, collect required hardware
evidence, execute three OpenLLMBench Benchmark Protocol v1.0
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
OpenLLMBench submission validation path.

A ZIP package is created only when validation passes.

This phase does not modify the OpenLLMBench database.
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


# ------------------------------------------------------------
# Runner configuration
# ------------------------------------------------------------

RUNNER_VERSION = "0.3.0-dev3"
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

    OpenLLMBench stores managed runtime assets and benchmark results
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


OPENLLMBENCH_ROOT = (
    get_local_app_data()
    / "OpenLLMBench"
)

PROTOCOL_ROOT = (
    OPENLLMBENCH_ROOT
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
    OPENLLMBENCH_ROOT
    / "results"
)

ARTIFACTS_ROOT = (
    OPENLLMBENCH_ROOT
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

def print_header() -> None:
    """
    Print the runner startup banner.
    """

    print()
    print("=" * 60)
    print("OpenLLMBench Runner")
    print(f"Version: {RUNNER_VERSION}")
    print("=" * 60)
    print()


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

    print("Benchmark Model")
    print("-" * 60)

    try:
        manifest = load_asset_manifest(
            ASSET_MANIFEST_FILE
        )

    except RuntimeError as error:
        print(
            f"[FAIL] {error}"
        )
        print()
        return False

    manifest_protocol = manifest.get(
        "protocol_version"
    )

    if manifest_protocol != PROTOCOL_VERSION:
        print(
            "[FAIL] Asset manifest protocol version "
            "does not match the Runner."
        )
        print(
            f"Runner:   {PROTOCOL_VERSION}"
        )
        print(
            f"Manifest: {manifest_protocol}"
        )
        print()
        return False

    model_ok, model_message = (
        inspect_model(
            protocol_root=PROTOCOL_ROOT,
            manifest=manifest,
        )
    )

    if model_ok:
        print(
            "[OK] "
            f"{model_message}"
        )
        print()
        return True

    print(
        "[INFO] "
        f"{model_message}"
    )
    print(
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
        print(
            "[FAIL] Model manifest does not define "
            "filename."
        )
        print()
        return False

    if size_bytes is None:
        print(
            "[FAIL] Model manifest does not define "
            "size_bytes."
        )
        print()
        return False

    if not expected_sha256:
        print(
            "[FAIL] Model manifest does not define "
            "sha256."
        )
        print()
        return False

    if not isinstance(
        source,
        dict,
    ):
        print(
            "[FAIL] Model manifest does not define "
            "a source."
        )
        print()
        return False

    url = source.get(
        "url"
    )

    if not url:
        print(
            "[FAIL] Model source does not define url."
        )
        print()
        return False

    artifact_path = (
        ARTIFACTS_ROOT
        / filename
    )

    print(
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
        print(
            "[FAIL] "
            f"{acquired_message}"
        )
        print()
        return False

    print(
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
        print(
            "[FAIL] "
            f"{provisioned_message}"
        )
        print()
        return False

    print(
        "[OK] "
        f"{provisioned_message}"
    )
    print()

    return True


# ------------------------------------------------------------
# Managed runtime provisioning
# ------------------------------------------------------------

def ensure_runtime_ready() -> bool:
    """
    Verify or automatically acquire and provision the frozen
    Protocol v1.0 llama.cpp Windows NVIDIA runtime.
    """

    print("Benchmark Runtime")
    print("-" * 60)

    try:
        manifest = load_asset_manifest(
            ASSET_MANIFEST_FILE
        )

    except RuntimeError as error:
        print(
            f"[FAIL] {error}"
        )
        print()
        return False

    manifest_protocol = manifest.get(
        "protocol_version"
    )

    if manifest_protocol != PROTOCOL_VERSION:
        print(
            "[FAIL] Asset manifest protocol version "
            "does not match the Runner."
        )
        print(
            f"Runner:   {PROTOCOL_VERSION}"
        )
        print(
            f"Manifest: {manifest_protocol}"
        )
        print()
        return False

    runtime_ok, runtime_message = (
        inspect_runtime(
            protocol_root=PROTOCOL_ROOT,
            manifest=manifest,
        )
    )

    if runtime_ok:
        print(
            "[OK] "
            f"{runtime_message}"
        )
        print()
        return True

    print(
        "[INFO] "
        f"{runtime_message}"
    )
    print(
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
        print(
            "[FAIL] Runtime manifest does not define "
            "sources."
        )
        print()
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
            print(
                "[FAIL] Runtime source does not define id."
            )
            print()
            return False

        if not filename:
            print(
                "[FAIL] Runtime source does not define "
                f"filename: {source_id}"
            )
            print()
            return False

        if size_bytes is None:
            print(
                "[FAIL] Runtime source does not define "
                f"size_bytes: {source_id}"
            )
            print()
            return False

        if not expected_sha256:
            print(
                "[FAIL] Runtime source does not define "
                f"sha256: {source_id}"
            )
            print()
            return False

        if not url:
            print(
                "[FAIL] Runtime source does not define "
                f"url: {source_id}"
            )
            print()
            return False

        artifact_path = (
            ARTIFACTS_ROOT
            / filename
        )

        print(
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
            print(
                "[FAIL] "
                f"{acquired_message}"
            )
            print()
            return False

        print(
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
        print(
            "[FAIL] "
            f"{provisioned_message}"
        )
        print()
        return False

    print(
        "[OK] "
        f"{provisioned_message}"
    )
    print()

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

    print(label)
    print(f"Path: {file_path}")

    if not file_path.is_file():
        print("[FAIL] File not found.")
        print()
        return False

    print("[OK] File found.")
    print("Calculating SHA-256...")

    actual_sha256 = calculate_sha256(
        file_path
    )

    print(
        f"Expected: {expected_sha256}"
    )

    print(
        f"Actual:   {actual_sha256}"
    )

    if actual_sha256 != expected_sha256:
        print("[FAIL] SHA-256 does not match.")
        print()
        return False

    print("[OK] SHA-256 verified.")
    print()

    return True


def check_gpu() -> tuple[
    bool,
    dict | None,
    str | None,
]:
    """
    Verify NVIDIA GPU and driver availability.
    """

    print("NVIDIA GPU")
    print("-" * 60)

    try:
        raw_output = run_nvidia_smi()

        gpu = parse_nvidia_smi(
            raw_output
        )

    except RuntimeError as error:
        print(f"[FAIL] {error}")
        print()

        return False, None, None

    print(
        f"GPU: {gpu['gpu_model']}"
    )

    if gpu["vram_mib"] is not None:
        print(
            f"VRAM: {gpu['vram_mib']} MiB"
        )

    print(
        "Driver model: "
        f"{gpu['driver_model']}"
    )

    print(
        "NVIDIA-SMI: "
        f"{gpu['nvidia_smi_version'] or 'Unknown'}"
    )

    print(
        "Driver: "
        f"{gpu['driver_version'] or 'Unknown'}"
    )

    print(
        "CUDA reported: "
        f"{gpu['cuda_version'] or 'Unknown'}"
    )

    print(
        "[OK] NVIDIA environment detected."
    )

    print()

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
    Capture required OpenLLMBench hardware evidence files.
    """

    print("=" * 60)
    print("Hardware Evidence")
    print("=" * 60)
    print()

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
            "Get-CimInstance Win32_ComputerSystem | "
            "Select-Object TotalPhysicalMemory | "
            "Format-Table -AutoSize | "
            "Out-String -Width 240"
        ),
        "system.txt": (
            "Get-CimInstance Win32_ComputerSystem | "
            "Select-Object Manufacturer,Model | "
            "Format-Table -AutoSize | "
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

        print(
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

    print("[OK] nvidia-smi.txt")
    print()


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

    print(
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

    print(
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

    print()
    print("=" * 60)
    print("Benchmark Results")
    print("=" * 60)
    print()

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
            print(f"[FAIL] {error}")
            return False

        parsed_results.append(
            result
        )

        print(
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

    print()

    print(
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
        print(
            f"llama.cpp commit: "
            f"{next(iter(commits))}"
        )

    if len(builds) == 1:
        print(
            f"llama.cpp build: "
            f"{next(iter(builds))}"
        )

    print()
    print(
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
    Create the canonical OpenLLMBench submission.json manifest.
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
    OpenLLMBench submission validation path.
    """

    print()
    print("=" * 60)
    print("Submission Validation")
    print("=" * 60)

    try:
        submission = Submission.from_path(
            result_path
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as error:
        print()
        print(
            f"[FAIL] Could not load submission: "
            f"{error}"
        )
        print()

        return False

    try:
        valid = print_preflight_result(
            submission
        )

    except Exception as error:
        print()
        print(
            "[FAIL] Submission validation "
            f"raised an unexpected error: {error}"
        )
        print()

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

def main() -> int:
    """
    Run Runner v0 Phase 3C.
    """

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
        print(
            "[FAIL] Benchmark model is not ready."
        )
        print()

    runtime_ok = ensure_runtime_ready()

    print("Benchmark Engine")
    print("-" * 60)

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
        print(
            "[FAIL] Benchmark runtime is not ready."
        )
        print()

    print("=" * 60)
    print("Environment Verification Summary")
    print("=" * 60)

    print(
        "[PASS] NVIDIA GPU"
        if gpu_ok
        else "[FAIL] NVIDIA GPU"
    )

    print(
        "[PASS] Benchmark model"
        if model_ok
        else "[FAIL] Benchmark model"
    )

    print(
        "[PASS] Benchmark runtime"
        if runtime_ok
        else "[FAIL] Benchmark runtime"
    )

    print(
        "[PASS] Benchmark engine"
        if engine_ok
        else "[FAIL] Benchmark engine"
    )

    print()

    if not (
        gpu_ok
        and model_ok
        and runtime_ok
        and engine_ok
    ):
        print(
            "Environment verification FAILED."
        )
        print()
        print(
            "Benchmarking did not start."
        )
        print(
            "Correct the failed checks above, "
            "then run the Runner again."
        )
        print()

        return 1

    print(
        "Environment verification PASSED."
    )

    print()

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

    print("=" * 60)
    print("Benchmark Workspace")
    print("=" * 60)

    print(
        f"Submission: {submission_name}"
    )

    print(
        f"Path: {result_path}"
    )

    print()

    try:
        capture_hardware_evidence(
            result_path=result_path,
            nvidia_smi_output=(
                nvidia_output
            ),
        )

        print("=" * 60)
        print("Benchmark Readiness")
        print("=" * 60)
        print()
        print("For best consistency:")
        print(
            "- Allow the system to reach a normal idle state."
        )
        print(
            "- Close unnecessary heavy applications or workloads."
        )
        print(
            "- Avoid changing GPU clocks or power settings "
            "during the run."
        )
        print()
        print(
            "Benchmark Protocol v1.0 does not require "
            "a fixed cooldown period."
        )
        print(
            "Benchmarking will begin automatically."
        )
        print()

        print("=" * 60)
        print("Benchmark Execution")
        print("=" * 60)
        print()

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
        print()
        print(f"[FAIL] {error}")
        print()
        print(
            "Runner stopped. Partial evidence "
            "has been preserved at:"
        )

        print(result_path)

        return 1

    if not results_ok:
        print()
        print(
            "Runner stopped because benchmark results "
            "could not be parsed."
        )
        print()
        print(
            "Benchmark evidence has been preserved at:"
        )
        print(result_path)
        print()

        return 1

    print()
    print("=" * 60)
    print("Submission Manifest")
    print("=" * 60)
    print()

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
        print(
            f"[FAIL] Could not create "
            f"{SUBMISSION_MANIFEST_FILE}: "
            f"{error}"
        )

        return 1

    print(
        f"[OK] {SUBMISSION_MANIFEST_FILE} created."
    )
    print()
    print(
        f"Path: {manifest_path}"
    )

    validation_ok = (
        validate_submission_workspace(
            result_path
        )
    )

    if not validation_ok:
        print()
        print("=" * 60)
        print("Runner Phase 3C Failed")
        print("=" * 60)
        print()
        print(
            "Benchmark evidence and manifest "
            "were created, but submission "
            "validation failed."
        )
        print()
        print(
            "No ZIP package was created."
        )
        print()
        print(
            "Workspace preserved at:"
        )
        print(result_path)
        print()

        return 1

    print()
    print("=" * 60)
    print("Submission Packaging")
    print("=" * 60)
    print()

    try:
        zip_path = build_submission_zip(
            result_path
        )

    except RuntimeError as error:
        print(
            f"[FAIL] {error}"
        )
        print()
        print(
            "Validated workspace preserved at:"
        )
        print(result_path)
        print()

        return 1

    print(
        "[OK] Submission ZIP created."
    )
    print()
    print(
        f"Path: {zip_path}"
    )

    print()
    print("=" * 60)
    print("Runner Phase 3C Complete")
    print("=" * 60)
    print()

    print(
        "[PASS] Benchmark evidence created."
    )

    print(
        "[PASS] Submission manifest created."
    )

    print(
        "[PASS] Submission validation passed."
    )

    print(
        "[PASS] Submission ZIP created."
    )

    print()

    print(
        "Validated submission workspace:"
    )
    print(result_path)
    print()

    print(
        "Upload-ready submission package:"
    )
    print(zip_path)
    print()

    print(
        "OpenLLMBench Runner completed successfully."
    )
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

