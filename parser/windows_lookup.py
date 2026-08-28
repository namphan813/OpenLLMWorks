"""
Windows operating-system normalization for OpenLLMWorks.

PowerShell and WMI may report Windows 11 as "Windows 10."
The OS build number is therefore used to identify the actual
Windows client release.

Raw reported values are always preserved elsewhere in the database.
"""


WINDOWS_CLIENT_BUILDS = {
    19045: {
        "family": "Windows 10",
        "release": "22H2",
    },
    22000: {
        "family": "Windows 11",
        "release": "21H2",
    },
    22621: {
        "family": "Windows 11",
        "release": "22H2",
    },
    22631: {
        "family": "Windows 11",
        "release": "23H2",
    },
    26100: {
        "family": "Windows 11",
        "release": "24H2",
    },
    26200: {
        "family": "Windows 11",
        "release": "25H2",
    },
}


def extract_edition(reported_name: str | None) -> str | None:
    """
    Extract an edition such as Pro, Home, Enterprise, or Education
    from the name reported by Windows.
    """

    if not reported_name:
        return None

    known_editions = [
        "Pro for Workstations",
        "Pro Education",
        "Enterprise",
        "Education",
        "Professional",
        "Pro",
        "Home",
    ]

    reported_name_lower = reported_name.lower()

    for edition in known_editions:
        if edition.lower() in reported_name_lower:
            if edition == "Professional":
                return "Pro"

            return edition

    return None


def normalize_windows(
    reported_name: str | None,
    reported_version: str | None,
    build: int | None,
) -> dict:
    """
    Normalize Windows client information using its base OS build.

    Unknown builds are preserved without guessing a feature release.
    """

    edition = extract_edition(reported_name)

    normalized = {
        "family": None,
        "edition": edition,
        "name": None,
        "release": None,
        "recognition_status": "unknown",
    }

    if build is None:
        return normalized

    build_record = WINDOWS_CLIENT_BUILDS.get(build)

    if build_record is not None:
        family = build_record["family"]
        release = build_record["release"]

        normalized["family"] = family
        normalized["release"] = release
        normalized["recognition_status"] = "recognized_build"

        if edition:
            normalized["name"] = f"{family} {edition}"
        else:
            normalized["name"] = family

        return normalized

    # Conservative fallback for unknown Windows client builds.
    # We identify the broad family but do not invent a release name.
    if build >= 22000:
        normalized["family"] = "Windows 11"
        normalized["recognition_status"] = "inferred_family"

    elif build >= 10240:
        normalized["family"] = "Windows 10"
        normalized["recognition_status"] = "inferred_family"

    if normalized["family"] and edition:
        normalized["name"] = (
            f"{normalized['family']} {edition}"
        )

    else:
        normalized["name"] = normalized["family"]

    return normalized