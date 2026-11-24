"""Small standard-library reference helpers for AIID draft 0.1.

This module validates descriptors against the structural and type rules in
``schema/aiid-0.1.schema.json`` for every field that schema constrains, with
one disclosed exception: ``resource.uri`` is checked only as a string, not
for ``format: uri`` semantics. It resolves a descriptor's local companion
resource conservatively. It does not authenticate descriptors, verify
signatures, execute resources, or implement a full JSON Schema engine.
"""
from __future__ import annotations

import json
from pathlib import Path, PureWindowsPath
from typing import Any


class AIIDError(ValueError):
    """Raised when an AIID descriptor is malformed or unsafe to resolve."""


def _require_non_empty_string(container: dict[str, Any], field: str, label: str) -> None:
    item = container.get(field)
    if not isinstance(item, str) or len(item) < 1:
        raise AIIDError(f"{label} must be a non-empty string")


def validate_descriptor(value: Any) -> dict[str, Any]:
    """Validate the AIID 0.1 contract in ``schema/aiid-0.1.schema.json``.

    The verdicts match the schema for every field it constrains, except
    ``format: uri`` on ``resource.uri``, which is checked only as a string.
    Unknown fields and unknown identity type labels are tolerated, as the
    schema and SPEC require. A whitespace-only string satisfies the
    schema's ``minLength: 1`` and is therefore accepted: neither the schema
    nor SPEC section 5 defines a trimming rule for identity fields.
    """
    if not isinstance(value, dict):
        raise AIIDError("descriptor must be a JSON object")
    if value.get("aiid_version") != "0.1":
        raise AIIDError("aiid_version must be '0.1'")
    identity = value.get("identity")
    if not isinstance(identity, dict):
        raise AIIDError("identity must be an object")
    for field in ("id", "type"):
        _require_non_empty_string(identity, field, f"identity.{field}")
    for field in ("version", "scheme"):
        if field in identity:
            _require_non_empty_string(identity, field, f"identity.{field}")
    if "resource" in value:
        resource = value["resource"]
        if not isinstance(resource, dict):
            raise AIIDError("resource must be an object when present")
        for field in ("name", "media_type"):
            if field in resource:
                _require_non_empty_string(resource, field, f"resource.{field}")
        if "uri" in resource and not isinstance(resource["uri"], str):
            raise AIIDError("resource.uri must be a string")
    if "description" in value and not isinstance(value["description"], str):
        raise AIIDError("description must be a string")
    for field in ("metadata", "provenance", "integrity"):
        if field in value and not isinstance(value[field], dict):
            raise AIIDError(f"{field} must be an object when present")
    if "links" in value:
        links = value["links"]
        if not isinstance(links, list):
            raise AIIDError("links must be an array when present")
        for item in links:
            if not isinstance(item, dict):
                raise AIIDError("links items must be objects")
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
    relative_name = Path(name)
    windows_name = PureWindowsPath(name)
    if relative_name.is_absolute() or windows_name.is_absolute():
        raise AIIDError("resource.name must be a relative path")
    if ".." in relative_name.parts or ".." in windows_name.parts:
        raise AIIDError("resource.name must not contain parent-directory traversal")
    candidate = (descriptor_file.parent / relative_name).resolve()
    try:
        candidate.relative_to(descriptor_file.parent)
    except ValueError as exc:
        raise AIIDError("resource path escapes descriptor directory") from exc
    return candidate
