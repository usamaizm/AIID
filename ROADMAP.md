# AIID Roadmap

This roadmap is a proposal, not a promise or a ratified release schedule.

## Stage 1 — Establish the descriptor

- Publish AIID's purpose and scope.
- Define .aiid as a companion descriptor suffix, including names such as photo.jpeg.aiid.
- Publish the draft 0.1 UTF-8 JSON baseline and provisional schema.
- Add examples for ordinary files and AIDB containers.
- Document that descriptors are optional and untrusted by default.

## Stage 2 — Validate the model

- Gather feedback from implementers and AI-agent developers.
- Test discovery behavior across filesystems and package layouts.
- Refine resource types, identifiers, references, and collection handling.
- Add validation fixtures and a reference parser/writer.

## Stage 3 — Interoperability

- Define identifier scheme and version/instance semantics.
- Define extension namespacing and compatibility rules.
- Consider a formal media type and schema publication location.
- Evaluate binary serialization only with demonstrated use cases and equivalent test vectors.

## Stage 4 — Advanced metadata

- Specify provenance and cryptographic verification profiles.
- Develop safe trust and permission integrations without conflating identity with authorization.
- Define optional spatial metadata profiles or references in coordination with relevant payload/container formats.

## Principles

- Keep the core small.
- Preserve compatibility and tolerate unknown extensions.
- Keep AIID independent of any particular model, agent framework, programming language, or operating system.
- Do not make AIID mandatory for ordinary resources.
- Do not duplicate AIDB payload responsibilities.
