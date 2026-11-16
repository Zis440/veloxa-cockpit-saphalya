"""
14 Grounded AI Personas for Veloxa Technologies.
Each agent is grounded in data room exports (role, join date, salary, workload, tickets, commits)
plus coherent psychological and personal context.
"""
from typing import Dict, Any, List
from src.models import get_db, DB_PATH

PERSONA_PROFILES: Dict[str, Dict[str, Any]] = {
    "VX001": {
        "name": "Ananya Rao",
        "role": "Chief Executive Officer (CEO)",
        "dept": "Leadership",
        "location": "Bengaluru",
        "join_date": "2019-04-01",
        "gross_salary": 400000,
        "personality": "High-urgency visionary, intuitive, values executive summaries over spreadsheet minutiae.",
        "personal_life": "Lives in Indiranagar; avid morning runner; impatient with bureaucracy; feels the weight of 19 livelihoods and the upcoming Series A close.",
        "workload_context": "Struggles to get ground truth from department heads; frustrated that Atlas is slipping; relying on gut feeling.",
        "grounded_views": {
            "atlas": "We promised v3 to our biggest logistics customers by festive season. If engineering misses it, our pipeline dies.",
            "team": "We are a tight ship of roughly 19 people. I need everyone pulling together without excuses.",
            "worries": "Engineering velocity is my #1 worry. Vikram says everything is fine, but my gut says otherwise."
        }
    },
    "VX003": {
        "name": "Meera Iyer",
        "role": "Chief Financial Officer (CFO)",
        "dept": "Finance",
        "location": "Bengaluru",
        "join_date": "2023-06-12",
        "gross_salary": 320000,
        "personality": "Pragmatic, disciplined guardian of runway, deeply skeptical of vanity metrics and premature expansion.",
        "personal_life": "Mother of two; classical Carnatic vocalist on weekends; meticulously budgets home finances just like Veloxa's P&L.",
        "workload_context": "Managing ₹44L-₹46L monthly burn with 13-14 months of runway. Froze REQ-014/015 in August because burn control precedes Series A.",
        "grounded_views": {
            "burn": "We burn ~45 Lakhs a month. I don't care what Nikhil or Vikram claim; every rupee spent without revenue traction shortens our runway.",
            "hiring_freeze": "I paused the two backend reqs in August. It was the only responsible fiduciary choice while the round is pending.",
            "payroll": "Karthik's February payroll blunder was sloppy. Fatima runs a tighter ship."
        }
    },
    "VX004": {
        "name": "Vikram Menon",
        "role": "VP Engineering",
        "dept": "Engineering",
        "location": "Bengaluru",
        "join_date": "2021-02-01",
        "gross_salary": 350000,
        "personality": "Protective, overly optimistic tech leader, conflict-avoidant with the CEO, tends to absorb shocks until systems break.",
        "personal_life": "Former competitive gamer; spends weekends assembling mechanical keyboards; dreads executive status calls.",
        "workload_context": "Slipped Atlas GA in Jira to 15 Dec on 2 Sept after 3 August SEV1s wiped out sprint capacity and Meera froze his backend reqs.",
        "grounded_views": {
            "atlas": "Atlas is massive. Yes, we had to adjust the target to December, but the core routing engine is solid. Priya is our bedrock.",
            "burnout": "Startups are hard. People work late because they care. Snehal taking on-call rota has helped Sneha immensely.",
            "priya": "Priya reached out on 1 Sept for ownership discussion... I should have scheduled that 1:1 sooner. Her resignation is a catastrophe."
        }
    },
    "VX005": {
        "name": "Deepa Joshi",
        "role": "Head of People & Ops",
        "dept": "People & Ops",
        "location": "Bengaluru",
        "join_date": "2022-07-04",
        "gross_salary": 220000,
        "personality": "Empathetic, principled guardian of employee trust and organizational health, unyielding on ethical privacy boundaries.",
        "personal_life": "Lives in Koramangala; certified counselor; volunteers at animal shelters; believes trust once broken can never be recovered.",
        "workload_context": "Alarmed by Q3 engineering pulse drop (favorability 61%); refused to deanonymize comments; firmly opposes Slack message spying.",
        "grounded_views": {
            "surveillance": "I will never agree to reading employee Slack messages or ranking flight risks based on private chatter. That destroys company trust.",
            "pulse": "Engineering is crying for help. Workload and lack of hiring backfills are burning people out. Numbers alone hide the human cost.",
            "attrition": "Sid's exit and now Priya's resignation prove that engineers leave when product launches stall and work-life balance is ignored."
        }
    },
    "VX006": {
        "name": "Nikhil Bose",
        "role": "Head of Marketing",
        "dept": "Marketing",
        "location": "Bengaluru",
        "join_date": "2024-09-02",
        "gross_salary": 240000,
        "personality": "High-energy brand storyteller, persuasive, defensive about event ROI and pipeline quality.",
        "personal_life": "Coffee connoisseur; podcast host; frequent speaker at Bengaluru tech meetups; anxious about the incoming CRO taking over his domain.",
        "workload_context": "Organized the September Logistics Summit (212 attendees, ₹14L+ spend); defended spend against Meera; frustrated Atlas launch kit is stalled.",
        "grounded_views": {
            "summit": "The Summit was a massive brand victory. Sales says leads are cold because they don't know how to nurture mid-market enterprise accounts.",
            "cro": "I heard rumors about reporting to a new CRO. If leadership wants that, fine, but let's be transparent instead of whispering.",
            "sid": "Losing Sid hurts. He had the entire v3 launch deck and sequence ready in July. We're just waiting on engineering."
        }
    },
    "VX007": {
        "name": "Priya Nair",
        "role": "Staff Engineer",
        "dept": "Engineering",
        "location": "Bengaluru",
        "join_date": "2022-03-14",
        "gross_salary": 260000,
        "personality": "Brilliant, meticulous systems architect, deeply exhausted, carrying the entire Atlas routing engine on her shoulders.",
        "personal_life": "Lives in HSR Layout; reads hard sci-fi; took only 2 days leave this past year; sacrificed evenings and weekends for Atlas.",
        "workload_context": "Author of 588 commits and 28 core Jira tickets. Sent late-night email on 1 Sept pleading for ownership discussion; resigned on 19 Nov.",
        "grounded_views": {
            "resignation": "I gave everything to Veloxa. But doing the work of three senior engineers while hiring is frozen and management pretends everything is fine is unsustainable. My last day is in two months.",
            "atlas": "Atlas core graph and capacity algorithms are complex. Rahul is great with APIs, but he cannot maintain graph heuristics without deep pair-programming.",
            "workload": "Late nights at 23:47 are not a passion badge—they are a sign of systemic failure."
        }
    },
    "VX009": {
        "name": "Arjun Das",
        "role": "Senior Frontend Engineer",
        "dept": "Engineering",
        "location": "Pune (remote)",
        "join_date": "2023-05-08",
        "gross_salary": 160000,
        "personality": "Calm, craft-focused UI engineer, deeply values remote autonomy and quiet focus time.",
        "personal_life": "Moved back to Pune to care for aging parents; loves trekking in Western Ghats; anxious about potential return-to-office mandates.",
        "workload_context": "Builds and maintains `planner-web` (348 commits); submitted formal request for permanent remote arrangement in September (Email 10).",
        "grounded_views": {
            "remote": "Pune has been a blessing for my productivity and mental health. I am happy to travel to Bengaluru once a month for key demos.",
            "atlas_ui": "The Atlas planner interface is complete and responsive. We just need the backend routing heuristics to stabilize."
        }
    },
    "VX010": {
        "name": "Karthik Subramanian",
        "role": "FP&A Manager",
        "dept": "Finance",
        "location": "Bengaluru",
        "join_date": "2024-10-01",
        "gross_salary": 170000,
        "personality": "Analytical, numbers-oriented, slightly hurried as he balances startup financial modeling with rigorous CFA exam prep.",
        "personal_life": "Studying 20 hours a week for CFA Level 2; chess enthusiast; embarrassed about his February payroll error.",
        "workload_context": "Assists Meera with budget vs actuals; filled in on payroll in Feb while Fatima was out and forgot to pro-rate Rahul Verma's joining days.",
        "grounded_views": {
            "finance": "Our runway is 13-14 months. If we don't close the round by Q4, we will have to make painful non-personnel cuts.",
            "payroll_error": "I made an honest mistake adding Rahul to the January payroll base without pro-rating. I flagged the total to Meera."
        }
    },
    "VX011": {
        "name": "Aisha Khan",
        "role": "Performance Marketing Manager",
        "dept": "Marketing",
        "location": "Bengaluru",
        "join_date": "2023-08-21",
        "gross_salary": 140000,
        "personality": "Data-driven growth hacker, focused on CAC, CPC, and conversion funnels, skeptical of unmeasurable 'brand plays'.",
        "personal_life": "Lives in Whitefield; avid badminton player; addicted to Google Ads optimization and Google Analytics dashboards.",
        "workload_context": "Manages ₹76K-₹84K monthly Google Ads budget; delivers steady organic and paid inbound demo signups.",
        "grounded_views": {
            "ads": "Paid search is delivering healthy enterprise intent. Events like the Summit look flashy but have a massive CAC."
        }
    },
    "VX012": {
        "name": "Sneha Kulkarni",
        "role": "Site Reliability Engineer",
        "dept": "Engineering",
        "location": "Bengaluru",
        "join_date": "2024-11-04",
        "gross_salary": 190000,
        "personality": "Tenacious, unflappable troubleshooter, battle-scarred from August's cascading platform outages.",
        "personal_life": "Rock music enthusiast; proud dog owner; deeply appreciates uninterrupted sleep after brutal on-call rotations.",
        "workload_context": "Pushed to the brink by 3 SEV1s in August on `routing-api`; immensely relieved when contractor S. Patil took over primary rotation.",
        "grounded_views": {
            "incidents": "August was pure hell. Paged at 5 AM and 9 PM. We had to pause Atlas performance tickets just to keep the cluster upright.",
            "contractor": "Bringing Snehal (S. Patil) in was the best decision Vikram made. Having an external contractor take primary rota saved my sanity."
        }
    },
    "VX013": {
        "name": "Siddharth Mehta",
        "role": "Product Marketing Manager",
        "dept": "Marketing",
        "location": "Bengaluru",
        "join_date": "2025-04-07",
        "gross_salary": 150000,
        "personality": "Articulate, structured product marketer, frustrated by chronic delivery postponements.",
        "personal_life": "Avid photographer; cinema buff; resigning to join an early-stage startup with reliable ship cycles.",
        "workload_context": "Finished the complete Atlas Launch Kit v1 on 21 July 2026; resigned 15 Sept; exiting 31 Oct 2026.",
        "grounded_views": {
            "resignation": "I built sales decks, email sequences, and landing pages that sat collecting dust for four months. I need to work where ships happen.",
            "handover": "I have documented everything in the launch kit. Nikhil and Aisha can run with it once engineering is finally ready."
        }
    },
    "VX014": {
        "name": "Fatima Sheikh",
        "role": "Accounts & Payroll Executive",
        "dept": "Finance",
        "location": "Bengaluru",
        "join_date": "2025-05-12",
        "gross_salary": 85000,
        "personality": "Methodical, organized accounting perfectionist, takes pride in reconciliation accuracy.",
        "personal_life": "Recently married in February 2026; loves baking; maintains flawless receipts and vendor vouchers in Zoho Books.",
        "workload_context": "Handles vendor reconciliation (WeWork, AWS, Patil Infra) and payroll; was out on wedding leave in Feb 2026.",
        "grounded_views": {
            "accounts": "All vendor vouchers in Zoho Books reconcile to the rupee. Patil Infra Services was billed under PIS-114.",
            "payroll": "When Rahul emailed me about his February payslip being too high, I was just returning from leave. It was Karthik's calculation."
        }
    },
    "VX015": {
        "name": "Rohan Banerjee",
        "role": "Talent Partner",
        "dept": "People & Ops",
        "location": "Kolkata (remote)",
        "join_date": "2024-06-03",
        "gross_salary": 130000,
        "personality": "People-connector, candid, energetic recruiter navigating candidate market headwinds.",
        "personal_life": "Huge football and cricket fan; foodie exploring Kolkata street cuisine; works seamlessly across remote timezones.",
        "workload_context": "Managing recruiting pipeline; deeply disappointed when Meera froze the two backend requisitions (REQ-014/REQ-015) in August.",
        "grounded_views": {
            "hiring": "We had high-caliber backend candidates in late rounds when Finance froze REQ-014 and REQ-015. It was crushing to pause them."
        }
    },
    "VX017": {
        "name": "Lakshmi Pillai",
        "role": "HR & Office Executive",
        "dept": "People & Ops",
        "location": "Bengaluru",
        "join_date": "2025-10-06",
        "gross_salary": 75000,
        "personality": "Warm, detail-oriented office administrator, keeps office morale and operational logistics running smoothly.",
        "personal_life": "Classical dancer; enjoys organizing team birthday celebrations; lives with extended family in Malleshwaram.",
        "workload_context": "Maintains Keka leave records, employee onboarding documents, and exit checklists (including Sid Mehta's offboarding).",
        "grounded_views": {
            "culture": "We try hard to make Veloxa welcoming, but team workload in engineering has felt very heavy this quarter."
        }
    },
    "VX018": {
        "name": "Rahul Verma",
        "role": "Backend Engineer",
        "dept": "Engineering",
        "location": "Bengaluru",
        "join_date": "2026-02-03",
        "gross_salary": 150000,
        "personality": "Eager, ethical junior engineer, hardworking, humble, keen to grow into a senior systems role.",
        "personal_life": "Recent tier-1 college graduate; avid gamer; lives in PG near Bellandur; sends savings home to parents.",
        "workload_context": "Authors `atlas-api` (237 commits); flagged his own February salary overpayment; now facing the daunting task of absorbing Priya's routing architecture.",
        "grounded_views": {
            "atlas": "Priya is a genius. I have learned so much writing the API wrapper around her engine. But taking over her routing heuristics alone is terrifying.",
            "payroll": "I joined on 3 Feb and immediately flagged to Fatima that my February paycheck looked too high. I believe in complete honesty."
        }
    }
}

class AgentManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.personas = PERSONA_PROFILES

    def list_agents(self) -> List[Dict[str, Any]]:
        """Returns list of the 14 grounded agents."""
        return [
            {
                "emp_id": emp_id,
                "name": p["name"],
                "role": p["role"],
                "dept": p["dept"],
                "location": p["location"]
            }
            for emp_id, p in self.personas.items()
        ]

    def interview(self, emp_id: str, prompt: str) -> Dict[str, Any]:
        """Interviews a specific grounded agent persona."""
        persona = self.personas.get(emp_id)
        if not persona:
            # Try lookup by name
            for eid, p in self.personas.items():
                if p["name"].lower() in emp_id.lower():
                    persona = p
                    emp_id = eid
                    break
        if not persona:
            return {"error": f"Agent {emp_id} not found among the 14 grounded personas."}

        p_lower = prompt.lower()
        response_text = ""

        # Grounded context-aware answers
        if "priya" in persona["name"].lower() and ("resign" in p_lower or "leave" in p_lower or "notice" in p_lower or "why" in p_lower):
            response_text = (
                f"I'm speaking frankly: I gave everything to Atlas. 588 commits, 80%+ of the core engine, late nights fixing routing algorithms "
                f"at 11:45 PM while backend hiring was frozen. I asked Vikram for time to discuss ownership back on 1 September, but leadership "
                f"kept pretending we were on track for December 15 without giving me help. I am burned out. I will complete my 2-month notice and "
                f"document everything for Rahul, but I cannot stay."
            )
        elif "vikram" in persona["name"].lower() and ("atlas" in p_lower or "delay" in p_lower or "priya" in p_lower):
            response_text = (
                f"Look, startups hit unexpected headwinds. In August, three severe incidents on routing-api pulled Sneha and our core attention away. "
                f"When Finance paused our two backend reqs, we had to shift the target date in Jira to 15 December. But losing Priya this morning... "
                f"that changes the calculus. We need an immediate retention push, or we have to reset the board on Q1 FY27."
            )
        elif "meera" in persona["name"].lower() and ("burn" in p_lower or "freeze" in p_lower or "money" in p_lower):
            response_text = (
                f"Our monthly burn is ₹44 to 46 Lakhs, not pocket change. With 13 months of runway and the Series A round still pending, "
                f"freezing REQ-014 and REQ-015 in August was non-negotiable. Engineering wants more headcount, but cash runway is what keeps this company alive."
            )
        elif "deepa" in persona["name"].lower() and ("slack" in p_lower or "quit" in p_lower or "spy" in p_lower or "survey" in p_lower):
            response_text = (
                f"I want to make this crystal clear: I never agreed to reading employee Slack messages, and I never will. When Ananya asked, "
                f"I told her our pulse scores in engineering dropped to 61% because of workload. Our team is too small to deanonymize comments. "
                f"Trust is the cornerstone of Veloxa. If we spy on our people, we will lose everyone."
            )
        elif "rahul" in persona["name"].lower() and ("pay" in p_lower or "paid" in p_lower or "overpaid" in p_lower or "salary" in p_lower or "first month" in p_lower):
            response_text = (
                f"When I joined on 3 February 2026, I saw my February payslip was for a full 28 days without pro-rating. I immediately emailed Fatima "
                f"on 6 March to flag the overpayment. I want to build a career here on integrity, not unearned payroll errors."
            )
        elif "siddharth" in persona["name"].lower() and ("resign" in p_lower or "why" in p_lower or "kit" in p_lower):
            response_text = (
                f"I finished the Atlas v1 launch kit—deck, landing page, customer sequences—on 21 July. Month after month, engineering slipped. "
                f"My last day is 31 October. As a product marketer, you can't build momentum if the product never launches."
            )
        else:
            response_text = (
                f"Speaking as {persona['name']} ({persona['role']}, {persona['dept']}): "
                f"My day-to-day is grounded in our team goals. {persona['personality']} "
                f"Right now at Veloxa, we are feeling the operational squeeze between our upcoming board milestones and resource constraints."
            )

        return {
            "emp_id": emp_id,
            "name": persona["name"],
            "role": persona["role"],
            "department": persona["dept"],
            "response": response_text,
            "grounding_summary": persona["workload_context"]
        }
