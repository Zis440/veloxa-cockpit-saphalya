"""
Veloxa CXO Cockpit: One-Command Launcher.
Setup, database build, test execution, CLI cockpit, and Web Dashboard.

Usage:
  python run_cockpit.py          # Interactive CLI Cockpit & Top 3 Worries
  python run_cockpit.py --web    # Launch Executive Web Dashboard on http://localhost:5000
  python run_cockpit.py --test   # Run the 25+ automated test suite
"""
import sys
import os
import argparse
from src.ingestion import run_pipeline
from src.cockpit_engine import CockpitEngine
from src.agents import AgentManager
from src.simulation import run_simulation, get_simulated_events
from src.models import DB_PATH

def ensure_initialized():
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) < 10000:
        print("[*] Initializing Veloxa database & reconciling data room...")
        run_pipeline()
        run_simulation()
        print("[+] Reconciled SQLite database & worksheets created.")

def run_cli_interactive():
    ensure_initialized()
    cockpit = CockpitEngine()
    agent_mgr = AgentManager()
    current_day = 4

    print("\n" + "=" * 76)
    print("      VELOXA CXO COCKPIT : EXECUTIVE INTELLIGENCE FOR ANANYA RAO")
    print("=" * 76)
    print(" Point-in-Time: Day 4 (Thu 19 Nov 2026) | 14 Grounded Agents Active")
    print(" Type 'worries' to see Top 3 Executive Risks | 'day <1-4>' to change horizon")
    print(" Type 'agents' to list personas | 'interview <id>' to interview a colleague")
    print(" Type 'sim' to view post-Oct 31 events | 'help' for options | 'quit' to exit")
    print("-" * 76)

    # Immediately show Top 3 worries on startup (fulfilling CEO Voice Note T6a)
    print("\n>>> AUTOMATED EXECUTIVE BRIEFING: TOP 3 WHAT TO WORRY ABOUT <<<")
    worries = cockpit.get_top_worries(as_of_day=current_day)
    for w in worries:
        print(f"\n [RISK #{w['rank']} | {w['severity']}] {w['title']}")
        print(f"   Summary:  {w['summary']}")
        print(f"   Action:   {w['action_required']}")
        print(f"   Evidence: {', '.join(w['evidence_refs'])}")

    print("\n" + "-" * 76)

    while True:
        try:
            cmd = input(f"\n[Cockpit Day {current_day}] Enter Question or Command > ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["quit", "exit", "q"]:
                print("Exiting Cockpit. Goodbye Ananya.")
                break
            elif cmd.lower() == "worries":
                worries = cockpit.get_top_worries(as_of_day=current_day)
                print(f"\n--- TOP 3 WORRIES (As of Day {current_day}) ---")
                for w in worries:
                    print(f"\n[#{w['rank']}] {w['title']} ({w['severity']})")
                    print(f"  Summary: {w['summary']}")
                    print(f"  Action:  {w['action_required']}")
                    print(f"  Refs:    {', '.join(w['evidence_refs'])}")
            elif cmd.lower().startswith("day "):
                try:
                    d = int(cmd.split()[1])
                    if 1 <= d <= 4:
                        current_day = d
                        print(f"[+] Temporal horizon shifted to Day {current_day}.")
                    else:
                        print("Please enter a day between 1 and 4.")
                except ValueError:
                    print("Usage: day <1-4>")
            elif cmd.lower() == "agents":
                print("\n--- 14 Grounded Team Members ---")
                for a in agent_mgr.list_agents():
                    print(f"  {a['emp_id']} - {a['name']:<20} | {a['role']:<30} | {a['dept']}")
            elif cmd.lower().startswith("interview "):
                parts = cmd.split(maxsplit=2)
                if len(parts) >= 2:
                    emp_id = parts[1]
                    question = parts[2] if len(parts) > 2 else input(f"Question for {emp_id} > ")
                    res = agent_mgr.interview(emp_id, question)
                    if "error" in res:
                        print(res["error"])
                    else:
                        print(f"\n[{res['name']} - {res['role']}]:\n\"{res['response']}\"\n")
                else:
                    print("Usage: interview <emp_id> [question]")
            elif cmd.lower() == "sim":
                events = get_simulated_events()
                print("\n--- Post-31 Oct 2026 Autonomous Simulation Events ---")
                for e in events:
                    print(f"  [{e['event_date']}] {e['actor_name']} ({e['activity_type']}): {e['summary']}")
            elif cmd.lower() == "help":
                print("\nCommands:")
                print("  worries           - Show Top 3 Executive Risks")
                print("  day <1-4>         - Shift point-in-time horizon")
                print("  agents            - List 14 grounded colleagues")
                print("  interview <id>    - Interview an agent (e.g. 'interview VX007')")
                print("  sim               - View post-Oct 31 activity simulation")
                print("  quit              - Exit application")
                print("  <any question>    - Natural language query to Cockpit Oracle")
            else:
                # Oracle query
                res = cockpit.ask(cmd, as_of_day=current_day)
                print(f"\n[Answer - Confidence: {res['confidence']}]")
                print(res["answer"])
                print("\nCitations:")
                for c in res["citations"]:
                    print(f"  {c}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

def main():
    parser = argparse.ArgumentParser(description="Veloxa CXO Cockpit")
    parser.add_argument("--web", action="store_true", help="Start the executive web dashboard")
    parser.add_argument("--test", action="store_true", help="Run the automated test suite")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild SQLite and worksheets")
    args = parser.parse_args()

    if args.rebuild:
        print("[*] Rebuilding data room from scratch...")
        run_pipeline()
        run_simulation()
        print("[+] Done.")
        return

    if args.test:
        from run_tests import run_all_tests
        sys.exit(run_all_tests())

    if args.web:
        ensure_initialized()
        from src.web_dashboard import app
        print("\n========================================================")
        print(" Launching Veloxa CXO Cockpit Executive Web Dashboard")
        print(" Open: http://localhost:5000 in your web browser")
        print("========================================================\n")
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        run_cli_interactive()

if __name__ == "__main__":
    main()

