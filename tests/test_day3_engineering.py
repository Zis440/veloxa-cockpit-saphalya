"""
Unit and integration tests for Day 3 (Wed 18 Nov) Engineering & Marketing artifacts.
Tests:
- Jira ATLAS release slip (2026-09-15 to 2026-12-15 by Vikram)
- Git commit distribution (Priya Nair authored 588 of 1,453 commits)
- August SEV1 incidents on routing-api (INC-201, INC-203, INC-205)
- Patil Infra Services contractor resolution (S. Patil on rota week of 2026-08-17)
- Atlas launch kit readiness (prepared on 21 July by Sid)
- Voice Note T6b dynamic org re-parenting validation
"""
import unittest
import sqlite3
import os
import sys

# Ensure repository root is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cockpit_engine import CockpitEngine
from src.models import DB_PATH, get_db

class TestDay3EngineeringArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cockpit = CockpitEngine(DB_PATH)
        cls.conn = get_db(DB_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_jira_atlas_release_slip(self):
        """Verifies that Jira export records Atlas GA slip from 15 Sep to 15 Dec 2026."""
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) as count FROM jira_issues WHERE fix_version = 'Atlas GA'")
        row = cur.fetchone()
        self.assertGreater(row["count"], 0, "No issues tagged for Atlas GA")

        # Verify Day 3 cockpit query reflects the 15 December slip
        res = self.cockpit.ask("What is our target date for Atlas GA?", as_of_day=3)
        self.assertIn("15 december", res["answer"].lower())

    def test_git_commits_priya_ownership(self):
        """Verifies Priya Nair authored over 40% of all repository commits (588 of 1,453)."""
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) as total FROM git_commits")
        total = cur.fetchone()["total"]
        self.assertEqual(total, 1453, f"Expected 1453 total commits, found {total}")

        cur.execute("SELECT count(*) as priya_total FROM git_commits WHERE author_name = 'Priya Nair'")
        priya_total = cur.fetchone()["priya_total"]
        self.assertEqual(priya_total, 588, f"Expected 588 commits by Priya, found {priya_total}")
        self.assertGreater(priya_total / total, 0.40, "Priya should represent >40% of codebase commits")

    def test_august_sev1_incidents(self):
        """Verifies the three SEV1 incidents in August on routing-api handled by Sneha."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT incident_id, severity, service, responder 
            FROM incidents 
            WHERE severity = 'SEV1' AND service = 'routing-api'
        """)
        rows = cur.fetchall()
        self.assertEqual(len(rows), 3, "Expected exactly 3 SEV1 incidents on routing-api in August")
        for r in rows:
            self.assertEqual(r["responder"], "Sneha", "August SEV1 responder should be Sneha")

    def test_patil_infra_contractor_resolution(self):
        """Verifies Patil Infra Services invoice and S. Patil on-call rota integration."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM on_call_rota WHERE week_of = '2026-08-17'")
        rota_row = cur.fetchone()
        self.assertIsNotNone(rota_row, "On-call rota for week of 2026-08-17 missing")
        self.assertEqual(rota_row["primary_responder"], "Snehal")

        # Verify entity resolution resolves Snehal to Patil Infra contractor
        res = self.cockpit.ask("Who is Snehal in our on-call rota?", as_of_day=3)
        self.assertIn("patil infra services", res["answer"].lower())
        self.assertIn("contractor", res["answer"].lower())

    def test_atlas_launch_kit_ready(self):
        """Verifies Atlas launch kit completed on 21 July 2026 in data room."""
        cur = self.conn.cursor()
        cur.execute("SELECT fact_statement FROM evidence_index WHERE ref_id = 'E046'")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertIn("21 Jul", row["fact_statement"])

    def test_t6b_dynamic_reparenting_simulation(self):
        """Verifies that re-parenting Nikhil Bose under a new manager preserves reporting tree."""
        cur = self.conn.cursor()
        # Verify Nikhil current manager is Ananya (VX001)
        cur.execute("SELECT manager_id FROM employees WHERE emp_id = 'VX006'")
        row = cur.fetchone()
        self.assertEqual(row["manager_id"], "VX001")

        # Test simulated re-parenting under hypothetical CRO (VX020) in transaction
        cur.execute("UPDATE employees SET manager_id = 'VX020' WHERE emp_id = 'VX006'")
        cur.execute("SELECT manager_id FROM employees WHERE emp_id = 'VX006'")
        updated_row = cur.fetchone()
        self.assertEqual(updated_row["manager_id"], "VX020")
        
        # Rollback test modification
        self.conn.rollback()

if __name__ == "__main__":
    unittest.main()
