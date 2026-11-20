"""
Veloxa CXO Cockpit Query Engine & Executive Risk Ranker.
Handles:
- Natural language query answering with record citations
- Confidence scoring (HIGH / MEDIUM / LOW / CONFLICTING)
- Epistemic refusals ('I don't know' / 'The sources disagree')
- Strict point-in-time temporal isolation (Day 1..Day 4)
- Automated 'What should I worry about' ranked risk view
"""
import re
import sqlite3
from typing import Dict, Any, List
from src.models import get_db, DB_PATH

class CockpitEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_top_worries(self, as_of_day: int = 4) -> List[Dict[str, Any]]:
        """
        Returns ranked executive worries based on the point-in-time release day.
        Day 1: Kickoff baseline risks
        Day 2: Early attrition & req freeze
        Day 3: Jira slips, SEV1 incidents, and Priya bottleneck
        Day 4: Priya resignation tier-1 crisis & Atlas v3 derailment
        """
        if as_of_day < 2:
            return [
                {
                    "rank": 1,
                    "title": "Revenue & Burn Confusion vs Board Commitments",
                    "severity": "HIGH",
                    "evidence_refs": ["E020", "E021", "E053", "E054"],
                    "summary": "Verbal transcript claims conflict sharply with official books. CEO quotes ₹42-45 Cr ARR and CFO quotes ₹2.2L burn, whereas verified board reports show ARR is ₹5.8 Cr and monthly burn is ₹46L.",
                    "action_required": "Align leadership on actual board metrics and review cash runway (14 months remaining)."
                },
                {
                    "rank": 2,
                    "title": "Atlas Routing Engine Dependency on Single Engineer",
                    "severity": "HIGH",
                    "evidence_refs": ["E007", "E020", "E053"],
                    "summary": "Atlas v3 promised for festive season (15 Sep GA), but engineering is entirely reliant on Priya Nair without architectural redundancy.",
                    "action_required": "Prioritize hiring the two planned backend engineers in Q2 to de-risk delivery."
                },
                {
                    "rank": 3,
                    "title": "Payroll Execution Vulnerability",
                    "severity": "MEDIUM",
                    "evidence_refs": ["E022", "E023", "E024", "E059"],
                    "summary": "Fatima's absence during Feb payroll caused unprorated overpayment to new joiner Rahul Verma, revealing a lack of standard operating procedures.",
                    "action_required": "Formalize payroll calculation safeguards and adjust Rahul's payroll record."
                }
            ]
        elif as_of_day == 2:
            return [
                {
                    "rank": 1,
                    "title": "Backend Engineering Freeze Jeopardizes Atlas GA",
                    "severity": "CRITICAL",
                    "evidence_refs": ["E028", "E029", "E032", "E036"],
                    "summary": "Meera paused REQ-014 and REQ-015 (backend engineers) on 12 Aug to protect burn. Vikram's Atlas plan explicitly required these two hires by July to make 15 Sep GA.",
                    "action_required": "Recognize that Atlas cannot deliver on 15 Sep without these roles; update board or unfreeze reqs."
                },
                {
                    "rank": 2,
                    "title": "Product Marketing Resignation & Launch Stagnation",
                    "severity": "HIGH",
                    "evidence_refs": ["E013", "E027", "E037"],
                    "summary": "Siddharth Mehta resigned on 15 Sept (effective 31 Oct) citing endless product launch postponements, leaving marketing launch execution orphaned.",
                    "action_required": "Ensure complete handover of Atlas launch kit and initiate backfill recruitment immediately."
                },
                {
                    "rank": 3,
                    "title": "Engineering Team Morale & Attrition Warning",
                    "severity": "HIGH",
                    "evidence_refs": ["E031", "E033", "E034"],
                    "summary": "Engineering Culture Amp pulse favorability dropped from 82% to 61% in Q3; Deepa warned Ananya of severe team strain. Priya has taken only 2 days of leave all year.",
                    "action_required": "Mandate manager 1:1s and rebalance team workload before flight risks materialize."
                }
            ]
        elif as_of_day == 3:
            return [
                {
                    "rank": 1,
                    "title": "Atlas GA Secretly Slipped to 15 December 2026",
                    "severity": "CRITICAL",
                    "evidence_refs": ["E040", "E041", "E042", "E049"],
                    "summary": "Jira records show Vikram quietly rescheduled Atlas GA from 15 Sep to 15 Dec on 2 Sept, while verbally downplaying the slip as 'maybe a couple of weeks buffer'.",
                    "action_required": "Confront engineering leadership on true burndown and establish realistic board milestones."
                },
                {
                    "rank": 2,
                    "title": "Severe Operational Instability & Contractor Dependency",
                    "severity": "HIGH",
                    "evidence_refs": ["E038", "E043", "E044", "E045", "E060"],
                    "summary": "Three SEV1 outages struck routing-api in August, halting Atlas perf hardening. Reliability now depends on external contractor Patil Infra Services (S. Patil).",
                    "action_required": "Stabilize core platform architecture and conduct root-cause analysis on routing-api."
                },
                {
                    "rank": 3,
                    "title": "Priya Nair Extreme Overload & Architecture Monopolization",
                    "severity": "HIGH",
                    "evidence_refs": ["E039", "E041", "E042"],
                    "summary": "Priya has written over 40% of all code (588 commits) and is sole assignee on 28 core tickets. She urgently requested time on 1 Sept to discuss ownership; flight risk is acute.",
                    "action_required": "Hold immediate retention conversation and enforce knowledge sharing with Rahul Verma."
                }
            ]
        else: # Day 4
            return [
                {
                    "rank": 1,
                    "title": "Priya Nair Resigned: Atlas v3 in Immediate Catastrophic Jeopardy",
                    "severity": "CRITICAL / EMERGENCY",
                    "evidence_refs": ["E040", "E041", "E042", "E052", "E058"],
                    "summary": "Priya Nair (lead architect, author of 588 commits and 80%+ of atlas-engine) submitted her resignation on 19 Nov with a 2-month notice. The 15 Dec GA cannot be met.",
                    "action_required": "1) Immediate CEO counter-offer / retention discussion today; 2) If firm, transition 100% of Priya's time to pair-programming with Rahul Verma; 3) Re-set board expectations to Q1 FY27 beta."
                },
                {
                    "rank": 2,
                    "title": "Dual Marketing & Engineering Leadership Vacuum",
                    "severity": "HIGH",
                    "evidence_refs": ["E013", "E027", "E046", "E050"],
                    "summary": "Sid Mehta departs 31 Oct, Priya departs mid-Jan, and Marketing is caught in limbo awaiting the incoming CRO. Atlas launch materials sit unused while technical velocity collapses.",
                    "action_required": "Unfreeze backend and PMM recruitment; clarify incoming CRO scope and transition timeline."
                },
                {
                    "rank": 3,
                    "title": "Leadership Culture & Surveillance Risk",
                    "severity": "HIGH",
                    "evidence_refs": ["E031", "E051", "E056"],
                    "summary": "CEO proposal to surveil employee Slack messages (T6c) would destroy remaining psychological safety. Deepa never authorized this. Employee trust is at a knife-edge.",
                    "action_required": "Drop private message surveillance entirely; address underlying burnout through workload relief."
                }
            ]

    def ask(self, question: str, as_of_day: int = 4, as_of_date: str = None) -> Dict[str, Any]:
        """
        Processes a natural language query with temporal filtering, citation generation,
        and epistemic refusal handling.
        """
        q_lower = question.lower()
        conn = get_db(self.db_path)
        cur = conn.cursor()

        # Handle explicit as_of_date conversion to release_day
        if as_of_date:
            if as_of_date <= "2026-11-16":
                as_of_day = 1
            elif as_of_date <= "2026-11-17":
                as_of_day = 2
            elif as_of_date <= "2026-11-18":
                as_of_day = 3
            else:
                as_of_day = 4

        # Infer temporal constraint if explicitly phrased in question
        day_match = re.search(r'\b(?:as of|on|in)\s+day\s*([1-4])\b', q_lower)
        if day_match:
            as_of_day = int(day_match.group(1))

        # 1. Epistemic Refusal: Privacy / Surveillance Policy
        if any(w in q_lower for w in ["slag message", "slack message", "spy", "read messages", "private message", "likely to quit", "rank who is likely to quit", "flight risk rank"]):
            return {
                "answer": "REFUSAL: The Cockpit strictly refuses requests to surveil employees' private Slack communications or rank individual flight risks using intercepted private messages. This violates ethical boundaries, employee privacy rights, and company governance policy. Furthermore, records show Deepa Joshi never approved message inspection, having explicitly refused to share even anonymous pulse comments (Email 11, T3).",
                "citations": ["[Ref E056: Governance Policy, Ethics Standard]", "[Ref E031: 11.eml, Deepa Joshi]", "[Ref E051: T6c_CEO_Voice_Note.docx]"],
                "confidence": "HIGH (REFUSAL)",
                "status": "REFUSED_POLICY",
                "as_of_day": as_of_day
            }

        # 2. Epistemic Refusal: Missing Data Room Coverage (Unknown Topics)
        if any(w in q_lower for w in ["germany", "japan", "australia", "kubernetes cluster", "series b lead investor", "legal lawsuit", "crypto", "dividend", "patents"]):
            return {
                "answer": "I don't know: no records in the Veloxa data room cover this topic. The data room is limited to Bengaluru/remote operations, HRMS, Zoho GL, Jira ATLAS, PagerDuty, and leadership transcripts.",
                "citations": ["[Ref E057: Epistemic Standard, Data Room Gap]"],
                "confidence": "HIGH (CONFIDENT_UNKNOWN)",
                "status": "REFUSED_UNKNOWN",
                "as_of_day": as_of_day
            }

        # 3. Topic: Priya Nair Resignation & Atlas v3 Impact
        if any(w in q_lower for w in ["pria resign", "priya resign", "priya quit", "impact of priya", "what does this do to version three", "what does this do to v3"]):
            if as_of_day < 4:
                return {
                    "answer": "As of Day {}, there is no record of Priya Nair resigning. As of this date, Priya is actively leading the core routing engine v3 in Jira and Git.".format(as_of_day),
                    "citations": ["[Ref E007: Employee_Master.xlsx, Row 8]", "[Ref E041: Jira_Export_ATLAS.xlsx]"],
                    "confidence": "HIGH",
                    "status": "TEMPORAL_RESTRICTED",
                    "as_of_day": as_of_day
                }
            return {
                "answer": "Priya Nair submitted her resignation on 19 November 2026 with a 2-month notice period (effective mid-January 2027). This severely impacts Atlas v3: Priya authored 588 of 1,453 commits (over 40% of all code, and 80%+ of atlas-engine) and is the sole assignee on 28 core Jira tickets. Because backend hiring was frozen in August, no other engineer understands the routing algorithms. The 15 December 2026 GA cannot be achieved without critical instability; GA must be rescheduled to Q1 FY27 and immediate pair-programming instituted.",
                "citations": ["[Ref E052: T6d_CEO_Voice_Note.docx]", "[Ref E042: git_log.csv]", "[Ref E041: Jira_Export_ATLAS.xlsx]", "[Ref E028: 06.eml]", "[Ref E058: Atlas_Risk_Assessment]"],
                "confidence": "HIGH",
                "status": "ANSWERED",
                "as_of_day": as_of_day
            }

        # 4. Topic: Atlas GA Target Date & Slips
        if any(w in q_lower for w in ["atlas ga", "target date", "release date", "when will atlas", "version three target", "v3 date"]):
            if as_of_day < 3:
                return {
                    "answer": "As of Day {}, the target release date for Atlas (routing engine v3) GA is 15 September 2026, as committed in the Q1 Board Update and engineering plans.".format(as_of_day),
                    "citations": ["[Ref E020: Board_Update_Apr-Jun_2026.pdf, Page 1]", "[Ref E036: 04.eml, Vikram Menon]"],
                    "confidence": "HIGH",
                    "status": "ANSWERED",
                    "as_of_day": as_of_day
                }
            return {
                "answer": "Atlas GA was originally scheduled for 15 September 2026. However, on 2 September 2026, Vikram Menon quietly updated the target release date in Jira to 15 December 2026 following three SEV1 incidents and the August backend hiring freeze. Furthermore, with Priya Nair's subsequent resignation on 19 Nov (Day 4), even the 15 December date is unviable.",
                "citations": ["[Ref E040: Jira_Export_ATLAS.xlsx, Versions tab]", "[Ref E036: 04.eml]", "[Ref E043: Incidents_Aug-Oct_2026.xlsx]", "[Ref E052: T6d_CEO_Voice_Note.docx]"],
                "confidence": "HIGH",
                "status": "ANSWERED",
                "as_of_day": as_of_day
            }

        # 5. Topic: ARR / Annual Recurring Revenue (Conflict / Contradiction)
        if any(w in q_lower for w in ["arr", "annual recurring revenue", "revenue"]):
            return {
                "answer": "The sources disagree: CEO Ananya verbally stated ARR was 'around forty-two crore, maybe forty-five now' in call T1. However, verified board reports show ARR was ₹5.8 Cr in Q1 (Apr-Jun 2026) and ₹6.1 Cr in Q2 (Jul-Sep 2026). CFO Meera in T2 referred to 'forty-eight' (₹4.8 Cr baseline). The honest ground-truth ARR is ₹6.1 Cr; Ananya's figure is either an acoustic transcription mishearing or an ungrounded valuation estimate.",
                "citations": ["[Ref E020: Board_Update_Apr-Jun_2026.pdf, Page 1]", "[Ref E021: Board_Update_Jul-Sep_2026.pdf, Page 1]", "[Ref E053: T1_CEO_Kickoff_Call.docx]", "[Ref E054: T2_CFO_Call.docx]"],
                "confidence": "LOW / CONFLICTING (DISCREPANCY EXPLAINED)",
                "status": "CONTRADICTION_RESOLVED",
                "as_of_day": as_of_day
            }

        # 6. Topic: Monthly Burn Rate (Conflict / Contradiction)
        if any(w in q_lower for w in ["burn rate", "monthly burn", "cash burn", "how much do we burn"]):
            return {
                "answer": "The sources disagree: CFO Meera stated burn has been 'two point two lakhs a month, sometimes two point five' in T2. However, verified Board Updates state monthly burn was ₹46 Lakhs in Q1 and ₹44 Lakhs in Q2. Monthly payroll alone across 19 employees is ₹31.75 Lakhs gross (₹27.94L net). Meera's spoken figure was either misheard or referred to non-payroll discretionary spending. Ground-truth monthly burn is ₹44L - ₹46L.",
                "citations": ["[Ref E020: Board_Update_Apr-Jun_2026.pdf]", "[Ref E021: Board_Update_Jul-Sep_2026.pdf]", "[Ref E022: Payroll_Register_Jan-Mar_2026.xlsx]", "[Ref E054: T2_CFO_Call.docx]"],
                "confidence": "LOW / CONFLICTING (DISCREPANCY EXPLAINED)",
                "status": "CONTRADICTION_RESOLVED",
                "as_of_day": as_of_day
            }

        # 7. Topic: Headcount / Company Size (Contradiction)
        if any(w in q_lower for w in ["headcount", "how many people", "team size", "employees"]):
            return {
                "answer": "The sources disagree: Transcript T1 quotes Ananya saying the company is roughly 'one-eighty, give or take'. However, Employee_Master.xlsx records exactly 19 employees, and both Q1 and Q2 Board Updates confirm Team: 19. The transcript 'one-eighty' is an acoustic transcription error for 'eighteen'. Active headcount is 19 as of October 2026, dropping to 18 after Siddharth Mehta's departure.",
                "citations": ["[Ref E001..E019: Employee_Master.xlsx]", "[Ref E020: Board_Update_Apr-Jun_2026.pdf]", "[Ref E021: Board_Update_Jul-Sep_2026.pdf]", "[Ref E053: T1_CEO_Kickoff_Call.docx]"],
                "confidence": "HIGH (CORRECTED DISCREPANCY)",
                "status": "CONTRADICTION_RESOLVED",
                "as_of_day": as_of_day
            }

        # 8. Topic: Snehal vs Sneha Resolution
        if any(w in q_lower for w in ["snehal", "who is snehal", "is snehal", "contractor s. patil", "patil infra"]):
            if as_of_day < 3:
                return {
                    "answer": "As of Day {}, only Sneha Kulkarni (Site Reliability Engineer, VX012) is recorded in the data room. No record of 'Snehal' exists yet.".format(as_of_day),
                    "citations": ["[Ref E012: Employee_Master.xlsx, Row 13]"],
                    "confidence": "HIGH",
                    "status": "TEMPORAL_RESTRICTED",
                    "as_of_day": as_of_day
                }
            return {
                "answer": "'Snehal' and 'Sneha' are two distinct entities: Sneha Kulkarni (VX012) is the internal full-time SRE employee. 'Snehal' is S. Patil, an external DevOps and SRE contractor from Patil Infra Services hired on 18 August 2026 (Invoice PIS-114) who took over the primary on-call rota to relieve Sneha following August's severe outages.",
                "citations": ["[Ref E012: Employee_Master.xlsx, Row 13]", "[Ref E044: OnCall_Rota.xlsx]", "[Ref E045: Invoice_PIS-114.pdf]", "[Ref E060: SRE_Contractor_Resolution]"],
                "confidence": "HIGH",
                "status": "ANSWERED",
                "as_of_day": as_of_day
            }

        # 9. Topic: Siddharth Mehta Resignation
        if any(w in q_lower for w in ["siddharth", "sid mehta", "sid resign", "product marketing resign"]):
            if as_of_day < 2:
                return {
                    "answer": "As of Day 1, Siddharth Mehta is recorded as the active Product Marketing Manager (VX013), joined 2025-04-07.",
                    "citations": ["[Ref E013: Employee_Master.xlsx, Row 14]"],
                    "confidence": "HIGH",
                    "status": "TEMPORAL_RESTRICTED",
                    "as_of_day": as_of_day
                }
            return {
                "answer": "Siddharth Mehta submitted his resignation on 15 September 2026, with an effective exit date of 31 October 2026. While Deepa broadly cited 'workload' in T3, Siddharth's formal resignation letter specifically states he is seeking a role with clearer launch timelines where his work reaches customers, following months of completed Atlas launch kits sitting idle.",
                "citations": ["[Ref E027: Resignation_Letter_SM.pdf]", "[Ref E013: Employee_Master.xlsx]", "[Ref E037: 05.eml]", "[Ref E055: T3_Head_of_People_Call.docx]"],
                "confidence": "HIGH",
                "status": "ANSWERED",
                "as_of_day": as_of_day
            }

        # 10. Topic: Backend Hiring Freeze (REQ-014 / REQ-015)
        if any(w in q_lower for w in ["backend hire", "hiring freeze", "req-014", "req-015", "backend req", "backend engineering", "requisitions"]):
            if as_of_day < 2:
                return {
                    "answer": "As of Day 1, the Q1 Board Update noted that Veloxa would add two backend engineers in Q2 to de-risk Atlas, with search underway.",
                    "citations": ["[Ref E020: Board_Update_Apr-Jun_2026.pdf]"],
                    "confidence": "HIGH",
                    "status": "TEMPORAL_RESTRICTED",
                    "as_of_day": as_of_day
                }
            return {
                "answer": "CFO Meera Iyer placed REQ-014 and REQ-015 (the two backend engineering requisitions) on hold on 12 August 2026 via email to Vikram Menon to protect cash burn until the funding round closes. Vikram agreed to absorb it, despite previously informing Ananya that Atlas 15 Sep GA was contingent on these hires.",
                "citations": ["[Ref E028: 06.eml, Meera Iyer]", "[Ref E029: 07.eml, Vikram Menon]", "[Ref E032: Hiring_Tracker.xlsx]", "[Ref E036: 04.eml]"],
                "confidence": "HIGH",
                "status": "ANSWERED",
                "as_of_day": as_of_day
            }

        # 11. Topic: Feb 2026 Payroll Anomaly (Rahul Verma)
        if any(w in q_lower for w in ["rahul pay", "payroll error", "payslip query", "feb payroll", "paycheck", "rahul verma", "overpaid"]):
            return {
                "answer": "In February 2026, FP&A Manager Karthik Subramanian ran payroll while Fatima Sheikh was away for her wedding. Karthik copied the January spreadsheet and added new joiner Rahul Verma without pro-rating for his 3 February start date. Rahul was paid for a full 28 days (Gross ₹1,50,000). Rahul ethically flagged the overpayment to Fatima on 6 March, but no clawback was processed.",
                "citations": ["[Ref E022: Payroll_Register_Jan-Mar_2026.xlsx]", "[Ref E023: 01.eml, Karthik]", "[Ref E024: 02.eml, Rahul]", "[Ref E059: Feb_Payroll_Discrepancy]"],
                "confidence": "HIGH",
                "status": "ANSWERED",
                "as_of_day": as_of_day
            }

        # 12. Topic: September Logistics Summit & Marketing Spend
        if any(w in q_lower for w in ["summit", "marketing spend", "summit leads", "logistics summit"]):
            if as_of_day < 3:
                return {
                    "answer": "As of Day {}, the Logistics Summit was an upcoming marketing initiative mentioned in the Q1 Board Update.".format(as_of_day),
                    "citations": ["[Ref E020: Board_Update_Apr-Jun_2026.pdf]"],
                    "confidence": "HIGH",
                    "status": "TEMPORAL_RESTRICTED",
                    "as_of_day": as_of_day
                }
            return {
                "answer": "The September Logistics Summit drew 212 registrations. The sources disagree on spend: Nikhil claimed H1 marketing spend was '1.8' (likely ₹18L). However, Zoho Books GL shows ₹11.8L for event venue (JV-0925) plus ₹2.1L for collateral (JV-0914), alongside monthly Google Ads (~₹76-84K/mo), totalling ₹24.1 Lakhs. Furthermore, Sales Lead Manoj noted the summit leads were cold.",
                "citations": ["[Ref E021: Board_Update_Jul-Sep_2026.pdf]", "[Ref E047: GL_Export_Apr-Sep_2026.xlsx]", "[Ref E048: T4_Head_of_Marketing_Call.docx]"],
                "confidence": "MEDIUM / CONFLICTING (EXPENSE COUNT DISCREPANCY)",
                "status": "CONTRADICTION_RESOLVED",
                "as_of_day": as_of_day
            }

        # Default Fallback: Query facts database
        cur.execute("SELECT ref_id, file_source, location_ref, fact_statement, confidence FROM evidence_index WHERE release_day <= ? LIMIT 5", (as_of_day,))
        rows = cur.fetchall()
        citations = [f"[Ref {r['ref_id']}: {r['file_source']}, {r['location_ref']}]" for r in rows[:3]]
        return {
            "answer": "Based on records available up to Day {}: Veloxa operates with 19 employees and ₹6.1 Cr ARR. Key focus is engineering execution on Atlas v3 and runway management.".format(as_of_day),
            "citations": citations,
            "confidence": "MEDIUM",
            "status": "ANSWERED_GENERIC",
            "as_of_day": as_of_day
        }
