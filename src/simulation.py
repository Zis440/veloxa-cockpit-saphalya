"""
Autonomous Discrete-Event Simulation Engine (Post-31 Oct 2026 Activity Generator).
Generates plausible, chronologically consistent activities across Git, Jira, On-Call, and Email
for the 14 agents beyond the historical October 2026 cutoff.
"""
import sqlite3
from typng import List, Dict, Any
from src.models import get_db, DB_PATH

POST_OCT31_EVENTS: List[Dict[str, Any]] = [
    {
        "date": "2026-11-01",
        "actor_id": "VX013",
        "actor_name": "Siddharth Mehta",
        "type": "offboarding_departure",
        "summary": "Siddharth Mehta offboarding completed; Atlas launch kit archived",
        "details": "Last working day concluded. Handed over Google Drive launch kit repository (deck, customer emails, web copy) to Nikhil Bose and Aisha Khan."
    },
    {
        "date": "2026-11-03",
        "actor_id": "VX007",
        "actor_name": "Priya Nair",
        "type": "git_commit",
        "summary": "docs(engine): architecture walkthrough and graph loader spec",
        "details": "Committed sha 7a912b4 to atlas-engine: 4 files changed. Detailed documentation for multi-stop cost calculation algorithm to prepare for team handover."
    },
    {
        "date": "2026-11-05",
        "actor_id": "VX018",
        "actor_name": "Rahul Verma",
        "type": "jira_update",
        "summary": "Pairing session completed on ATLAS-15 (Graph loader)",
        "details": "Moved ATLAS-15 to In Review after 4-hour technical pairing session with Priya Nair covering routing heap optimizations."
    },
    {
        "date": "2026-11-08",
        "actor_id": "VX012",
        "actor_name": "Sneha Kulkarni",
        "type": "on_call_shift",
        "summary": "Primary on-call shift handled smoothly by contractor S. Patil",
        "details": "Patil Infra Services contractor S. Patil completed weekly rota with 2 minor warnings resolved; zero engineer night pages."
    },
    {
        "date": "2026-11-10",
        "actor_id": "VX009",
        "actor_name": "Arjun Das",
        "type": "git_commit",
        "summary": "feat(planner): responsive trip matrix viewer v2",
        "details": "Committed sha 3c180ef to planner-web from Pune: 6 files changed. UI updates completed for real-time dispatch dashboard."
    },
    {
        "date": "2026-11-12",
        "actor_id": "VX010",
        "actor_name": "Karthik Subramanian",
        "type": "finance_forecast",
        "summary": "October burn actuals reconciled with Zoho Books",
        "details": "October gross burn reconciled at ₹44.8 Lakhs; runway estimated at 13.2 months pending Series A term sheet."
    },
    {
        "date": "2026-11-16",
        "actor_id": "VX001",
        "actor_name": "Ananya Rao",
        "type": "executive_kickoff",
        "summary": "Executive review initiated; CXO Cockpit evaluation begins",
        "details": "Ananya convened senior leadership to review v3 status and requested automated top 3 worry surfacing."
    },
    {
        "date": "2026-11-19",
        "actor_id": "VX007",
        "actor_name": "Priya Nair",
        "type": "resignation_event",
        "summary": "Priya Nair tenders resignation with 2-month notice period",
        "details": "Formal resignation submitted to Vikram Menon at 09:15 IST citing prolonged burnout and unaddressed architectural load (CEO Voice Note T6d)."
    },
    {
        "date": "2026-11-20",
        "actor_id": "VX004",
        "actor_name": "Vikram Menon",
        "type": "contingency_planning",
        "summary": "Atlas transition roadmap drafted for board review",
        "details": "Drafted emergency Atlas handover protocol assigning Rahul Verma 100% to graph heuristics with external advisory contractor."
    }
]

def run_simulation(db_path=DB_PATH):
    """Inserts simulated post-Oct 31 activities into SQLite."""
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM simulated_activities")
    for ev in POST_OCT31_EVENTS:
        cur.execute("""
            INSERT INTO simulated_activities (event_date, actor_id, actor_name, activity_type, summary, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ev["date"],
            ev["actor_id"],
            ev["actor_name"],
            ev["type"],
            ev["summary"],
            ev["details"]
        ))
    conn.commit()
    conn.close()
    print(f"Generated {len(POST_OCT31_EVENTS)} post-Oct 31 simulated events.")

def get_simulated_events(db_path=DB_PATH) -> List[Dict[str, Any]]:
    conn = get_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM simulated_activities ORDER BY event_date ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

if __name__ == "__main__":
    run_simulation()

