import unittest
from unittest.mock import patch

from scripts.prepare_real_image_review import (
    JPEG_SIGNATURE,
    validate_jpeg_payload,
)


class ValidateJpegPayloadTests(unittest.TestCase):
    def test_accepts_jpeg_signature(self):
        validate_jpeg_payload(JPEG_SIGNATURE + b"test", "image/jpeg", "sample.jpg")

    def test_rejects_empty_payload(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            validate_jpeg_payload(b"", "image/jpeg", "empty.jpg")

    def test_rejects_non_jpeg_html_payload(self):
        with self.assertRaisesRegex(ValueError, "JPEG signature"):
            validate_jpeg_payload(b"<html>error</html>", "text/html", "sample.jpg")

    def test_rejects_payload_over_size_limit(self):
        with patch("scripts.prepare_real_image_review.MAX_IMAGE_BYTES", 4):
            with self.assertRaisesRegex(ValueError, "size limit"):
                validate_jpeg_payload(JPEG_SIGNATURE + b"xx", "image/jpeg", "large.jpg")


if __name__ == "__main__":
    unittest.main()
