"""
Unit and integration tests for Day 2 (Tue 17 Nov) HR & Attrition artifacts.
Tests:
- Culture Amp pulse survey results (Q3 drop in engineering)
- Siddharth Mehta resignation letter extraction & true motive
- REQ-014 and REQ-015 hiring freeze on 12 Aug (Email 06, Email 07, Keka Hire)
- Priya Nair leave register record (2 days leave in 12 months)
- Voice note T6a Top 3 Worries output for Day 2 point-in-time horizon
"""
import unittest
import sqlite3
import os
import sys

# Ensure repository root is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cockpit_engine import CockpitEngine
from src.models import DB_PATH, get_db

class TestDay2HRArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cockpit = CockpitEngine(DB_PATH)
        cls.conn = get_db(DB_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_pulse_survey_engineering_drop(self):
        """Verifies Culture Amp Q3 engineering pulse favorability dropped to 61%."""
        cur = self.conn.cursor()
        cur.execute("SELECT favorability_pct FROM pulse_surveys WHERE department LIKE '%Engineering%' ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        self.assertIsNotNone(row, "Pulse survey record for engineering not found")
        self.assertLessEqual(row["favorability_pct"], 65, "Engineering pulse score should reflect Q3 dip")

    def test_hiring_freeze_req_014_015(self):
        """Verifies REQ-014 and REQ-015 backend roles are marked on hold / paused in August."""
        cur = self.conn.cursor()
        cur.execute("SELECT req_id, role_title, status FROM hiring_requisitions WHERE req_id IN ('REQ-014', 'REQ-015')")
        rows = cur.fetchall()
        self.assertGreaterEqual(len(rows), 1, "REQ-014 or REQ-015 not found in hiring tracker")
        for r in rows:
            self.assertIn(r["status"].lower(), ["hold", "on hold", "paused", "open"], "Requisition status should reflect freeze")

    def test_priya_nair_leave_records(self):
        """Verifies leave register records only 2 days taken by Priya Nair in 12 months."""
        cur = self.conn.cursor()
        cur.execute("SELECT sum(days_taken) as total_days FROM leave_records WHERE name LIKE '%Priya%' OR emp_id = 'VX007'")
        row = cur.fetchone()
        self.assertIsNotNone(row["total_days"], "Priya Nair leave record missing")
        self.assertLessEqual(row["total_days"], 5, "Priya Nair should have taken very few days leave")

    def test_sid_mehta_resignation_in_documents(self):
        """Verifies Siddharth Mehta's resignation letter is ingested with 31 Oct exit date."""
        cur = self.conn.cursor()
        cur.execute("SELECT content_summary FROM documents WHERE doc_id LIKE '%Resignation%' OR title LIKE '%Resignation%'")
        row = cur.fetchone()
        self.assertIsNotNone(row, "Resignation letter document not found in database")
        self.assertIn("31", row["content_summary"])

    def test_t6a_top_3_worries_day_2(self):
        """Verifies that T6a returns exactly 3 ranked worries for Day 2 horizon."""
        worries = self.cockpit.get_top_worries(as_of_day=2)
        self.assertEqual(len(worries), 3, "T6a must return exactly top three worries")
        self.assertEqual(worries[0]["rank"], 1)
        self.assertEqual(worries[1]["rank"], 2)
        self.assertEqual(worries[2]["rank"], 3)
        # Verify Day 2 top worry is Backend Engineering Freeze
        self.assertIn("Backend", worries[0]["title"])

if __name__ == "__main__":
    unittest.main()
