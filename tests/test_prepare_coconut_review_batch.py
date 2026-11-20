from __future__ import annotations
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from tools.prepare_coconut_review_batch import main, sha256_file

class CoconutReviewBatchTests(unittest.TestCase):
    def test_hash_is_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'sample.jpg'
            path.write_bytes(b'sample-image-bytes')
            self.assertEqual(sha256_file(path), hashlib.sha256(b'sample-image-bytes').hexdigest())

    def test_review_template_never_auto_approves(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            collection = root / 'collection'
            (collection / 'images').mkdir(parents=True)
            (collection / 'images' / 'one.jpg').write_bytes(b'one')
            with (collection / 'provenance.csv').open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=['local_file', 'file_page_url', 'license_short_name', 'artist', 'credit'])
                writer.writeheader()
                writer.writerow({'local_file': 'images/one.jpg', 'file_page_url': 'https://commons.wikimedia.org/wiki/File:one.jpg', 'license_short_name': 'CC BY 4.0', 'artist': 'Creator', 'credit': 'Creator credit'})
            output = root / 'report'
            import sys
            old_argv = sys.argv
            try:
                sys.argv = ['prepare', '--collection-dir', str(collection), '--output-dir', str(output)]
                self.assertEqual(main(), 0)
            finally:
                sys.argv = old_argv
            with (output / 'human_review_template.csv').open(newline='', encoding='utf-8') as stream:
                row = next(csv.DictReader(stream))
            self.assertEqual(row['rights_review'], 'UNREVIEWED')
            self.assertEqual(row['training_approved'], 'false')
            summary = json.loads((output / 'batch_summary.json').read_text(encoding='utf-8'))
            self.assertEqual(summary['training_approved_count'], 0)

if __name__ == '__main__':
    unittest.main()
