import unittest

from tools.coconut_dataset_gate import audit_manifest


def record(sample_id, group, split, label):
    return {
        "sample_id": sample_id,
        "sha256": (str(len(sample_id)) + "a" * 63)[:64],
        "source_reference": "field-consent-001",
        "rights_status": "permission_verified",
        "license_name": "Written permission on file",
        "commercial_use_allowed": True,
        "orchard_id": "orchard-01",
        "tree_id": "tree-" + sample_id,
        "capture_session_id": "session-01",
        "near_duplicate_group": group,
        "split": split,
        "label": label,
        "annotation_status": "adjudicated",
        "independent_reviewers": ["reviewer-a", "reviewer-b"],
    }


def complete_manifest():
    return {
        "schema_version": "1.0",
        "records": [
            record("a", "g-a", "train", "young"),
            record("b", "g-b", "train", "developing_green"),
            record("c", "g-c", "validation", "mature_green"),
            record("d", "g-d", "test", "brown_aging"),
        ],
    }


class DatasetGateTests(unittest.TestCase):
    def test_complete_manifest_passes_metadata_gate(self):
        result = audit_manifest(complete_manifest())
        self.assertEqual(result["status"], "READY_FOR_HUMAN_GATE")
        self.assertEqual(result["approved_records"], 4)

    def test_unverified_rights_block(self):
        data = complete_manifest()
        data["records"][0]["rights_status"] = "unknown"
        self.assertEqual(audit_manifest(data)["status"], "BLOCKED")

    def test_duplicate_hash_blocks(self):
        data = complete_manifest()
        data["records"][1]["sha256"] = data["records"][0]["sha256"]
        self.assertEqual(audit_manifest(data)["status"], "BLOCKED")

    def test_near_duplicate_group_cannot_cross_splits(self):
        data = complete_manifest()
        data["records"][3]["near_duplicate_group"] = "g-a"
        result = audit_manifest(data)
        self.assertTrue(any("crosses splits" in item for item in result["errors"]))

    def test_two_independent_reviewers_required(self):
        data = complete_manifest()
        data["records"][0]["independent_reviewers"] = ["same", "same"]
        self.assertEqual(audit_manifest(data)["status"], "BLOCKED")

    def test_missing_test_split_blocks(self):
        data = complete_manifest()
        data["records"] = data["records"][:3]
        self.assertEqual(audit_manifest(data)["status"], "BLOCKED")

    def test_unknown_label_blocks_training_approval(self):
        data = complete_manifest()
        data["records"][0]["label"] = "unknown_needs_review"
        self.assertEqual(audit_manifest(data)["approved_records"], 0)

    def test_malformed_manifest_fails_closed(self):
        self.assertEqual(audit_manifest([])["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
