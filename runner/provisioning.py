"""
OpenLLMBench Runner asset provisioning.

This module owns managed benchmark asset inspection and
installation.

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
import zipfile


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
                1024 * 1024
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


def inspect_runtime(
    *,
    protocol_root: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Inspect the installed managed runtime.

    This verifies the critical benchmark executable defined in
    the asset manifest.
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

    runtime_root = (
        protocol_root
        / install_path
    )

    critical_path = (
        runtime_root
        / critical_file
    )

    if not runtime_root.is_dir():
        return (
            False,
            "Managed runtime directory "
            "is not installed.",
        )

    if not critical_path.is_file():
        return (
            False,
            "Managed runtime is missing "
            f"{critical_file}.",
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


def verify_runtime_archive(
    *,
    archive_path: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Verify the canonical runtime archive using size and SHA-256.
    """

    runtime = manifest["assets"]["runtime"]

    expected_size = runtime.get(
        "archive_size_bytes"
    )

    expected_sha256 = runtime.get(
        "archive_sha256"
    )

    if expected_size is None:
        return (
            False,
            "Runtime manifest does not define "
            "archive_size_bytes.",
        )

    if not expected_sha256:
        return (
            False,
            "Runtime manifest does not define "
            "archive_sha256.",
        )

    if not archive_path.is_file():
        return (
            False,
            "Runtime archive was not found.",
        )

    try:
        actual_size = archive_path.stat().st_size

    except OSError as error:
        return (
            False,
            "Could not inspect runtime archive: "
            f"{error}",
        )

    if actual_size != int(expected_size):
        return (
            False,
            "Runtime archive size does not match.",
        )

    try:
        actual_sha256 = calculate_sha256(
            archive_path
        )

    except OSError as error:
        return (
            False,
            "Could not hash runtime archive: "
            f"{error}",
        )

    if (
        actual_sha256.upper()
        != str(expected_sha256).upper()
    ):
        return (
            False,
            "Runtime archive SHA-256 does not match.",
        )

    return (
        True,
        "Runtime archive size and SHA-256 verified.",
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

                try:
                    member_resolved = (
                        member_path.resolve()
                    )

                except OSError as error:
                    raise RuntimeError(
                        "Could not resolve runtime archive "
                        f"entry: {member.filename}"
                    ) from error

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


def provision_runtime_from_archive(
    *,
    protocol_root: Path,
    archive_path: Path,
    manifest: dict[str, Any],
) -> tuple[bool, str]:
    """
    Install the managed runtime from a verified local archive.

    The archive is verified before extraction. Extraction occurs
    in a staging directory. The staged runtime must pass critical
    file verification before it replaces the managed runtime.
    """

    runtime = manifest["assets"]["runtime"]

    install_path = runtime.get(
        "install_path"
    )

    if not install_path:
        return (
            False,
            "Runtime manifest does not define "
            "install_path.",
        )

    archive_ok, archive_message = (
        verify_runtime_archive(
            archive_path=archive_path,
            manifest=manifest,
        )
    )

    if not archive_ok:
        return (
            False,
            archive_message,
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

        _safe_extract_zip(
            archive_path=archive_path,
            destination=staged_runtime,
        )

        staged_protocol_root = (
            staging_root
        )

        staged_ok, staged_message = (
            inspect_runtime(
                protocol_root=staged_protocol_root,
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
            "Managed runtime was provisioned "
            "and verified successfully.",
        )

    except (
        OSError,
        RuntimeError,
        zipfile.BadZipFile,
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
