"""OpenLLMWorks accelerator identity verifier (development candidate).

Checks consistency between the selection manifest, saved llama.cpp device
discovery, and (for Vulkan) independently collected Windows controller data.

Evidence consistency is not proof of physical execution or authenticity.
Historical CUDA submissions without selection metadata use the legacy path.
"""

import json
from pathlib import Path
import re


class DeviceIdentityError(ValueError):
    """Accelerator selection evidence is missing or inconsistent."""


def _normalize(name: str) -> str:
    name = name.casefold()

    for term in ("(r)", "(tm)", "series"):
        name = name.replace(term, " ")

    tokens = re.findall(r"[a-z0-9]+", name)

    if tokens and tokens[0] in ("amd", "nvidia", "intel"):
        tokens = tokens[1:]

    return " ".join(tokens)


def _matches(a: str, b: str) -> bool:
    left = _normalize(a)
    right = _normalize(b)
    return bool(left and right and left == right)


def _parse_devices(text: str, backend: str) -> list[dict]:
    pattern = re.compile(
        r"^\s*([A-Za-z]+[0-9]+):\s*(.+?)"
        r"(?:\s+\((\d+)\s+MiB,\s*(\d+)\s+MiB free\))?\s*$"
    )

    devices = []

    for line in text.splitlines():
        match = pattern.match(line)

        if match and re.fullmatch(
            re.escape(backend) + r"[0-9]+",
            match.group(1),
            re.IGNORECASE,
        ):
            devices.append({
                "device_id": match.group(1),
                "name": match.group(2).strip(),
                "reported_memory_mib": (
                    int(match.group(3))
                    if match.group(3) is not None
                    else None
                ),
                "reported_free_memory_mib": (
                    int(match.group(4))
                    if match.group(4) is not None
                    else None
                ),
            })

    return devices


def _read_windows_controllers(path: Path) -> list[dict]:
    """Read independent Windows controller evidence from system.txt."""

    try:
        from parser.hardware import parse_video_controllers
        return parse_video_controllers(path / "system.txt")
    except (OSError, UnicodeError, ValueError) as exc:
        raise DeviceIdentityError(
            f"Cannot read Windows controller evidence: {exc}"
        ) from exc


def _verify_windows_evidence(
    path: Path,
    windows: dict,
    submission_backend: str,
) -> None:
    controllers = _read_windows_controllers(path)

    if not controllers:
        raise DeviceIdentityError(
            "Vulkan submission requires VIDEO CONTROLLERS in system.txt."
        )

    selected_name = windows["name"]
    matches = [
        controller
        for controller in controllers
        if isinstance(controller.get("name"), str)
        and _matches(selected_name, controller["name"])
    ]

    if len(matches) != 1:
        raise DeviceIdentityError(
            f"Selected Windows GPU matches {len(matches)} controllers; "
            "expected exactly one."
        )

    recorded_pnp = windows.get("pnp_device_id")

    if not isinstance(recorded_pnp, str) or not recorded_pnp.strip():
        raise DeviceIdentityError(
            "Vulkan selection requires a Windows PNP device ID."
        )

    pci = matches[0].get("pci")

    if not isinstance(pci, dict):
        raise DeviceIdentityError(
            "Matching Windows controller lacks parseable PCI evidence."
        )

    evidence_pnp = pci.get("pnp_device_id")

    if not isinstance(evidence_pnp, str) or (
        recorded_pnp.strip().casefold()
        != evidence_pnp.strip().casefold()
    ):
        raise DeviceIdentityError(
            "Selected Windows PNP device ID disagrees with system.txt."
        )

    vendor_id = str(pci.get("vendor_id") or "").upper()
    expected_vendor = {
        "amd": "1002",
        "nvidia": "10DE",
        "intel": "8086",
    }

    vendor = windows.get("vendor")

    if vendor in expected_vendor and (
        vendor_id != expected_vendor[vendor]
    ):
        raise DeviceIdentityError(
            "Selected GPU vendor disagrees with Windows PCI evidence."
        )

    if vendor_id not in expected_vendor.values():
        raise DeviceIdentityError(
            "Windows controller has an unsupported PCI vendor."
        )

    expected_backend = (
        "cuda" if vendor_id == "10DE" else "vulkan"
    )

    if windows.get("backend") not in (None, expected_backend):
        raise DeviceIdentityError(
            "Windows GPU backend disagrees with PCI vendor."
        )

    if submission_backend != expected_backend:
        raise DeviceIdentityError(
            "Submission backend disagrees with Windows PCI vendor."
        )


def verify_device_identity(submission_path: Path) -> dict:
    path = Path(submission_path)

    try:
        selection = json.loads(
            (path / "selected-accelerator.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise DeviceIdentityError(
            f"Cannot read accelerator selection: {exc}"
        ) from exc

    if not isinstance(selection, dict):
        raise DeviceIdentityError("Selection must be a JSON object.")

    backend = selection.get("backend")

    if backend not in ("cuda", "vulkan"):
        raise DeviceIdentityError(
            "Backend must be 'cuda' or 'vulkan'."
        )

    windows = selection.get("windows_accelerator")
    runtime = selection.get("runtime_device")

    if not isinstance(windows, dict) or not isinstance(runtime, dict):
        raise DeviceIdentityError(
            "Windows accelerator and runtime device objects are required."
        )

    windows_name = windows.get("name")
    runtime_name = runtime.get("name")
    device_id = runtime.get("device_id")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (windows_name, runtime_name, device_id)
    ):
        raise DeviceIdentityError(
            "GPU names and runtime device ID must be nonempty strings."
        )

    if not re.fullmatch(
        re.escape(backend) + r"[0-9]+",
        device_id,
        re.IGNORECASE,
    ):
        raise DeviceIdentityError(
            "Runtime device ID does not match selected backend."
        )

    if not _matches(windows_name, runtime_name):
        raise DeviceIdentityError(
            "Windows GPU name and runtime GPU name disagree."
        )

    evidence_file = (
        "vulkan-devices.txt"
        if backend == "vulkan"
        else "cuda-devices.txt"
    )

    try:
        evidence = (path / evidence_file).read_text(
            encoding="utf-8-sig"
        )
    except (OSError, UnicodeError) as exc:
        raise DeviceIdentityError(
            f"Cannot read runtime discovery evidence: {exc}"
        ) from exc

    devices = _parse_devices(evidence, backend)

    if not devices:
        raise DeviceIdentityError(
            "Runtime discovery contains no matching backend devices."
        )

    ids = [item["device_id"].casefold() for item in devices]

    if len(ids) != len(set(ids)):
        raise DeviceIdentityError(
            "Duplicate runtime device IDs in evidence."
        )

    matches = [
        item for item in devices
        if _matches(windows_name, item["name"])
    ]

    if len(matches) != 1:
        raise DeviceIdentityError(
            f"Windows GPU matches {len(matches)} runtime devices; "
            "expected exactly one."
        )

    match = matches[0]

    if (
        match["device_id"].casefold() != device_id.casefold()
        or not _matches(runtime_name, match["name"])
    ):
        raise DeviceIdentityError(
            "Recorded runtime device differs from discovery evidence."
        )

    if backend == "vulkan":
        _verify_windows_evidence(path, windows, backend)

        total = match["reported_memory_mib"]
        free = match["reported_free_memory_mib"]

        if (
            total is None
            or free is None
            or total <= 0
            or free < 0
            or free > total
        ):
            raise DeviceIdentityError(
                "Invalid or missing Vulkan memory evidence."
            )

        if (
            type(runtime.get("reported_memory_mib")) is not int
            or type(runtime.get("reported_free_memory_mib")) is not int
            or runtime["reported_memory_mib"] != total
            or runtime["reported_free_memory_mib"] != free
        ):
            raise DeviceIdentityError(
                "Vulkan memory evidence disagrees with selection manifest."
            )

    return {
        "backend": backend,
        "device_id": match["device_id"],
        "gpu_name": match["name"],
        "verification": "evidence_consistent",
        "reported_memory_mib": (
            match["reported_memory_mib"]
            if backend == "vulkan"
            else None
        ),
        "reported_free_memory_mib": (
            match["reported_free_memory_mib"]
            if backend == "vulkan"
            else None
        ),
    }
