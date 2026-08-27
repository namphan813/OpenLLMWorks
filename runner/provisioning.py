"""
OpenLLMBench Runner asset provisioning.

This module owns managed benchmark asset inspection, verified
artifact acquisition, and installation.

Provisioning is intentionally separate from benchmark execution
so protocol assets can be validated before the Runner attempts
to use them.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json
import shutil
import tempfile
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import zipfile


DOWNLOAD_CHUNK_SIZE = 1024 * 1024
DOWNLOAD_USER_AGENT = "OpenLLMBench-Runner/0.3"


def calculate_sha256(
    file_path: Path,
) -> str:
    """
    Calculate the uppercase SHA-256 digest for one file.
    """

    digest = sha256()

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(
                DOWNLOAD_CHUNK_SIZE
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest().upper()


def load_asset_manifest(
    manifest_path: Path,
) -> dict[str, Any]:
    """
    Load and minimally validate the Runner asset manifest.
    """

    if not manifest_path.is_file():
        raise RuntimeError(
            "Asset manifest was not found: "
            f"{manifest_path}"
        )

    try:
        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

    except (
        OSError,
        json.JSONDecodeError,
    ) as error:
        raise RuntimeError(
            "Asset manifest could not be loaded: "
            f"{error}"
        ) from error

    required_top_level = (
        "schema_version",
        "protocol_version",
        "platform",
        "accelerator",
        "assets",
    )

    for field in required_top_level:
        if field not in manifest:
            raise RuntimeError(
                "Asset manifest is missing "
                f"required field: {field}"
            )

    assets = manifest["assets"]

    if not isinstance(
        assets,
        dict,
    ):
        raise RuntimeError(
            "Asset manifest field 'assets' "
            "must be an object."
        )

    if "model" not in assets:
        raise RuntimeError(
            "Asset manifest is missing "
            "the model definition."
        )

    if "runtime" not in assets:
        raise RuntimeError(
            "Asset manifest is missing "
            "the runtime definition."
        )

    return manifest


def verify_file_identity(
    *,
    file_path: Path,
    expected_size: int,
    expected_sha256: str,
    label: str,
) -> tuple[bool, str]:
    """
    Verify one file using exact byte size and SHA-256.
    """

    if not file_path.is_file():
        return (
            False,
            f"{label} was not found.",
        )

    try:
        actual_size = file_path.stat().st_size

    except OSError as error:
        return (
            False,
            f"Could not inspect {label}: {error}",
        )

    if actual_size != int(expected_size):
        return (
            False,
            f"{label} size does not match.",
        )

    try:
        actual_sha256 = calculate_sha256(
            file_path
        )

    except OSError as error:
        return (
            False,
            f"Could not hash {label}: {error}",
        )

    if (
        actual_sha256.upper()
        != str(expected_sha256).upper()
    ):
        return (
            False,
            f"{label} SHA-256 does not match.",
        )

    return (
        True,
        f"{label} size and SHA-256 verified.",
    )


def download_verified_file(
    *,
    url: str,
    destination: Path,
    expected_size: int,
    expected_sha256: str,
    label: str,
) -> tuple[bool, str]:
    """
    Download one canonical artifact to a temporary partial file.

    The completed download is promoted to its canonical artifact
    path only after exact size and SHA-256 verification succeeds.
    Existing verified artifacts are reused.
    """

    existing_ok, existing_message = (
        verify_file_identity(
            file_path=destination,
            expected_size=expected_size,
            expected_sha256=expected_sha256,
            label=label,
        )
    )

    if existing_ok:
        return (
            True,
            "Existing artifact reused. "
            f"{existing_message}"
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    partial_path = destination.with_name(
        destination.name + ".part"
    )

    if partial_path.exists():
        partial_path.unlink()

    request = Request(
        url,
        headers={
            "User-Agent": DOWNLOAD_USER_AGENT,
        },
    )

    try:
        with urlopen(
            request,
            timeout=60,
        ) as response:
            with partial_path.open(
                "wb"
            ) as output:
                while True:
                    chunk = response.read(
                        DOWNLOAD_CHUNK_SIZE
                    )

                    if not chunk:
                        break

                    output.write(chunk)

    except (
        HTTPError,
        URLError,
        TimeoutError,
        OSError,
    ) as error:
        if partial_path.exists():
            partial_path.unlink()

        return (
            False,
            f"{label} download failed: {error}",
        )

    verified_ok, verified_message = (
        verify_file_identity(
            file_path=partial_path,
            expected_size=expected_size,
            expected_sha256=expected_sha256,
            label=label,
        )
    )

    if not verified_ok:
        if partial_path.exists():
            partial_path.unlink()

        return (
            False,
            verified_message,
        )

    try:
        partial_path.replace(
            destination
        )

    except OSError as error:
        if partial_path.exists():
            partial_path.unlink()

        return (
            False,
            f"Could not promote {label}: {error}",
        )

    return (
        True,
        f"{label} downloaded and verified.",
    )


def inspect_model(
    *,
    protocol_root: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Inspect the installed benchmark model.
    """

    model = manifest["assets"]["model"]

    install_path = model.get(
        "install_path"
    )

    expected_sha256 = model.get(
        "sha256"
    )

    if not install_path:
        return (
            False,
            "Model manifest does not define "
            "install_path.",
        )

    if not expected_sha256:
        return (
            False,
            "Model manifest does not define "
            "sha256.",
        )

    model_path = (
        protocol_root
        / install_path
    )

    if not model_path.is_file():
        return (
            False,
            "Managed benchmark model "
            "is not installed.",
        )

    try:
        actual_sha256 = calculate_sha256(
            model_path
        )

    except OSError as error:
        return (
            False,
            "Could not verify managed model: "
            f"{error}",
        )

    if (
        actual_sha256.upper()
        != str(expected_sha256).upper()
    ):
        return (
            False,
            "Managed benchmark model "
            "SHA-256 does not match.",
        )

    return (
        True,
        "Managed benchmark model is installed "
        "and verified.",
    )


def verify_model_artifact(
    *,
    artifact_path: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Verify the canonical local benchmark-model artifact.
    """

    model = manifest["assets"]["model"]

    expected_size = model.get(
        "size_bytes"
    )

    expected_sha256 = model.get(
        "sha256"
    )

    if expected_size is None:
        return (
            False,
            "Model manifest does not define "
            "size_bytes.",
        )

    if not expected_sha256:
        return (
            False,
            "Model manifest does not define "
            "sha256.",
        )

    return verify_file_identity(
        file_path=artifact_path,
        expected_size=int(expected_size),
        expected_sha256=str(expected_sha256),
        label="Benchmark model artifact",
    )


def provision_model_from_artifact(
    *,
    protocol_root: Path,
    artifact_path: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Install the benchmark model from a verified local artifact.

    The model is copied into a staging location, verified there,
    then promoted into the managed protocol directory.
    """

    model = manifest["assets"]["model"]

    install_path = model.get(
        "install_path"
    )

    if not install_path:
        return (
            False,
            "Model manifest does not define "
            "install_path.",
        )

    artifact_ok, artifact_message = (
        verify_model_artifact(
            artifact_path=artifact_path,
            manifest=manifest,
        )
    )

    if not artifact_ok:
        return (
            False,
            artifact_message,
        )

    protocol_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        protocol_root
        / install_path
    )

    model_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    staging_parent = (
        protocol_root
        / ".staging"
    )

    staging_parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    staging_root = Path(
        tempfile.mkdtemp(
            prefix="model-",
            dir=staging_parent,
        )
    )

    staged_model = (
        staging_root
        / model_path.name
    )

    backup_path = model_path.with_name(
        model_path.name + ".backup"
    )

    try:
        shutil.copy2(
            artifact_path,
            staged_model,
        )

        staged_sha256 = calculate_sha256(
            staged_model
        )

        expected_sha256 = str(
            model["sha256"]
        ).upper()

        if staged_sha256.upper() != expected_sha256:
            return (
                False,
                "Staged benchmark model "
                "SHA-256 does not match.",
            )

        if backup_path.exists():
            backup_path.unlink()

        if model_path.exists():
            shutil.move(
                str(model_path),
                str(backup_path),
            )

        try:
            shutil.move(
                str(staged_model),
                str(model_path),
            )

        except Exception:
            if (
                backup_path.exists()
                and not model_path.exists()
            ):
                shutil.move(
                    str(backup_path),
                    str(model_path),
                )

            raise

        installed_ok, installed_message = (
            inspect_model(
                protocol_root=protocol_root,
                manifest=manifest,
            )
        )

        if not installed_ok:
            if model_path.exists():
                model_path.unlink()

            if backup_path.exists():
                shutil.move(
                    str(backup_path),
                    str(model_path),
                )

            return (
                False,
                "Installed model verification failed: "
                f"{installed_message}"
            )

        if backup_path.exists():
            backup_path.unlink()

        return (
            True,
            "Managed benchmark model was provisioned "
            "and verified successfully.",
        )

    except OSError as error:
        return (
            False,
            "Model provisioning failed: "
            f"{error}",
        )

    finally:
        if staging_root.exists():
            shutil.rmtree(
                staging_root,
                ignore_errors=True,
            )

        if (
            staging_parent.exists()
            and not any(
                staging_parent.iterdir()
            )
        ):
            staging_parent.rmdir()


def inspect_runtime(
    *,
    protocol_root: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Inspect the installed managed runtime.

    All manifest-required runtime files must be present and the
    critical benchmark executable must match its frozen hash.
    """

    runtime = manifest["assets"]["runtime"]

    install_path = runtime.get(
        "install_path"
    )

    critical_file = runtime.get(
        "critical_file"
    )

    expected_sha256 = runtime.get(
        "critical_file_sha256"
    )

    required_files = runtime.get(
        "required_files"
    )

    if not install_path:
        return (
            False,
            "Runtime manifest does not define "
            "install_path.",
        )

    if not critical_file:
        return (
            False,
            "Runtime manifest does not define "
            "critical_file.",
        )

    if not expected_sha256:
        return (
            False,
            "Runtime manifest does not define "
            "critical_file_sha256.",
        )

    if not isinstance(
        required_files,
        list,
    ) or not required_files:
        return (
            False,
            "Runtime manifest does not define "
            "required_files.",
        )

    runtime_root = (
        protocol_root
        / install_path
    )

    if not runtime_root.is_dir():
        return (
            False,
            "Managed runtime directory "
            "is not installed.",
        )

    missing_files = [
        name
        for name in required_files
        if not (
            runtime_root
            / name
        ).is_file()
    ]

    if missing_files:
        return (
            False,
            "Managed runtime is missing required file: "
            f"{missing_files[0]}",
        )

    critical_path = (
        runtime_root
        / critical_file
    )

    try:
        actual_sha256 = calculate_sha256(
            critical_path
        )

    except OSError as error:
        return (
            False,
            "Could not verify managed runtime: "
            f"{error}",
        )

    if (
        actual_sha256.upper()
        != str(expected_sha256).upper()
    ):
        return (
            False,
            "Managed runtime critical-file "
            "SHA-256 does not match.",
        )

    return (
        True,
        "Managed runtime is installed "
        "and verified.",
    )


def verify_runtime_source(
    *,
    archive_path: Path,
    source: dict[str, Any],
) -> tuple[bool, str]:
    """
    Verify one frozen upstream runtime archive.
    """

    expected_size = source.get(
        "size_bytes"
    )

    expected_sha256 = source.get(
        "sha256"
    )

    source_id = str(
        source.get(
            "id",
            source.get(
                "filename",
                "Runtime source",
            ),
        )
    )

    if expected_size is None:
        return (
            False,
            f"{source_id} does not define size_bytes.",
        )

    if not expected_sha256:
        return (
            False,
            f"{source_id} does not define sha256.",
        )

    return verify_file_identity(
        file_path=archive_path,
        expected_size=int(expected_size),
        expected_sha256=str(expected_sha256),
        label=f"Runtime source {source_id}",
    )


def _safe_extract_zip(
    *,
    archive_path: Path,
    destination: Path,
) -> None:
    """
    Extract a ZIP archive while rejecting paths outside destination.
    """

    destination_resolved = destination.resolve()

    try:
        with zipfile.ZipFile(
            archive_path,
            mode="r",
        ) as archive:
            for member in archive.infolist():
                member_path = (
                    destination
                    / member.filename
                )

                member_resolved = (
                    member_path.resolve()
                )

                try:
                    member_resolved.relative_to(
                        destination_resolved
                    )

                except ValueError as error:
                    raise RuntimeError(
                        "Runtime archive contains an "
                        "unsafe path: "
                        f"{member.filename}"
                    ) from error

            archive.extractall(
                destination
            )

    except zipfile.BadZipFile as error:
        raise RuntimeError(
            "Runtime archive is not a valid ZIP file."
        ) from error


def _find_required_runtime_file(
    *,
    extracted_roots: list[Path],
    filename: str,
) -> Path:
    """
    Locate one required runtime file in extracted source archives.
    """

    matches: list[Path] = []

    for root in extracted_roots:
        matches.extend(
            path
            for path in root.rglob(
                filename
            )
            if path.is_file()
        )

    if not matches:
        raise RuntimeError(
            "Required runtime file was not found "
            f"in upstream sources: {filename}"
        )

    if len(matches) > 1:
        hashes = {
            calculate_sha256(
                path
            )
            for path in matches
        }

        if len(hashes) != 1:
            raise RuntimeError(
                "Multiple different upstream files "
                f"matched required runtime file: {filename}"
            )

    return matches[0]


def provision_runtime_from_sources(
    *,
    protocol_root: Path,
    artifact_paths: dict[str, Path],
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Assemble the managed runtime from frozen upstream archives.

    Every source archive is verified before extraction. Only the
    manifest-defined runtime subset is promoted into the managed
    protocol runtime directory.
    """

    runtime = manifest["assets"]["runtime"]

    install_path = runtime.get(
        "install_path"
    )

    sources = runtime.get(
        "sources"
    )

    required_files = runtime.get(
        "required_files"
    )

    if not install_path:
        return (
            False,
            "Runtime manifest does not define "
            "install_path.",
        )

    if not isinstance(
        sources,
        list,
    ) or not sources:
        return (
            False,
            "Runtime manifest does not define sources.",
        )

    if not isinstance(
        required_files,
        list,
    ) or not required_files:
        return (
            False,
            "Runtime manifest does not define "
            "required_files.",
        )

    for source in sources:
        source_id = source.get(
            "id"
        )

        if not source_id:
            return (
                False,
                "Runtime source does not define id.",
            )

        archive_path = artifact_paths.get(
            str(source_id)
        )

        if archive_path is None:
            return (
                False,
                "Runtime artifact path was not supplied "
                f"for source: {source_id}",
            )

        source_ok, source_message = (
            verify_runtime_source(
                archive_path=archive_path,
                source=source,
            )
        )

        if not source_ok:
            return (
                False,
                source_message,
            )

    protocol_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    runtime_root = (
        protocol_root
        / install_path
    )

    staging_parent = (
        protocol_root
        / ".staging"
    )

    staging_parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    staging_root = Path(
        tempfile.mkdtemp(
            prefix="runtime-",
            dir=staging_parent,
        )
    )

    extracted_roots: list[Path] = []

    staged_runtime = (
        staging_root
        / install_path
    )

    backup_root = (
        protocol_root
        / ".runtime-backup"
    )

    try:
        staged_runtime.mkdir(
            parents=True,
            exist_ok=False,
        )

        extracted_parent = (
            staging_root
            / "sources"
        )

        extracted_parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        for source in sources:
            source_id = str(
                source["id"]
            )

            archive_path = (
                artifact_paths[
                    source_id
                ]
            )

            extracted_root = (
                extracted_parent
                / source_id
            )

            extracted_root.mkdir(
                parents=True,
                exist_ok=False,
            )

            _safe_extract_zip(
                archive_path=archive_path,
                destination=extracted_root,
            )

            extracted_roots.append(
                extracted_root
            )

        for filename in required_files:
            source_file = (
                _find_required_runtime_file(
                    extracted_roots=extracted_roots,
                    filename=str(filename),
                )
            )

            shutil.copy2(
                source_file,
                staged_runtime
                / str(filename),
            )

        staged_ok, staged_message = (
            inspect_runtime(
                protocol_root=staging_root,
                manifest=manifest,
            )
        )

        if not staged_ok:
            return (
                False,
                "Staged runtime verification failed: "
                f"{staged_message}"
            )

        if backup_root.exists():
            shutil.rmtree(
                backup_root
            )

        if runtime_root.exists():
            shutil.move(
                str(runtime_root),
                str(backup_root),
            )

        try:
            shutil.move(
                str(staged_runtime),
                str(runtime_root),
            )

        except Exception:
            if (
                backup_root.exists()
                and not runtime_root.exists()
            ):
                shutil.move(
                    str(backup_root),
                    str(runtime_root),
                )

            raise

        installed_ok, installed_message = (
            inspect_runtime(
                protocol_root=protocol_root,
                manifest=manifest,
            )
        )

        if not installed_ok:
            if runtime_root.exists():
                shutil.rmtree(
                    runtime_root
                )

            if backup_root.exists():
                shutil.move(
                    str(backup_root),
                    str(runtime_root),
                )

            return (
                False,
                "Installed runtime verification failed: "
                f"{installed_message}"
            )

        if backup_root.exists():
            shutil.rmtree(
                backup_root
            )

        return (
            True,
            "Managed runtime was assembled from "
            "verified upstream sources successfully.",
        )

    except (
        OSError,
        RuntimeError,
    ) as error:
        return (
            False,
            "Runtime provisioning failed: "
            f"{error}",
        )

    finally:
        if staging_root.exists():
            shutil.rmtree(
                staging_root,
                ignore_errors=True,
            )

        if (
            staging_parent.exists()
            and not any(
                staging_parent.iterdir()
            )
        ):
            staging_parent.rmdir()


def provision_runtime_from_archive(
    *,
    protocol_root: Path,
    archive_path: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Compatibility shim for the retired single-archive runtime.

    Manifest schema 1.1 uses frozen upstream runtime sources
    instead of one OpenLLMBench-hosted runtime archive.
    """

    del protocol_root
    del archive_path
    del manifest

    return (
        False,
        "Single-archive runtime provisioning is retired. "
        "Use provision_runtime_from_sources().",
    )
