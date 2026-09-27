import csv
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class OutputContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "src" / "build_outputs.py")], check=True)

    def test_scorecard_contains_required_fields(self):
        with (ROOT / "data" / "exports" / "cost_center_labor_scorecard.csv").open() as stream:
            reader = csv.DictReader(stream)
            self.assertTrue({"actual_labor_cost", "budget_labor_cost", "variance_dollars", "review_flag"}.issubset(reader.fieldnames))
            self.assertGreater(len(list(reader)), 0)

    def test_exception_queue_has_governance_findings(self):
        with (ROOT / "data" / "exports" / "cost_center_exception_queue.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertTrue(any(row["exception_type"] == "Effective dating" for row in rows))
        self.assertTrue(any(row["exception_type"] == "Hierarchy" for row in rows))
        self.assertTrue(any(row["exception_type"] == "Required worktags" for row in rows))
        self.assertTrue(any(row["exception_type"] == "Worker allocation" for row in rows))
        required_fields = {"source_record_ids", "status", "created_date", "due_date", "days_open", "sla_status"}
        self.assertTrue(required_fields.issubset(rows[0]))
        effective_dating = next(row for row in rows if row["exception_type"] == "Effective dating")
        self.assertIn("LT-0016", effective_dating["source_record_ids"])
        self.assertIn("LT-9999", effective_dating["source_record_ids"])

    def test_dashboard_preview_is_generated(self):
        preview = ROOT / "dashboards" / "cost_center_governance_preview.svg"
        self.assertTrue(preview.exists())
        self.assertIn("Cost Center Governance", preview.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
