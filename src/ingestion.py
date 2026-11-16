"""
Data Ingestion and Reconciliation Pipeline for Veloxa CXO Cockpit.
Extracts data across all 4 release packs and populates veloxa_cockpit.db.
"""
import os
import glob
import email
import sqlite3
import pandas as pd
import pypdf
import docx
from src.models import get_db, init_db, DB_PATH
from src.evidence import ENTITY_RESOLUTIONS_DATA, EVIDENCE_INDEX_DATA

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASE_PACKS = os.path.join(BASE_DIR, "Veloxa_Hackathon_Release_Packs")

def find_file(pattern):
    matches = glob.glob(os.path.join(RELEASE_PACKS, "**", pattern), recursive=True)
    return matches[0] if matches else None

def ingest_employees(conn):
    path = find_file("Employee_Master.xlsx")
    if not path:
        return
    df = pd.read_excel(path, header=2)
    df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
    cur = conn.cursor()
    for _, row in df.iterrows():
        emp_id = str(row.get("Emp ID", "")).strip()
        if not emp_id or emp_id == "nan":
            continue
        cur.execute("""
            INSERT OR REPLACE INTO employees 
            (emp_id, full_name, work_email, department, title, manager_id, join_date, location, status, exit_date, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            emp_id,
            str(row.get("Full Name", "")).strip(),
            str(row.get("Work Email", "")).strip(),
            str(row.get("Department", "")).strip(),
            str(row.get("Title", "")).strip(),
            str(row.get("Manager ID", "")).strip() if pd.notna(row.get("Manager ID")) else None,
            str(row.get("Join Date", ""))[:10].strip(),
            str(row.get("Location", "")).strip(),
            str(row.get("Status", "Active")).strip(),
            str(row.get("Exit Date", ""))[:10].strip() if pd.notna(row.get("Exit Date")) else None
        ))
    conn.commit()
    print("Ingested employees.")

def ingest_general_ledger(conn):
    path = find_file("GL_Export_Apr-Sep_2026.xlsx")
    if not path:
        return
    df = pd.read_excel(path, header=2)
    df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
    cur = conn.cursor()
    for _, row in df.iterrows():
        voucher = str(row.get("Voucher", "")).strip()
        if not voucher or voucher == "nan":
            continue
        cur.execute("""
            INSERT INTO general_ledger 
            (txn_date, voucher, payee, ref, cost_centre, amount_inr, narration, entered_by, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            str(row.get("Txn Date", ""))[:10].strip(),
            voucher,
            str(row.get("Vendor / Payee", "")).strip(),
            str(row.get("Ref", "")).strip() if pd.notna(row.get("Ref")) else None,
            str(row.get("Cost Centre", "")).strip(),
            float(row.get("Amount (Rs.)", 0.0)),
            str(row.get("Narration", "")).strip(),
            str(row.get("Entered By", "")).strip()
        ))
    conn.commit()
    print("Ingested General Ledger.")

def ingest_payroll(conn):
    path = find_file("Payroll_Register_Jan-Mar_2026.xlsx")
    if not path:
        return
    df = pd.read_excel(path, header=2)
    df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
    cur = conn.cursor()
    for _, row in df.iterrows():
        emp_id = str(row.get("Emp ID", "")).strip()
        if not emp_id or emp_id == "nan":
            continue
        cur.execute("""
            INSERT INTO payroll 
            (emp_id, name, month, days_in_month, days_payable, gross_inr, deductions_inr, net_inr, processed_by, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            emp_id,
            str(row.get("Name", "")).strip(),
            str(row.get("Month", "")).strip(),
            int(row.get("Days in Month", 30)),
            int(row.get("Days Payable", 30)),
            float(row.get("Gross (Rs.)", 0.0)),
            float(row.get("Deductions (Rs.)", 0.0)),
            float(row.get("Net (Rs.)", 0.0)),
            str(row.get("Processed By", "FS")).strip()
        ))
    conn.commit()
    print("Ingested Payroll.")

def ingest_leave_and_hiring(conn):
    # Leave
    leave_path = find_file("Leave_Register.xlsx")
    if leave_path:
        df = pd.read_excel(leave_path, header=2)
        df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
        cur = conn.cursor()
        for _, row in df.iterrows():
            emp = str(row.get("Employee", "")).strip()
            if not emp or emp == "nan":
                continue
            cur.execute("""
                INSERT INTO leave_records (emp_id, name, department, leave_type, start_date, days_taken, release_day)
                VALUES (?, ?, ?, ?, ?, ?, 2)
            """, (
                emp,
                emp,
                "Company",
                str(row.get("Leave Type", "Annual")).strip(),
                str(row.get("From", ""))[:10].strip(),
                int(row.get("Days", 1)) if pd.notna(row.get("Days")) else 1
            ))
        conn.commit()
        print("Ingested Leave Register.")

    # Hiring
    hire_path = find_file("Hiring_Tracker.xlsx")
    if hire_path:
        df = pd.read_excel(hire_path, header=2)
        df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
        cur = conn.cursor()
        for _, row in df.iterrows():
            req_id = str(row.get("Req ID", "")).strip()
            if not req_id or req_id == "nan":
                continue
            cur.execute("""
                INSERT OR REPLACE INTO hiring_requisitions 
                (req_id, role_title, department, status, opened_date, target_hire_date, hiring_manager, notes, release_day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 2)
            """, (
                req_id,
                str(row.get("Role", "")).strip(),
                str(row.get("Team", "")).strip(),
                str(row.get("Status", "Open")).strip(),
                str(row.get("Target Date", ""))[:10].strip(),
                str(row.get("Target Date", ""))[:10].strip(),
                str(row.get("Hiring Manager", "")).strip(),
                str(row.get("Notes / Status Details", "")).strip() if pd.notna(row.get("Notes / Status Details")) else None
            ))
        conn.commit()
        print("Ingested Hiring Tracker.")

    # Pulse
    pulse_path = find_file("Pulse_Survey.xlsx")
    if pulse_path:
        df = pd.read_excel(pulse_path, header=2)
        df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
        cur = conn.cursor()
        for _, row in df.iterrows():
            dept = str(row.get("Team", "")).strip()
            if not dept or dept == "nan":
                continue
            cur.execute("""
                INSERT INTO pulse_surveys (quarter, department, favorability_pct, participation_pct, key_themes, release_day)
                VALUES (?, ?, ?, ?, ?, 2)
            """, (
                str(row.get("Quarter", "Q3 2026")).strip(),
                dept,
                int(row.get("Favorability (%)", row.get("Score (%)", 70))) if pd.notna(row.get("Favorability (%)", row.get("Score (%)", 70))) else 70,
                int(row.get("Responses", 10)) if pd.notna(row.get("Responses")) else 10,
                str(row.get("Top Themes / Highlights", "")).strip()
            ))
        conn.commit()
        print("Ingested Pulse Surveys.")

def ingest_engineering(conn):
    # Jira
    jira_path = find_file("Jira_Export_ATLAS.xlsx")
    if jira_path:
        df = pd.read_excel(jira_path, sheet_name="Issues", header=2)
        df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
        cur = conn.cursor()
        assignee_map = {"PN": "Priya Nair", "AD": "Arjun Das", "RV": "Rahul Verma", "SK": "Sneha Kulkarni", "VM": "Vikram Menon"}
        for _, row in df.iterrows():
            key = str(row.get("Key", "")).strip()
            if not key or key == "nan":
                continue
            initials = str(row.get("Assignee", "")).strip()
            cur.execute("""
                INSERT OR REPLACE INTO jira_issues 
                (key, issue_type, summary, epic_link, assignee_initials, assignee_name, story_points, status, created_date, resolved_date, fix_version, release_day)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 3)
            """, (
                key,
                str(row.get("Type", "Story")).strip(),
                str(row.get("Summary", "")).strip(),
                str(row.get("Epic Link", "")).strip(),
                initials,
                assignee_map.get(initials, initials),
                int(row.get("Story Points", 1)) if pd.notna(row.get("Story Points")) else 1,
                str(row.get("Status", "To Do")).strip(),
                str(row.get("Created", ""))[:10].strip(),
                str(row.get("Resolved", ""))[:10].strip() if pd.notna(row.get("Resolved")) else None,
                str(row.get("Fix Version", "Atlas GA")).strip()
            ))
        conn.commit()
        print("Ingested Jira Issues.")

    # Git log
    git_path = find_file("git_log.csv")
    if git_path:
        df = pd.read_csv(git_path)
        cur = conn.cursor()
        author_map = {
            "priya.n@veloxa.in": "Priya Nair",
            "pnair@users.noreply.github.com": "Priya Nair",
            "arjun@veloxa.in": "Arjun Das",
            "rahul.v@veloxa.in": "Rahul Verma",
            "sneha.k@veloxa.in": "Sneha Kulkarni",
            "vikram@veloxa.in": "Vikram Menon"
        }
        for _, row in df.iterrows():
            sha = str(row.get("sha", "")).strip()
            email_addr = str(row.get("author_email", "")).strip()
            cur.execute("""
                INSERT OR REPLACE INTO git_commits 
                (sha, author_email, author_name, committed_at, repo, message, files_changed, release_day)
                VALUES (?, ?, ?, ?, ?, ?, ?, 3)
            """, (
                sha,
                email_addr,
                author_map.get(email_addr, email_addr),
                str(row.get("committed_at", "")).strip(),
                str(row.get("repo", "")).strip(),
                str(row.get("message", "")).strip(),
                int(row.get("files_changed", 1))
            ))
        conn.commit()
        print("Ingested Git Commits.")

    # Incidents
    inc_path = find_file("Incidents_Aug-Oct_2026.xlsx")
    if inc_path:
        df = pd.read_excel(inc_path, header=2)
        df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
        cur = conn.cursor()
        for _, row in df.iterrows():
            inc_id = str(row.get("ID", "")).strip()
            if not inc_id or inc_id == "nan":
                continue
            cur.execute("""
                INSERT OR REPLACE INTO incidents 
                (incident_id, severity, opened_at, resolved_at, service, responder, release_day)
                VALUES (?, ?, ?, ?, ?, ?, 3)
            """, (
                inc_id,
                str(row.get("Severity", "SEV2")).strip(),
                str(row.get("Opened", "")).strip(),
                str(row.get("Resolved", "")).strip(),
                str(row.get("Service", "")).strip(),
                str(row.get("Responder", "")).strip()
            ))
        conn.commit()
        print("Ingested Incidents.")

    # OnCall rota
    rota_path = find_file("OnCall_Rota.xlsx")
    if rota_path:
        df = pd.read_excel(rota_path, header=2)
        df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]
        cur = conn.cursor()
        for _, row in df.iterrows():
            week_of = str(row.get("Week of", "")).strip()
            if not week_of or week_of == "nan":
                continue
            cur.execute("""
                INSERT INTO on_call_rota (week_of, primary_responder, secondary_responder, release_day)
                VALUES (?, ?, ?, 3)
            """, (
                str(week_of)[:10],
                str(row.get("Primary", "")).strip(),
                str(row.get("Secondary", "")).strip()
            ))
        conn.commit()
        print("Ingested On-Call Rota.")

def ingest_emails_and_docs(conn):
    cur = conn.cursor()
    # Emails
    email_files = sorted(glob.glob(os.path.join(RELEASE_PACKS, "**", "*.eml"), recursive=True))
    for em_path in email_files:
        fn = os.path.basename(em_path)
        rel_day = 1 if "Day1" in em_path else (2 if "Day2" in em_path else (3 if "Day3" in em_path else 4))
        with open(em_path, 'r', encoding='utf-8', errors='ignore') as f:
            msg = email.message_from_file(f)
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore') if msg.get_payload() else ''
            
            cur.execute("""
                INSERT OR REPLACE INTO emails (email_id, from_addr, to_addr, sent_date, subject, body, release_day)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                fn,
                str(msg['From'] or '').strip(),
                str(msg['To'] or '').strip(),
                str(msg['Date'] or '').strip(),
                str(msg['Subject'] or '').strip(),
                body.strip(),
                rel_day
            ))
    conn.commit()
    print(f"Ingested {len(email_files)} Emails.")

    # Transcripts
    transcript_files = sorted(glob.glob(os.path.join(RELEASE_PACKS, "**", "transcripts", "*.docx"), recursive=True))
    for t_path in transcript_files:
        fn = os.path.basename(t_path)
        rel_day = 1 if "Day1" in t_path else (2 if "Day2" in t_path else (3 if "Day3" in t_path else 4))
        doc = docx.Document(t_path)
        text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
        cur.execute("""
            INSERT OR REPLACE INTO transcripts (transcript_id, title, speaker, call_date, raw_text, key_takeaways, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fn.replace(".docx", ""),
            fn,
            "Ananya / Leadership",
            "Nov 2026",
            text,
            text[:300],
            rel_day
        ))
    conn.commit()
    print(f"Ingested {len(transcript_files)} Transcripts.")

    # Documents
    pdf_files = sorted(glob.glob(os.path.join(RELEASE_PACKS, "**", "*.pdf"), recursive=True))
    for p_path in pdf_files:
        fn = os.path.basename(p_path)
        if "Worksheet" in fn or "Printout" in fn:
            continue
        rel_day = 1 if "Day1" in p_path else (2 if "Day2" in p_path else (3 if "Day3" in p_path else 4))
        try:
            reader = pypdf.PdfReader(p_path)
            content = '\n'.join([p.extract_text() or '' for p in reader.pages])
            cur.execute("""
                INSERT OR REPLACE INTO documents (doc_id, title, doc_date, doc_type, file_path, content_summary, release_day)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                fn.replace(".pdf", ""),
                fn,
                "2026",
                "PDF Report",
                p_path,
                content[:500],
                rel_day
            ))
        except Exception as e:
            print(f"Error parsing PDF {fn}: {e}")
    conn.commit()
    print(f"Ingested PDFs.")

def ingest_evidence_and_entities(conn):
    cur = conn.cursor()
    # Entity resolutions
    for row in ENTITY_RESOLUTIONS_DATA:
        cur.execute("""
            INSERT INTO entity_resolutions (raw_identifier, seen_in_file, resolves_to, kind, evidence_refs, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, row)
    
    # Evidence index
    for row in EVIDENCE_INDEX_DATA:
        cur.execute("""
            INSERT OR REPLACE INTO evidence_index 
            (ref_id, file_source, location_ref, fact_statement, entities_named, date_as_written, date_normalized, confidence, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)
    conn.commit()
    print(f"Populated {len(ENTITY_RESOLUTIONS_DATA)} Entity Resolutions and {len(EVIDENCE_INDEX_DATA)} Evidence Index Facts.")

def export_templates():
    os.makedirs(os.path.join(BASE_DIR, "reconciled_worksheets"), exist_ok=True)
    df_ent = pd.DataFrame(ENTITY_RESOLUTIONS_DATA, columns=[
        "Name or identifier as seen", "Seen in (file)", "Resolves to", "Kind (person/vendor/project)", "Evidence refs", "Confidence (H/M/L)"
    ])
    df_ent.to_excel(os.path.join(BASE_DIR, "reconciled_worksheets", "Entity_Resolution.xlsx"), index=False)
    
    df_ev = pd.DataFrame(EVIDENCE_INDEX_DATA, columns=[
        "Ref", "File", "Sheet / page / row", "Fact (your words)", "Entities named", "Date (as written)", "Date (normalised, IST)", "Confidence (H/M/L)", "Release Day"
    ])
    df_ev.to_excel(os.path.join(BASE_DIR, "reconciled_worksheets", "Evidence_Index.xlsx"), index=False)
    print("Exported reconciled worksheets to reconciled_worksheets/ folder.")

def run_pipeline():
    init_db()
    conn = get_db()
    ingest_employees(conn)
    ingest_general_ledger(conn)
    ingest_payroll(conn)
    ingest_leave_and_hiring(conn)
    ingest_engineering(conn)
    ingest_emails_and_docs(conn)
    ingest_evidence_and_entities(conn)
    conn.close()
    export_templates()
    print("\n--- INGESTION & RECONCILIATION PIPELINE COMPLETE ---")

if __name__ == "__main__":
    run_pipeline()
