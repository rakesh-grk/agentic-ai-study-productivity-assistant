import streamlit as st
import time
import json
from pathlib import Path
from core.configuration import AppConfig
from core.orchestrator import StudyOrchestrator
from core.models import AgentStepRecord
from memory.manager import MemoryManager
from tools.calculator import safe_calculate, calculate_study_schedule
from tools.study_tools import (
    generate_study_timetable,
    generate_topic_summary,
    generate_practice_quiz,
    summarize_text_document
)

# Page configuration
st.set_page_config(
    page_title="Agentic AI Study & Productivity Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Navy & Blue Design System
st.markdown("""
<style>
    /* Primary Color Palette: Deep Navy & Electric Azure */
    :root {
        --bg-navy: #09111e;
        --card-navy: #111e33;
        --accent-blue: #0077b6;
        --bright-azure: #00b4d8;
        --text-light: #f0f4f8;
        --border-color: #1e355b;
    }
    
    .stApp {
        background-color: var(--bg-navy);
        color: var(--text-light);
    }
    
    .main-header {
        background: linear-gradient(135deg, #0b1a30 0%, #003060 50%, #005082 100%);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #1e3d6b;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    
    .main-header p {
        color: #90e0ef;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    
    .metric-card {
        background: #112240;
        padding: 16px;
        border-radius: 8px;
        border-left: 4px solid #00b4d8;
        margin-bottom: 12px;
    }
    
    .step-box {
        background: #0f1c30;
        border: 1px solid #1a3356;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    
    .step-box.error {
        border-left: 4px solid #e63946;
    }
    
    .step-box.success {
        border-left: 4px solid #2a9d8f;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #0077b6 0%, #0096c7 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #0096c7 0%, #00b4d8 100%);
        box-shadow: 0 0 12px rgba(0, 180, 216, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Initialize persistent memory manager
memory = MemoryManager()

# Sidebar: System Status & Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("System Control")
    
    st.markdown("### ⚙️ Mode Settings")
    force_offline = st.toggle("Force Offline Demo Mode", value=True, help="Disable live LLM calls and demonstrate deterministic multi-agent behavior without requiring API credits.")
    
    provider = st.selectbox(
        "Preferred LLM Provider",
        options=["gemini", "openai", "anthropic"],
        index=0,
        help="Select which LLM provider to use when Offline Mode is disabled."
    )
    
    is_configured = AppConfig.is_api_configured(provider)
    if force_offline:
        st.info("ℹ️ **Active Mode:** Deterministic Offline Demo\n(All agents, tools, memory, and verification operate locally without API tokens).")
    elif is_configured:
        st.success(f"✅ **{provider.upper()} API Key Configured**\n`{AppConfig.get_masked_key(provider)}`")
    else:
        st.warning(f"⚠️ **{provider.upper()} Key Not Set**\nAdd to `.env` or run in Offline Demo Mode.")
        
    st.markdown("---")
    st.markdown("### 📊 System Metadata")
    st.write(f"**Max Revisions:** {AppConfig.MAX_REVISION_ATTEMPTS}")
    st.write(f"**Database:** SQLite (`{AppConfig.DB_PATH.name}`)")
    st.write(f"**Memory Records:** {len(memory.get_all_memories())}")

# Main Header Banner
st.markdown("""
<div class="main-header">
    <h1>🎓 Agentic AI Study & Productivity Assistant</h1>
    <p>A course-completion autonomous multi-agent system featuring Planning, Local Knowledge Retrieval, Tool Calling, Persistent Memory, and Critic Verification.</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_assistant, tab_memory, tab_tools, tab_docs = st.tabs([
    "🚀 Assistant Dashboard",
    "🧠 Approved Task Memory",
    "🛠️ Direct Tool Sandbox",
    "📖 Architecture & Docs"
])

# ----------------- TAB 1: ASSISTANT DASHBOARD -----------------
with tab_assistant:
    st.subheader("🎯 Goal Formulation & Agent Task Execution")
    
    # Example task shortcuts
    st.markdown("**Quick Examples (Click to populate):**")
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    selected_goal = ""
    if col_ex1.button("📅 7-Day Timetable: Agentic AI"):
        selected_goal = "Create a 7-day intensive study timetable for Agentic AI Architecture with 3 hours daily."
    if col_ex2.button("🧠 Quiz: Python & Algorithms"):
        selected_goal = "Generate an active recall practice quiz on Python data structures and Big-O complexity."
    if col_ex3.button("📖 Review: Machine Learning"):
        selected_goal = "Synthesize a structured revision summary and active recall quiz on Machine Learning Model Evaluation."
        
    goal_input = st.text_area(
        "Enter your study goal or learning objective:",
        value=selected_goal if selected_goal else st.session_state.get("goal_input_val", ""),
        placeholder="e.g. Create a 5-day study schedule for Deep Learning Optimization with 2 hours per day...",
        height=100,
        key="main_goal_area"
    )
    
    constraints_input = st.text_input(
        "Optional Constraints (comma-separated):",
        placeholder="e.g. Maximum 3 hours/day, include active recall checkpoints, incorporate Pomodoro breaks",
        key="constraints_input_key"
    )
    
    col_run, col_clear = st.columns([1, 5])
    run_clicked = col_run.button("🚀 Run Multi-Agent Plan", type="primary")

    if run_clicked:
        if not goal_input.strip():
            st.error("Please enter a valid study goal.")
        else:
            constraints = [c.strip() for c in constraints_input.split(",") if c.strip()]
            orchestrator = StudyOrchestrator(force_offline=force_offline)
            
            progress_bar = st.progress(0, text="Initializing Multi-Agent Workflow...")
            status_container = st.container()
            
            # Step callback to render real-time timeline
            timeline_ph = st.empty()
            steps_log = []
            
            def on_step(record: AgentStepRecord):
                steps_log.append(record)
                with timeline_ph.container():
                    st.markdown("#### ⏱️ Real-Time Agent Execution Timeline")
                    for s in steps_log:
                        icon = "❌" if s.is_error else "🤖" if "Agent" in s.agent_name else "⚙️"
                        color_cls = "error" if s.is_error else "success"
                        st.markdown(
                            f"<div class='step-box {color_cls}'>"
                            f"<strong>{icon} Step {s.step_number} [{s.agent_name}]</strong> — <em>{s.action}</em> ({s.duration_seconds}s)<br>"
                            f"<small>{s.details}</small>"
                            f"</div>",
                            unsafe_allow_html=True
                        )

            progress_bar.progress(25, text="Formulating Plan & Querying Knowledge Base...")
            res = orchestrator.run(goal_input, constraints, on_step_callback=on_step)
            progress_bar.progress(100, text="Workflow Concluded & Verified!")
            
            st.session_state["latest_result"] = res

    # Display Results if available
    if "latest_result" in st.session_state:
        res = st.session_state["latest_result"]
        st.markdown("---")
        
        # Metric Bar
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Execution Time", f"{res.execution_time_seconds}s")
        with col_m2:
            st.metric("Subtasks Executed", len(res.plan.subtasks) if res.plan else 0)
        with col_m3:
            st.metric("Verification Score", f"{int((res.verification.score if res.verification else 0) * 100)}%")
        with col_m4:
            st.metric("Status", "Verified ✅" if res.success else "Flagged ⚠️")
            
        # Tabbed Deliverable View
        tab_report, tab_plan, tab_audit, tab_save = st.tabs([
            "📄 Consolidated Final Deliverable",
            "📋 Subtask Plan Details",
            "🔍 Critic Verification Audit",
            "💾 Save to Approved Memory"
        ])
        
        with tab_report:
            st.markdown(res.final_output)
            
        with tab_plan:
            if res.plan:
                st.write(f"**Target Outcome:** {res.plan.target_outcome}")
                st.write(f"**Identified Constraints:** {', '.join(res.plan.constraints) if res.plan.constraints else 'None'}")
                st.markdown("### Ordered Subtasks")
                for st_item in res.plan.subtasks:
                    st.markdown(f"- **Subtask #{st_item.id}: {st_item.title}**")
                    st.write(f"  - **Assigned:** `{st_item.assigned_agent}` | **Tool:** `{st_item.tool_required or 'None'}` | **Status:** `{st_item.status}`")
                    st.write(f"  - *Description:* {st_item.description}")
                    
        with tab_audit:
            if res.verification:
                v = res.verification
                st.markdown(f"### Critic Audit Score: **{int(v.score * 100)}%**")
                st.info(v.critique_notes)
                st.markdown("**Checks Passed:**")
                for cp in v.checks_passed:
                    st.success(f"✓ {cp}")
                if v.deficiencies:
                    st.markdown("**Deficiencies Identified:**")
                    for df in v.deficiencies:
                        st.warning(f"⚠️ {df}")
                        
        with tab_save:
            st.write("Persist this verified task output to the local SQLite knowledge store for multi-turn session recall.")
            summary_tag = st.selectbox("Category Tag", ["study_schedule", "quiz_set", "concept_summary", "general"], index=0)
            if st.button("💾 Approve & Save Task to Memory"):
                mem_id = memory.save_task_memory(
                    goal=res.goal,
                    summary=f"Task #{res.task_id}: {res.goal[:80]}... Score: {int(res.verification.score * 100)}%",
                    tags=summary_tag,
                    details={"task_id": res.task_id, "score": res.verification.score, "mode": res.mode}
                )
                st.success(f"Saved to memory with Record ID #{mem_id}!")

# ----------------- TAB 2: APPROVED TASK MEMORY -----------------
with tab_memory:
    st.subheader("🧠 Local Persistent Task Memory (SQLite)")
    st.markdown("All task summaries stored here have been explicitly approved by the user. No API keys or passwords are ever saved.")
    
    col_search, col_clear_all = st.columns([3, 1])
    search_q = col_search.text_input("Search past tasks:", placeholder="Type keywords...")
    if col_clear_all.button("🗑️ Clear Entire History", help="Permanently delete all stored memories"):
        memory.clear_all_memories()
        st.success("All task memories cleared.")
        
    records = memory.search_memories(search_q) if search_q else memory.get_all_memories()
    
    if not records:
        st.info("No task memory records found.")
    else:
        st.write(f"Showing **{len(records)}** stored record(s):")
        for rec in records:
            with st.expander(f"📌 [ID #{rec.id}] {rec.created_at} — {rec.goal[:60]}..."):
                st.write(f"**Goal:** {rec.goal}")
                st.write(f"**Summary:** {rec.summary}")
                st.write(f"**Category Tag:** `{rec.tags}`")
                if rec.details_json:
                    st.json(rec.details_json)
                if st.button(f"Delete Record #{rec.id}", key=f"del_mem_{rec.id}"):
                    memory.delete_memory(rec.id)
                    st.rerun()

# ----------------- TAB 3: DIRECT TOOL SANDBOX -----------------
with tab_tools:
    st.subheader("🛠️ Allowlisted Tool Direct Sandbox")
    st.markdown("Directly evaluate any individual tool with custom arguments to verify its output format and error handling.")
    
    tool_choice = st.selectbox(
        "Select Tool to Test:",
        [
            "Study Schedule Pacing Calculator",
            "Personalized Study Timetable Generator",
            "Active Recall Practice Quiz Generator",
            "Concept Topic Summary Breakdown",
            "Safe Arithmetic Calculator",
            "Safe Document Text Summarizer"
        ]
    )
    
    if tool_choice == "Study Schedule Pacing Calculator":
        c1, c2, c3 = st.columns(3)
        hours = c1.number_input("Total Target Study Hours:", min_value=1.0, value=25.0, step=1.0)
        days = c2.number_input("Available Days:", min_value=1, value=7, step=1)
        pomo = c3.number_input("Pomodoro Length (min):", min_value=15, value=25, step=5)
        if st.button("Calculate Pacing"):
            res = calculate_study_schedule(hours, int(days), int(pomo))
            st.json(res)
            
    elif tool_choice == "Personalized Study Timetable Generator":
        sub = st.text_input("Subject / Topic:", value="Deep Learning & Neural Networks")
        c1, c2 = st.columns(2)
        td = c1.number_input("Total Days:", min_value=1, value=5, step=1)
        hpd = c2.number_input("Hours Per Day:", min_value=0.5, value=3.0, step=0.5)
        if st.button("Generate Timetable"):
            res = generate_study_timetable(sub, int(td), float(hpd))
            st.json(res)

    elif tool_choice == "Active Recall Practice Quiz Generator":
        q_topic = st.text_input("Quiz Topic:", value="Agentic AI Multi-Agent Orchestration")
        num_q = st.slider("Number of Questions:", min_value=1, max_value=5, value=3)
        if st.button("Generate Practice Quiz"):
            res = generate_practice_quiz(q_topic, num_q)
            st.json(res)

    elif tool_choice == "Concept Topic Summary Breakdown":
        sum_topic = st.text_input("Topic to Summarize:", value="Spaced Repetition Cognitive Mechanisms")
        if st.button("Generate Summary"):
            res = generate_topic_summary(sum_topic)
            st.json(res)

    elif tool_choice == "Safe Arithmetic Calculator":
        math_expr = st.text_input("Enter Math Expression:", value="(40 / 7) * 2.5 + 15")
        if st.button("Compute Safely (AST Parser)"):
            res = safe_calculate(math_expr)
            st.json(res)

    elif tool_choice == "Safe Document Text Summarizer":
        doc_text = st.text_area("Paste Text Content (Max 4,000 characters):", height=150)
        if st.button("Summarize Document"):
            res = summarize_text_document(doc_text)
            st.json(res)

# ----------------- TAB 4: ARCHITECTURE & DOCS -----------------
with tab_docs:
    st.subheader("📖 System Architecture & Course Documentation")
    
    st.markdown("""
    ### 🏛️ Multi-Agent Architecture
    
    This application utilizes an autonomous multi-agent design:
    
    ```mermaid
    graph TD
        User([User Input: Goal & Constraints]) --> Orch[Study Orchestrator]
        Orch --> Planner[Planner Agent]
        Planner -->|Generates TaskPlan| Orch
        
        Orch -->|Queries Knowledge| KA[Knowledge & Research Agent]
        KA -->|Local Verified Curriculum| KB[(Local Knowledge Base)]
        
        Orch -->|Dispatches Subtasks| Exec[Executor Agent]
        Exec --> Tools{Allowlisted Tools}
        Tools --> T1[Study Timetable Generator]
        Tools --> T2[Active Recall Quiz Maker]
        Tools --> T3[Safe Pacing Calculator]
        Tools --> T4[Doc Summarizer]
        
        Orch -->|Audits Outputs| Critic[Critic & Verification Agent]
        Critic -->|Evaluates Checks & Calculations| Critic
        Critic -.->|Bounded Revision Loop| Exec
        
        Orch -->|Stores Approved Task| Mem[(Persistent SQLite Memory)]
        Orch --> UI([Final Consolidated Report])
    ```
    
    ### 🛡️ Security & Reliability Guardrails
    1. **Strict Tool Allowlist**: LLMs and user inputs can never execute arbitrary shell commands or code.
    2. **AST Math Parser**: Evaluates mathematical formulas via Python AST nodes rather than `eval()`.
    3. **SQL Injection Prevention**: All SQLite queries use parameterized placeholders (`?`).
    4. **Credential Isolation**: API keys are loaded via environment variables and masked in all UI elements.
    5. **Bounded Revisions**: The Critic Agent enforces a maximum retry count to prevent infinite loops.
    """)
