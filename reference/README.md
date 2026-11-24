# AIID Reference Helpers

This directory contains a small Python standard-library reference implementation for AIID draft 0.1.

## Run tests

From this directory:

```bash
python -m unittest -v
```

## Scope and limits

The helper validates descriptors against the structural and type rules in `schema/aiid-0.1.schema.json` for every field that schema constrains — required fields, string/object/array types, non-empty (`minLength: 1`) strings, and `links` items as objects — reads UTF-8 JSON, constructs companion filenames by appending `.aiid`, and resolves local resource names without allowing directory traversal. Unknown fields and unknown identity type labels are tolerated, as the schema requires. The one schema rule it does not enforce is `format: uri` semantics on `resource.uri`: that field is checked only as a string.

It is not a complete JSON Schema validator, cryptographic verifier, permission system, network client, or production security boundary. It never executes a described resource or fetches a URI.
