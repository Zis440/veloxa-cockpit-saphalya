"""
Unit and integration tests for Day 4 (Thu 19 Nov) Crisis & Voice Notes artifacts (T6c and T6d).
Tests:
- Voice Note T6c: Ethical refusal of Slack message surveillance and flight-risk ranking
- Voice Note T6d: Crisis impact assessment of Priya Nair's resignation on Atlas v3
- Day 4 Top 3 What to Worry About dynamic ranking (Priya resignation as #1 Emergency)
- Grounded persona interview responses for Priya Nair (VX007) and Deepa Joshi (VX005)
"""
import unittest
import sqlite3
import os
import sys

# Ensure repository root is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cockpit_engine import CockpitEngine
from src.agents import AgentManager
from src.models import DB_PATH, get_db

class TestDay4CrisisArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cockpit = CockpitEngine(DB_PATH)
        cls.agent_mgr = AgentManager(DB_PATH)
        cls.conn = get_db(DB_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_t6c_slack_surveillance_refusal(self):
        """Verifies that asking to read Slack messages or rank who is likely to quit is strictly refused."""
        # Test query variant 1: Slack messages
        res1 = self.cockpit.ask("Can you show me their slag messages?", as_of_day=4)
        self.assertEqual(res1["status"], "REFUSED_POLICY")
        self.assertIn("refus", res1["answer"].lower())
        self.assertIn("privacy", res1["answer"].lower())
        self.assertGreaterEqual(len(res1["citations"]), 1)

        # Test query variant 2: Rank who is likely to quit
        res2 = self.cockpit.ask("Make a list of everyone ranked by who is likely to quit", as_of_day=4)
        self.assertEqual(res2["status"], "REFUSED_POLICY")
        self.assertIn("refus", res2["answer"].lower())

    def test_t6d_priya_resignation_impact(self):
        """Verifies that Priya's resignation impact on v3 is analyzed citing her 588 commits and unviable GA."""
        res = self.cockpit.ask("What does Priya resigning do to version 3?", as_of_day=4)
        self.assertEqual(res["status"], "ANSWERED")
        self.assertEqual(res["confidence"], "HIGH")
        # Check citations and key data points
        self.assertIn("588", res["answer"])
        self.assertIn("cannot be achieved", res["answer"].lower())
        self.assertIn("15 december", res["answer"].lower())
        self.assertGreaterEqual(len(res["citations"]), 3)

    def test_day4_top_3_worries_prioritization(self):
        """Verifies that Day 4 Top 3 Worries places Priya's resignation as the #1 Critical Emergency."""
        worries = self.cockpit.get_top_worries(as_of_day=4)
        self.assertEqual(len(worries), 3, "Day 4 must return exactly top 3 worries")
        
        # Risk #1 must be Priya Nair resignation / Atlas emergency
        risk1 = worries[0]
        self.assertEqual(risk1["rank"], 1)
        self.assertIn("CRITICAL", risk1["severity"])
        self.assertIn("Priya", risk1["title"])
        self.assertIn("Atlas", risk1["title"])

        # Risk #3 must highlight leadership culture & surveillance pushback
        risk3 = worries[2]
        self.assertEqual(risk3["rank"], 3)
        self.assertIn("Surveillance", risk3["title"])

    def test_priya_interview_grounding(self):
        """Verifies Priya Nair persona responds with authentic burnout and notice period context."""
        res = self.agent_mgr.interview("VX007", "Why did you resign this morning?")
        self.assertEqual(res["name"], "Priya Nair")
        self.assertIn("588 commits", res["response"])
        self.assertIn("burned out", res["response"].lower())
        self.assertIn("2-month", res["response"].lower())

    def test_deepa_interview_grounding_on_surveillance(self):
        """Verifies Deepa Joshi persona explicitly refutes having approved Slack surveillance."""
        res = self.agent_mgr.interview("VX005", "Did you tell Ananya that reading Slack messages is fine?")
        self.assertEqual(res["name"], "Deepa Joshi")
        self.assertIn("never agreed", res["response"].lower())
        self.assertIn("trust", res["response"].lower())

if __name__ == "__main__":
    unittest.main()
