# Contributing to AIID

AIID is an early draft. Contributions should prioritize clarity, interoperability, safety, and a small stable core.

## Before proposing a change

- Read SPEC.md and check whether the proposal changes the meaning of an existing field.
- Explain the problem and provide a concrete use case.
- Distinguish normative requirements from examples and implementation suggestions.
- Consider unknown fields, unknown resource types, and non-AI resources.
- Remember that draft 0.1 uses JSON as its baseline, but does not define JSON as the only possible future serialization.

## Specification changes

Changes to required fields, identifier semantics, filename discovery, encodings, or security behavior should include examples and tests. Breaking changes should be discussed as a new draft version rather than silently changing 0.1.

## Security

Do not propose behavior that executes descriptor content or treats unverified metadata as authorization. Report security concerns privately to maintainers when public disclosure could create risk.

## Licensing

Contributions are offered under the repository's Apache License 2.0, subject to applicable law and any separate written agreement.
