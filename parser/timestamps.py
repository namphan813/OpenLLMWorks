"""
OpenLLMBench Timestamp Utilities

Purpose:
Creates, parses, validates, and normalizes timestamps used by
benchmark submissions and persistent database records.

Version:
0.8.0-dev2
"""

from datetime import date, datetime, timezone
from typing import Any


TIMESTAMP_MODULE_VERSION = "0.8.0-dev2"


# ------------------------------------------------------------
# CURRENT TIME
# ------------------------------------------------------------

def utc_now() -> datetime:
    """
    Return the current timezone-aware UTC datetime.
    """

    return datetime.now(timezone.utc)


def utc_timestamp() -> str:
    """
    Return the current UTC time as an ISO 8601 timestamp.

    Example:
        2026-08-02T16:45:00+00:00
    """

    return utc_now().isoformat(
        timespec="seconds"
    )


# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------

def normalize_datetime(
    value: datetime,
) -> datetime:
    """
    Convert one datetime to timezone-aware UTC.

    Naive datetimes are rejected because their timezone cannot
    be safely inferred.
    """

    if value.tzinfo is None:
        raise ValueError(
            "Datetime value has no timezone information."
        )

    return value.astimezone(timezone.utc)


def normalize_timestamp(
    value: Any,
) -> str | None:
    """
    Normalize a supported timestamp value to ISO 8601 UTC.

    Accepted values:

    - timezone-aware datetime
    - date
    - ISO 8601 string
    - None

    Date-only values are stored at midnight UTC.

    Returns:
        A normalized ISO 8601 string, or None when the input is
        None or blank.

    Raises:
        ValueError:
            If the supplied value cannot be safely interpreted.
    """

    if value is None:
        return None

    if isinstance(value, str):
        cleaned = value.strip()

        if not cleaned:
            return None

        return parse_timestamp(cleaned)

    # datetime must be checked before date because datetime
    # is a subclass of date in Python.
    if isinstance(value, datetime):
        normalized = normalize_datetime(value)

        return normalized.isoformat(
            timespec="seconds"
        )

    if isinstance(value, date):
        normalized = datetime(
            year=value.year,
            month=value.month,
            day=value.day,
            tzinfo=timezone.utc,
        )

        return normalized.isoformat(
            timespec="seconds"
        )

    raise ValueError(
        "Timestamp must be an ISO 8601 string, "
        "date, datetime, or None."
    )


# ------------------------------------------------------------
# PARSING
# ------------------------------------------------------------

def parse_date_only(
    value: str,
) -> str:
    """
    Parse an ISO 8601 date and store it as midnight UTC.

    Example:
        2026-08-02
        becomes
        2026-08-02T00:00:00+00:00
    """

    try:
        parsed_date = date.fromisoformat(value)

    except ValueError as error:
        raise ValueError(
            f"Invalid ISO 8601 date: {value!r}"
        ) from error

    parsed_datetime = datetime(
        year=parsed_date.year,
        month=parsed_date.month,
        day=parsed_date.day,
        tzinfo=timezone.utc,
    )

    return parsed_datetime.isoformat(
        timespec="seconds"
    )


def parse_timestamp(
    value: str,
) -> str:
    """
    Parse and normalize one ISO 8601 timestamp string.

    Supported examples:

    - 2026-08-02
    - 2026-08-02T10:30:00-06:00
    - 2026-08-02T16:30:00+00:00
    - 2026-08-02T16:30:00Z

    Date-only values become midnight UTC.
    """

    cleaned = value.strip()

    if not cleaned:
        raise ValueError(
            "Timestamp value cannot be blank."
        )

    # A standard ISO date contains 10 characters:
    # YYYY-MM-DD
    if len(cleaned) == 10:
        return parse_date_only(cleaned)

    if cleaned.endswith("Z"):
        cleaned = (
            cleaned[:-1]
            + "+00:00"
        )

    try:
        parsed = datetime.fromisoformat(
            cleaned
        )

    except ValueError as error:
        raise ValueError(
            f"Invalid ISO 8601 timestamp: {value!r}"
        ) from error

    if parsed.tzinfo is None:
        raise ValueError(
            "Timestamp includes a time but no timezone: "
            f"{value!r}"
        )

    normalized = parsed.astimezone(
        timezone.utc
    )

    return normalized.isoformat(
        timespec="seconds"
    )


# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------

def is_valid_timestamp(
    value: Any,
) -> bool:
    """
    Return True when a value is a valid supported timestamp.
    """

    try:
        normalized = normalize_timestamp(
            value
        )

    except ValueError:
        return False

    return normalized is not None


def compare_timestamps(
    earlier: str,
    later: str,
) -> int:
    """
    Compare two ISO 8601 timestamps.

    Returns:
        -1 when earlier comes first
         0 when both represent the same instant
         1 when earlier actually comes after later
    """

    earlier_normalized = parse_timestamp(
        earlier
    )

    later_normalized = parse_timestamp(
        later
    )

    earlier_datetime = datetime.fromisoformat(
        earlier_normalized
    )

    later_datetime = datetime.fromisoformat(
        later_normalized
    )

    if earlier_datetime < later_datetime:
        return -1

    if earlier_datetime > later_datetime:
        return 1

    return 0