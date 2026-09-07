"""License and attribution checks.

MuseForge never copies a prompt whose license is unclear. This module maps a license string to
a redistribution decision and records attribution requirements.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LicenseDecision:
    """Whether and how a prompt may be redistributed."""

    license: str
    can_redistribute: bool
    requires_attribution: bool
    share_alike: bool = False
    non_commercial_only: bool = False
    no_derivatives: bool = False
    note: str = ""


# License string (lowercased) → decision. Unknown licenses are treated as non-redistributable.
_LICENSE_TABLE: dict[str, LicenseDecision] = {
    "cc0-1.0": LicenseDecision("CC0-1.0", True, False, note="Public domain dedication."),
    "cc0": LicenseDecision("CC0-1.0", True, False, note="Public domain dedication."),
    "mit": LicenseDecision("MIT", True, True, note="Redistribute with the license notice."),
    "cc by 4.0": LicenseDecision("CC BY 4.0", True, True, note="Redistribute with attribution."),
    "cc-by-4.0": LicenseDecision("CC BY 4.0", True, True, note="Redistribute with attribution."),
    "cc by-sa 4.0": LicenseDecision(
        "CC BY-SA 4.0", True, True, share_alike=True, note="Attribution + share-alike."
    ),
    "cc by-nc 4.0": LicenseDecision(
        "CC BY-NC 4.0", True, True, non_commercial_only=True, note="Non-commercial only."
    ),
    "cc by-nd 4.0": LicenseDecision(
        "CC BY-ND 4.0", True, True, no_derivatives=True, note="No derivatives."
    ),
    "apache-2.0": LicenseDecision("Apache-2.0", True, True, note="Redistribute with the notice."),
}


def decide(license_str: str | None) -> LicenseDecision:
    """Return the redistribution decision for a license string.

    An empty or unrecognized license is treated as non-redistributable (the safe default).
    """
    if not license_str:
        return LicenseDecision(
            "", False, True, note="No license — do not copy the prompt text."
        )
    key = license_str.strip().lower()
    if key in _LICENSE_TABLE:
        return _LICENSE_TABLE[key]
    return LicenseDecision(
        license_str,
        False,
        True,
        note="Unrecognized license — do not copy the prompt text; store metadata + analysis only.",
    )


def can_redistribute(license_str: str | None) -> bool:
    return decide(license_str).can_redistribute
