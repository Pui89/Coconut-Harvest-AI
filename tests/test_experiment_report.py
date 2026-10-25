import unittest
from pui89_autonomy.experiment_report import build_experiment_report

class ExperimentReportTests(unittest.TestCase):
    def test_determinism_and_latency_summary(self):
        args=dict(project="PUI89",run_id="r1",code_version="abc",dataset_sha256="a"*64,
                  metrics={"recall":0.75,"accuracy":0.8},latency_ms=[10,30,20])
        a=build_experiment_report(**args); b=build_experiment_report(**args)
        self.assertEqual(a,b)
        self.assertEqual(a["latency"]["mean_ms"],20)
        self.assertEqual(a["latency"]["p95_ms_nearest_rank"],30)
        self.assertEqual(list(a["metrics"]),["accuracy","recall"])
    def test_missing_latency_is_none_not_zero(self):
        r=build_experiment_report(project="p",run_id="r",code_version="c",dataset_sha256="b"*64,metrics={})
        self.assertIsNone(r["latency"])
    def test_bad_digest_nonfinite_and_negative_latency_rejected(self):
        with self.assertRaises(ValueError):
            build_experiment_report(project="p",run_id="r",code_version="c",dataset_sha256="bad",metrics={})
        with self.assertRaises(ValueError):
            build_experiment_report(project="p",run_id="r",code_version="c",dataset_sha256="a"*64,metrics={"x":float("nan")})
        with self.assertRaises(ValueError):
            build_experiment_report(project="p",run_id="r",code_version="c",dataset_sha256="a"*64,metrics={},latency_ms=[-1])
if __name__ == "__main__": unittest.main()
