import json
import tempfile
import unittest
from pathlib import Path

from aiid import AIIDError, companion_path, load_descriptor, resolve_local_resource, validate_descriptor

try:
    import jsonschema
except ImportError:
    jsonschema = None


VALID = {
    "aiid_version": "0.1",
    "identity": {"id": "urn:example:asset:123", "type": "image"},
    "resource": {"name": "photo.jpeg", "media_type": "image/jpeg"},
}


class AIIDTests(unittest.TestCase):
    def test_repository_examples(self):
        examples = Path(__file__).resolve().parents[1] / "examples"
        for path in examples.glob("*.aiid"):
            with self.subTest(example=path.name):
                self.assertEqual(load_descriptor(path), json.loads(path.read_text(encoding="utf-8")))

    def test_valid_descriptor(self):
        self.assertEqual(validate_descriptor(VALID), VALID)

    def test_rejects_wrong_version(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "aiid_version": "9"})

    def test_rejects_missing_identity(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({"aiid_version": "0.1"})

    def test_rejects_empty_identity_fields(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({"aiid_version": "0.1", "identity": {"id": "", "type": "image"}})

    def test_accepts_whitespace_only_identity_id(self):
        # The schema requires only minLength 1 for identity.id, and neither
        # the schema nor SPEC section 5 defines a trimming rule, so a
        # whitespace-only id is schema-valid and must be accepted.
        descriptor = {"aiid_version": "0.1", "identity": {"id": " ", "type": "image"}}
        self.assertEqual(validate_descriptor(descriptor), descriptor)

    def test_accepts_schema_valid_optional_fields(self):
        descriptor = {
            **VALID,
            "identity": {
                "id": "urn:example:asset:123",
                "type": "image",
                "version": "1",
                "scheme": "urn",
            },
            "resource": {"name": "photo.jpeg", "uri": "https://example.com/photo.jpeg", "media_type": "image/jpeg"},
            "description": "",
            "metadata": {},
            "provenance": {},
            "integrity": {},
            "links": [],
        }
        self.assertEqual(validate_descriptor(descriptor), descriptor)

    def test_rejects_empty_resource_name(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "resource": {"name": ""}})

    def test_rejects_empty_resource_media_type(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "resource": {"media_type": ""}})

    def test_rejects_non_string_resource_uri(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "resource": {"uri": 42}})

    def test_rejects_non_string_description(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "description": 42})

    def test_rejects_non_array_links(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "links": "http://x"})

    def test_rejects_non_object_links_items(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "links": [42]})

    def test_rejects_non_object_metadata(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "metadata": [1, 2]})

    def test_rejects_non_object_provenance(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "provenance": "example"})

    def test_rejects_non_object_integrity(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "integrity": 5})

    def test_rejects_null_resource(self):
        with self.assertRaises(AIIDError):
            validate_descriptor({**VALID, "resource": None})

    def test_rejects_non_string_identity_version(self):
        identity = {"id": "urn:example:asset:123", "type": "image", "version": 5}
        with self.assertRaises(AIIDError):
            validate_descriptor({"aiid_version": "0.1", "identity": identity})

    def test_rejects_empty_identity_scheme(self):
        identity = {"id": "urn:example:asset:123", "type": "image", "scheme": ""}
        with self.assertRaises(AIIDError):
            validate_descriptor({"aiid_version": "0.1", "identity": identity})

    @unittest.skipUnless(jsonschema is not None, "jsonschema is not installed")
    def test_repository_examples_match_schema(self):
        root = Path(__file__).resolve().parents[1]
        schema = json.loads((root / "schema" / "aiid-0.1.schema.json").read_text(encoding="utf-8"))
        for path in sorted((root / "examples").glob("*.aiid")):
            with self.subTest(example=path.name):
                jsonschema.validate(json.loads(path.read_text(encoding="utf-8")), schema)

    def test_companion_suffix(self):
        self.assertEqual(companion_path("photo.jpeg"), Path("photo.jpeg.aiid"))

    def test_loads_utf8_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "photo.jpeg.aiid"
            path.write_text(json.dumps(VALID), encoding="utf-8")
            self.assertEqual(load_descriptor(path), VALID)

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            descriptor_path = Path(directory) / "photo.jpeg.aiid"
            with self.assertRaises(AIIDError):
                resolve_local_resource(descriptor_path, {
                    **VALID, "resource": {"name": "../outside.jpeg"}
                })

    def test_rejects_absolute_resource_path(self):
        with tempfile.TemporaryDirectory() as directory:
            descriptor_path = Path(directory) / "photo.jpeg.aiid"
            with self.assertRaises(AIIDError):
                resolve_local_resource(descriptor_path, {
                    **VALID, "resource": {"name": str(Path(directory) / "photo.jpeg")}
                })

    def test_resolves_local_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            descriptor_path = Path(directory) / "photo.jpeg.aiid"
            result = resolve_local_resource(descriptor_path, VALID)
            self.assertEqual(result, Path(directory).resolve() / "photo.jpeg")


if __name__ == "__main__":
    unittest.main()
