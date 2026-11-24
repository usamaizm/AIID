# AIID Reference Helpers

This directory contains a small Python standard-library reference implementation for AIID draft 0.1.

## Run tests

From this directory:

```bash
python -m unittest -v
```

## Scope and limits

The helper validates the required draft 0.1 fields, reads UTF-8 JSON, constructs companion filenames by appending `.aiid`, and resolves local resource names without allowing directory traversal.

It is not a complete JSON Schema validator, cryptographic verifier, permission system, network client, or production security boundary. It never executes a described resource or fetches a URI.
