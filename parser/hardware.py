from pathlib import Path
import re

from parser.windows_lookup import normalize_windows


def read_text_file(file_path: Path) -> str:
    """
    Read a text file while supporting common Windows encodings.
    """

    raw_data = file_path.read_bytes()

    if raw_data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw_data.decode("utf-16")

    if raw_data.startswith(b"\xef\xbb\xbf"):
        return raw_data.decode("utf-8-sig")

    try:
        return raw_data.decode("utf-8")

    except UnicodeDecodeError:
        return raw_data.decode("cp1252", errors="replace")


def normalize_whitespace(value: str) -> str:
    """
    Replace repeated whitespace with a single space.
    """

    return " ".join(value.split())


def parse_cpu(file_path: Path) -> dict:
    """
    Parse cpu.txt generated from Get-CimInstance Win32_Processor.
    """

    text = read_text_file(file_path)

    row_match = re.search(
        r"^(.*?)\s+(\d+)\s+(\d+)\s*$",
        text,
        flags=re.MULTILINE,
    )

    if not row_match:
        raise ValueError(
            f"Could not parse CPU information from {file_path.name}"
        )

    return {
        "model": normalize_whitespace(row_match.group(1)),
        "physical_cores": int(row_match.group(2)),
        "logical_processors": int(row_match.group(3)),
    }


def parse_memory(file_path: Path) -> dict:
    """
    Parse total physical memory reported in bytes.
    """

    text = read_text_file(file_path)

    values = re.findall(r"^\s*(\d+)\s*$", text, re.MULTILINE)

    if not values:
        raise ValueError(
            f"Could not parse memory information from {file_path.name}"
        )

    total_bytes = int(values[-1])

    gibibytes = total_bytes / (1024 ** 3)
    rounded_capacity_gb = round(gibibytes)

    return {
        "reported_bytes": total_bytes,
        "calculated_gib": round(gibibytes, 2),
        "installed_capacity_gb": rounded_capacity_gb,
    }


def parse_system(file_path: Path) -> dict:
    """
    Parse computer manufacturer and model.
    """

    text = read_text_file(file_path)

    lines = [
        line.rstrip()
        for line in text.splitlines()
        if line.strip()
    ]

    separator_index = None

    for index, line in enumerate(lines):
        if re.fullmatch(r"[-\s]+", line):
            separator_index = index
            break

    if separator_index is None:
        raise ValueError(
            f"Could not locate the system table in {file_path.name}"
        )

    if separator_index + 1 >= len(lines):
        raise ValueError(
            f"Could not locate system values in {file_path.name}"
        )

    header = lines[separator_index - 1]
    separator = lines[separator_index]
    value_line = lines[separator_index + 1]

    model_column = header.find("Model")

    if model_column == -1:
        raise ValueError(
            f"Could not locate the Model column in {file_path.name}"
        )

    manufacturer = value_line[:model_column].strip()
    model = value_line[model_column:].strip()

    generic_values = {
        "system manufacturer",
        "system product name",
        "to be filled by o.e.m.",
        "default string",
    }

    generic_identity = (
        manufacturer.lower() in generic_values
        or model.lower() in generic_values
    )

    return {
        "manufacturer": manufacturer or None,
        "model": model or None,
        "generic_firmware_identity": generic_identity,
    }


def parse_windows(file_path: Path) -> dict:
    """
    Parse raw Windows information and create normalized values.
    """

    text = read_text_file(file_path)

    row_match = re.search(
        r"^(Windows.*?)\s+(\S+)\s+(\d+)\s*$",
        text,
        flags=re.MULTILINE,
    )

    if not row_match:
        raise ValueError(
            f"Could not parse Windows information from {file_path.name}"
        )

    reported_name = normalize_whitespace(row_match.group(1))
    reported_version = row_match.group(2)
    build = int(row_match.group(3))

    normalized = normalize_windows(
        reported_name=reported_name,
        reported_version=reported_version,
        build=build,
    )

    return {
        "platform": "Windows",
        "reported": {
            "product_name": reported_name,
            "version": reported_version,
            "build": build,
        },
        "normalized": normalized,
    }


def parse_nvidia_smi(file_path: Path) -> dict:
    """
    Parse NVIDIA GPU, VRAM, driver, CUDA UMD, and driver model.
    """

    text = read_text_file(file_path)

    version_match = re.search(
        r"NVIDIA-SMI\s+([0-9.]+).*?"
        r"KMD Version:\s*([0-9.]+).*?"
        r"CUDA UMD Version:\s*([0-9.]+)",
        text,
        flags=re.DOTALL,
    )

    gpu_match = re.search(
        r"\|\s*0\s+(.+?)\s{2,}(WDDM|TCC)\s+\|",
        text,
    )

    memory_match = re.search(
        r"(\d+)\s*MiB\s*/\s*(\d+)\s*MiB",
        text,
    )

    if not gpu_match:
        raise ValueError(
            f"Could not parse GPU information from {file_path.name}"
        )

    model = normalize_whitespace(gpu_match.group(1))
    driver_model = gpu_match.group(2)

    total_vram_mib = None
    total_vram_gib = None

    if memory_match:
        total_vram_mib = int(memory_match.group(2))
        total_vram_gib = round(total_vram_mib / 1024, 2)

    return {
        "vendor": "NVIDIA",
        "model": model,
        "type": "discrete",
        "driver_model": driver_model,
        "vram": {
            "reported_mib": total_vram_mib,
            "capacity_gib": total_vram_gib,
        },
        "software": {
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
            "cuda_umd_version": (
                version_match.group(3)
                if version_match
                else None
            ),
        },
    }


def load_hardware_profile(submission_folder: Path) -> dict:
    """
    Load and normalize all required hardware files.
    """

    required_files = {
        "cpu": submission_folder / "cpu.txt",
        "memory": submission_folder / "memory.txt",
        "system": submission_folder / "system.txt",
        "windows": submission_folder / "windows.txt",
        "nvidia_smi": submission_folder / "nvidia-smi.txt",
    }

    missing_files = [
        file_path.name
        for file_path in required_files.values()
        if not file_path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required hardware file(s): "
            + ", ".join(missing_files)
        )

    return {
        "system": parse_system(required_files["system"]),
        "cpu": parse_cpu(required_files["cpu"]),
        "memory": parse_memory(required_files["memory"]),
        "operating_system": parse_windows(
            required_files["windows"]
        ),
        "gpu": parse_nvidia_smi(
            required_files["nvidia_smi"]
        ),
    }