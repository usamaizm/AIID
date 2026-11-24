"""Small standard-library reference helpers for AIID draft 0.1.

This module validates the required structural fields and resolves a descriptor's
local companion resource conservatively. It does not authenticate descriptors,
verify signatures, execute resources, or implement a full JSON Schema engine.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AIIDError(ValueError):
    """Raised when an AIID descriptor is malformed or unsafe to resolve."""


def validate_descriptor(value: Any) -> dict[str, Any]:
    """Validate the mandatory AIID 0.1 structural contract."""
    if not isinstance(value, dict):
        raise AIIDError("descriptor must be a JSON object")
    if value.get("aiid_version") != "0.1":
        raise AIIDError("aiid_version must be '0.1'")
    identity = value.get("identity")
    if not isinstance(identity, dict):
        raise AIIDError("identity must be an object")
    for field in ("id", "type"):
        if not isinstance(identity.get(field), str) or not identity[field].strip():
            raise AIIDError(f"identity.{field} must be a non-empty string")
    resource = value.get("resource")
    if resource is not None and not isinstance(resource, dict):
        raise AIIDError("resource must be an object when present")
    if isinstance(resource, dict):
        for field in ("name", "uri", "media_type"):
            item = resource.get(field)
            if item is not None and not isinstance(item, str):
                raise AIIDError(f"resource.{field} must be a string")
    return value


def load_descriptor(path: str | Path) -> dict[str, Any]:
    """Load a UTF-8 JSON AIID descriptor and validate its core structure."""
    descriptor_path = Path(path)
    try:
        text = descriptor_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise AIIDError(f"cannot read descriptor: {exc}") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AIIDError(f"invalid JSON: {exc}") from exc
    return validate_descriptor(value)


def companion_path(resource_path: str | Path) -> Path:
    """Return the companion path by appending '.aiid' to the full filename."""
    path = Path(resource_path)
    return path.with_name(path.name + ".aiid")


def resolve_local_resource(descriptor_path: str | Path, descriptor: dict[str, Any]) -> Path:
    """Resolve resource.name relative to the descriptor, preventing directory escape.

    Only local relative names are supported here. URI fetching is intentionally
    excluded: descriptors are untrusted data and must not trigger network access.
    """
    descriptor_file = Path(descriptor_path).resolve()
    resource = descriptor.get("resource")
    if not isinstance(resource, dict):
        raise AIIDError("descriptor has no local resource object")
    name = resource.get("name")
    if not isinstance(name, str) or not name:
        raise AIIDError("resource.name is required for local resolution")
    candidate = (descriptor_file.parent / name).resolve()
    try:
        candidate.relative_to(descriptor_file.parent)
    except ValueError as exc:
        raise AIIDError("resource path escapes descriptor directory") from exc
    return candidate
