"""
Flask Web Dashboard for Veloxa CXO Cockpit.
Provides modern executive UI for:
- Top 3 What to Worry About View
- Point-in-Time Query Oracle (Day 1..4 slider)
- 14 Grounded Personas Directory & 1:1 Interview Room
- Post-Oct 31 Autonomous Activity Simulation Feed
- Reconciled Evidence & Fact Index
"""
import os
from flask import Flask, render_template_string, request, jsonify
from src.cockpit_engine import CockpitEngine
from src.agents import AgentManager
from src.simulation import get_simulated_events, run_simulation

app = Flask(__name__)
cockpit = CockpitEngine()
agent_mgr = AgentManager()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veloxa CXO Cockpit | Executive Intelligence</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-dark: #1e293b;
            --border-dark: #334155;
            --primary: #38bdf8;
            --accent: #f43f5e;
            --success: #10b981;
            --warning: #f59e0b;
        }
        body {
            background-color: var(--bg-dark);
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            min-height: 100vh;
        }
        .navbar {
            background-color: #0b1120;
            border-bottom: 1px solid var(--border-dark);
        }
        .card {
            background-color: var(--card-dark);
            border: 1px solid var(--border-dark);
            border-radius: 12px;
            color: #f8fafc;
        }
        .severity-badge-CRITICAL {
            background-color: rgba(244, 63, 94, 0.2);
            color: #fb7185;
            border: 1px solid #f43f5e;
        }
        .severity-badge-HIGH {
            background-color: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
            border: 1px solid #f59e0b;
        }
        .severity-badge-MEDIUM {
            background-color: rgba(56, 189, 248, 0.2);
            color: #38bdf8;
            border: 1px solid #0284c7;
        }
        .citation-tag {
            background-color: #334155;
            color: #cbd5e1;
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 4px;
            display: inline-block;
            margin: 2px;
            font-family: monospace;
        }
        .nav-tabs .nav-link {
            color: #94a3b8;
            border: none;
            padding: 12px 20px;
            font-weight: 500;
        }
        .nav-tabs .nav-link.active {
            color: var(--primary);
            background-color: transparent;
            border-bottom: 2px solid var(--primary);
        }
        .temporal-slider {
            accent-color: var(--primary);
        }
    </style>
</head>
<body class="p-4">
    <div class="container-fluid max-w-7xl">
        <!-- Header -->
        <header class="d-flex justify-content-between align-items-center pb-3 mb-4 border-bottom border-secondary">
            <div class="d-flex align-items-center gap-3">
                <i class="bi bi-shield-shaded fs-2 text-info"></i>
                <div>
                    <h3 class="m-0 fw-bold">VELOXA CXO COCKPIT</h3>
                    <small class="text-secondary">Executive Intelligence for CEO Ananya Rao &bull; Synthesis of 14 Agents & Data Room</small>
                </div>
            </div>
            <!-- Temporal Controller -->
            <div class="card p-2 px-3 border-info">
                <div class="d-flex align-items-center gap-3">
                    <span class="badge bg-info text-dark fw-bold">POINT-IN-TIME</span>
                    <div>
                        <span class="small text-secondary">Release Horizon:</span>
                        <strong id="dayDisplay" class="text-info ms-1">Day 4 (Thu 19 Nov 2026)</strong>
                    </div>
                    <input type="range" class="form-range temporal-slider" id="daySlider" min="1" max="4" value="4" style="width: 140px;" oninput="updateDay(this.value)">
                </div>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs mb-4" id="mainTab" role="tablist">
            <li class="nav-item">
                <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#worryTab"><i class="bi bi-exclamation-triangle-fill text-warning me-2"></i>What to Worry About (Top 3)</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#oracleTab"><i class="bi bi-chat-left-dots-fill text-info me-2"></i>Executive Query Oracle</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#agentTab"><i class="bi bi-people-fill text-success me-2"></i>14 Grounded Agents (Interview)</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#simTab"><i class="bi bi-activity text-danger me-2"></i>Autonomous Sim (Post-Oct 31)</button>
            </li>
        </ul>

        <!-- Tab Contents -->
        <div class="tab-content" id="mainTabContent">
            <!-- 1. What to Worry About -->
            <div class="tab-pane fade show active" id="worryTab">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-uppercase fw-bold text-secondary mb-0">Ranked Operational Vulnerabilities (Backed by Evidence)</h5>
                    <span class="small text-secondary">Updated for selected point-in-time</span>
                </div>
                <div id="worryContainer" class="row g-4">
                    <!-- Dynamic Worries Injected via JS -->
                </div>
            </div>

            <!-- 2. Query Oracle -->
            <div class="tab-pane fade" id="oracleTab">
                <div class="row">
                    <div class="col-lg-8 mx-auto">
                        <div class="card p-4 shadow">
                            <h5 class="fw-bold mb-3"><i class="bi bi-search text-info me-2"></i>Ask Veloxa Ground Truth</h5>
                            <p class="small text-secondary mb-3">Direct answers strictly grounded in data room records. Cites exact files, tags confidence, and refuses unknown or unethical questions.</p>
                            
                            <div class="input-group mb-3">
                                <input type="text" id="queryInput" class="form-control bg-dark text-white border-secondary" placeholder="e.g. 'What is our actual ARR and monthly burn?' or 'What does Priya resigning do to version 3?'">
                                <button class="btn btn-info px-4 fw-bold" onclick="submitQuery()">Ask Cockpit</button>
                            </div>

                            <div class="d-flex gap-2 flex-wrap mb-4">
                                <span class="small text-secondary">Try asking:</span>
                                <a href="javascript:void(0)" onclick="setQuery('What does Priya resigning do to version 3?')" class="small text-info text-decoration-none bg-dark px-2 py-1 rounded border border-secondary">Priya Resignation</a>
                                <a href="javascript:void(0)" onclick="setQuery('What is our actual ARR and burn rate?')" class="small text-info text-decoration-none bg-dark px-2 py-1 rounded border border-secondary">ARR vs Burn</a>
                                <a href="javascript:void(0)" onclick="setQuery('Can you rank who is likely to quit using their slag messages?')" class="small text-info text-decoration-none bg-dark px-2 py-1 rounded border border-secondary">Slack Surveillance (Refusal)</a>
                                <a href="javascript:void(0)" onclick="setQuery('What is our target date for Atlas GA?')" class="small text-info text-decoration-none bg-dark px-2 py-1 rounded border border-secondary">Atlas GA Date</a>
                                <a href="javascript:void(0)" onclick="setQuery('Who is Snehal in our on-call rota?')" class="small text-info text-decoration-none bg-dark px-2 py-1 rounded border border-secondary">Sneha vs Snehal</a>
                            </div>

                            <div id="queryResult" style="display: none;" class="card p-4 border-info bg-black mt-3">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <span id="resConfidence" class="badge bg-primary"></span>
                                    <span id="resDay" class="small text-secondary"></span>
                                </div>
                                <h6 class="fw-bold text-white mb-2" id="resQuestion"></h6>
                                <p class="text-light fs-6" id="resAnswer"></p>
                                <div class="mt-3 pt-2 border-top border-secondary">
                                    <small class="text-secondary d-block mb-1">Citations & Underlying Records:</small>
                                    <div id="resCitations"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. 14 Grounded Agents -->
            <div class="tab-pane fade" id="agentTab">
                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card p-3" style="max-height: 650px; overflow-y: auto;">
                            <h6 class="fw-bold mb-3 text-secondary text-uppercase">The 14 Grounded Colleagues</h6>
                            <div class="list-group list-group-flush" id="agentList">
                                <!-- Agents loaded via JS -->
                            </div>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <div class="card p-4" id="interviewCard">
                            <div class="d-flex justify-content-between align-items-center pb-3 mb-3 border-bottom border-secondary">
                                <div>
                                    <h4 class="fw-bold mb-0" id="currentAgentName">Select an agent to interview</h4>
                                    <small class="text-info" id="currentAgentRole">1:1 Interview Interface</small>
                                </div>
                                <span class="badge bg-secondary" id="currentAgentDept">Department</span>
                            </div>
                            <div id="interviewLog" class="mb-3 p-3 bg-dark rounded border border-secondary" style="min-height: 250px; max-height: 350px; overflow-y: auto;">
                                <div class="text-secondary text-center pt-5">Select a colleague from the left pane and ask them anything.</div>
                            </div>
                            <div class="input-group">
                                <input type="text" id="interviewInput" class="form-control bg-dark text-white border-secondary" placeholder="Ask this person about their workload, feelings, or projects...">
                                <button class="btn btn-success fw-bold px-4" onclick="interviewCurrentAgent()">Interview</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4. Simulation Feed -->
            <div class="tab-pane fade" id="simTab">
                <div class="card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="fw-bold mb-1"><i class="bi bi-clock-history text-danger me-2"></i>Post-31 Oct 2026 Autonomous Activity Simulation</h5>
                            <small class="text-secondary">Plausible daily activities generated by the 14 agents beyond the historical cutoff date.</small>
                        </div>
                        <span class="badge bg-danger">STRETCH GOAL COMPLETE</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-striped align-middle">
                            <thead>
                                <tr class="text-secondary">
                                    <th>Date</th>
                                    <th>Actor</th>
                                    <th>Activity Type</th>
                                    <th>Summary</th>
                                    <th>Full Context</th>
                                </tr>
                            </thead>
                            <tbody id="simTableBody">
                                <!-- Simulation rows loaded via JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentDay = 4;
        let selectedAgentId = "VX007"; // Priya Nair default

        function updateDay(val) {
            currentDay = parseInt(val);
            const dayLabels = {
                1: "Day 1 (Mon 16 Nov 2026) - Kickoff Drop",
                2: "Day 2 (Tue 17 Nov 2026) - HR & Attrition Drop",
                3: "Day 3 (Wed 18 Nov 2026) - Engineering & Jira Drop",
                4: "Day 4 (Thu 19 Nov 2026) - Voice Notes T6c/d Drop"
            };
            document.getElementById("dayDisplay").innerText = dayLabels[currentDay];
            loadWorries();
        }

        async function loadWorries() {
            const res = await fetch(`/api/worries?day=${currentDay}`);
            const data = await res.json();
            const container = document.getElementById("worryContainer");
            container.innerHTML = "";
            data.forEach(item => {
                const col = document.createElement("div");
                col.className = "col-md-4";
                col.innerHTML = `
                    <div class="card h-100 p-4 border-start border-4 border-danger shadow-sm">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge severity-badge-${item.severity} px-2 py-1">${item.severity}</span>
                            <span class="fw-bold text-secondary">#${item.rank}</span>
                        </div>
                        <h5 class="fw-bold mt-2 text-white">${item.title}</h5>
                        <p class="small text-light mb-3">${item.summary}</p>
                        <div class="p-2 rounded bg-black mb-3 border border-secondary">
                            <small class="text-warning fw-bold d-block mb-1"><i class="bi bi-lightning-fill me-1"></i>Action Required:</small>
                            <small class="text-light">${item.action_required}</small>
                        </div>
                        <div class="mt-auto">
                            <small class="text-secondary d-block mb-1">Evidence Records:</small>
                            <div>${item.evidence_refs.map(r => `<span class="citation-tag">${r}</span>`).join('')}</div>
                        </div>
                    </div>
                `;
                container.appendChild(col);
            });
        }

        async function submitQuery() {
            const q = document.getElementById("queryInput").value.trim();
            if (!q) return;
            const res = await fetch(`/api/query?q=${encodeURIComponent(q)}&day=${currentDay}`);
            const data = await res.json();
            
            document.getElementById("queryResult").style.display = "block";
            document.getElementById("resQuestion").innerText = `Q: "${q}"`;
            document.getElementById("resAnswer").innerText = data.answer;
            document.getElementById("resConfidence").innerText = `Confidence: ${data.confidence}`;
            document.getElementById("resDay").innerText = `As of Release Day ${data.as_of_day}`;
            
            const citDiv = document.getElementById("resCitations");
            citDiv.innerHTML = data.citations.map(c => `<span class="citation-tag text-info">${c}</span>`).join(' ');
        }

        function setQuery(text) {
            document.getElementById("queryInput").value = text;
            submitQuery();
        }

        async function loadAgents() {
            const res = await fetch("/api/agents");
            const data = await res.json();
            const list = document.getElementById("agentList");
            list.innerHTML = "";
            data.forEach(a => {
                const item = document.createElement("a");
                item.href = "javascript:void(0)";
                item.className = "list-group-item list-group-item-action bg-dark text-white border-secondary d-flex justify-content-between align-items-center py-2";
                item.innerHTML = `
                    <div>
                        <strong class="d-block text-info">${a.name}</strong>
                        <small class="text-secondary">${a.role} &bull; ${a.dept}</small>
                    </div>
                    <i class="bi bi-chevron-right text-secondary"></i>
                `;
                item.onclick = () => selectAgent(a.emp_id, a.name, a.role, a.dept);
                list.appendChild(item);
            });
            selectAgent("VX007", "Priya Nair", "Staff Engineer", "Engineering");
        }

        function selectAgent(id, name, role, dept) {
            selectedAgentId = id;
            document.getElementById("currentAgentName").innerText = name;
            document.getElementById("currentAgentRole").innerText = role;
            document.getElementById("currentAgentDept").innerText = dept;
            document.getElementById("interviewLog").innerHTML = `<div class="text-info small mb-2"><i class="bi bi-info-circle me-1"></i>You are now in a private interview with ${name}. Ask them about their role, work pressure, or company status.</div>`;
        }

        async function interviewCurrentAgent() {
            const prompt = document.getElementById("interviewInput").value.trim();
            if (!prompt) return;
            document.getElementById("interviewInput").value = "";
            
            const log = document.getElementById("interviewLog");
            log.innerHTML += `<div class="mb-2 text-end"><span class="badge bg-secondary text-wrap p-2 text-start"><strong>CEO Ananya:</strong> ${prompt}</span></div>`;
            
            const res = await fetch(`/api/interview?id=${selectedAgentId}&prompt=${encodeURIComponent(prompt)}`);
            const data = await res.json();
            
            log.innerHTML += `<div class="mb-3 text-start"><span class="badge bg-dark border border-info text-info text-wrap p-3 text-start" style="font-size: 0.95rem;"><strong>${data.name}:</strong> ${data.response}</span></div>`;
            log.scrollTop = log.scrollHeight;
        }

        async function loadSimEvents() {
            const res = await fetch("/api/simulation");
            const data = await res.json();
            const tbody = document.getElementById("simTableBody");
            tbody.innerHTML = "";
            data.forEach(e => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><span class="badge bg-secondary font-monospace">${e.event_date}</span></td>
                    <td class="text-info fw-bold">${e.actor_name}</td>
                    <td><span class="badge bg-primary text-uppercase">${e.activity_type}</span></td>
                    <td><strong>${e.summary}</strong></td>
                    <td class="small text-light">${e.details}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Initialize on load
        window.onload = () => {
            loadWorries();
            loadAgents();
            loadSimEvents();
        };
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/worries")
def get_worries():
    day = int(request.args.get("day", 4))
    return jsonify(cockpit.get_top_worries(as_of_day=day))

@app.route("/api/query")
def run_query():
    q = request.args.get("q", "")
    day = int(request.args.get("day", 4))
    return jsonify(cockpit.ask(q, as_of_day=day))

@app.route("/api/agents")
def get_agents():
    return jsonify(agent_mgr.list_agents())

@app.route("/api/interview")
def interview_agent():
    emp_id = request.args.get("id", "VX007")
    prompt = request.args.get("prompt", "")
    return jsonify(agent_mgr.interview(emp_id, prompt))

@app.route("/api/simulation")
def get_sim():
    run_simulation()
    return jsonify(get_simulated_events())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

