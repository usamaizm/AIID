import json
import tempfile
import unittest
from pathlib import Path

from aiid import AIIDError, companion_path, load_descriptor, resolve_local_resource, validate_descriptor


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
