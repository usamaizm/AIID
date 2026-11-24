# AIID — Artificial Intelligence Identification

AIID is an open, general-purpose identification and description format for digital resources. It gives software and AI agents a portable way to identify a resource and discover machine-readable information about it.

**The companion descriptor uses the .aiid extension.** Append it to the complete resource filename: photo.jpeg.aiid describes photo.jpeg. The original resource remains unchanged; the AIID file describes it rather than replacing it.

## Status

AIID is an early community-designed draft. The repository currently proposes a 0.1 baseline, not a ratified industry standard. The schema and rules are provisional until a stable release is published.

## Core design

- **Descriptor, not payload:** an AIID file identifies and describes a resource; it does not contain the resource's primary payload.
- **Companion naming:** append .aiid to the complete filename, for example model.bin.aiid or photo.jpeg.aiid.
- **Portable baseline:** draft 0.1 uses UTF-8 JSON for inspectability and broad tooling support.
- **Serialization-neutral model:** the information model is separate from JSON. A future binary serialization may be specified without changing field meanings.
- **Optional:** ordinary resources remain usable without AIID descriptors.
- **Broad scope:** AIID can describe files, programs, agents, models, datasets, collections, services, devices, and other resources.
- **Identity is not trust:** an identifier or descriptor is a claim, not proof of authenticity, safety, ownership, or permission.

## Quick example

A resource and its companion descriptor:

    photo.jpeg
    photo.jpeg.aiid

Example descriptor:

    {
      "aiid_version": "0.1",
      "identity": {
        "id": "urn:uuid:00000000-0000-4000-8000-000000000001",
        "type": "image"
      },
      "resource": {
        "name": "photo.jpeg",
        "media_type": "image/jpeg"
      },
      "description": "A sample photograph."
    }

The sample identifier is illustrative only and must not be reused as a real identifier.

## Repository guide

- SPEC.md — draft format and interoperability specification.
- schema/aiid-0.1.schema.json — provisional JSON Schema.
- examples/ — illustrative companion descriptors.
- CONTRIBUTING.md — contribution guidelines.
- ROADMAP.md — proposed development stages.

## Relationship to AIDB

AIID and AIDB have distinct responsibilities. An AIDB file is a data container. An AIID descriptor can identify and describe an AIDB file, just as it can describe a JPEG, program, dataset, or other resource. AIID does not prescribe AIDB internals. Spatial or other specialized payloads can remain in the appropriate resource or container; AIID may describe their type, reference, and relevant metadata without duplicating the payload.

## License

Project materials are provided under the Apache License, Version 2.0. See LICENSE.

## Reference implementation

A minimal Python standard-library helper and unit tests are available in [reference/](reference/README.md). They cover draft 0.1 structural validation, UTF-8 JSON loading, companion filename construction, and safe local path resolution. They are illustrative reference code, not a complete conformance or security implementation.


## Ecosystem integration

This project is part of a set of independent, interoperable open projects. See the [ecosystem integration contract](https://github.com/usamaizm/AIDB/blob/main/docs/ECOSYSTEM_INTEGRATION.md) for its role, interoperability boundaries, and integration principles.


## Contributor attribution

Human and AI contributors must follow the [contributor identity and attribution protocol](CONTRIBUTOR_PROTOCOL.md). Keep the authenticated GitHub account separate from a contributor's self-declared identity; never guess who performed earlier work.
