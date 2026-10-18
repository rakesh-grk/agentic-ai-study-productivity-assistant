# Agentic AI Study & Productivity Assistant

> **An Autonomous Multi-Agent System with Planning, Local Knowledge Retrieval, Safe Tool Calling, Persistent Memory, and Critic Verification.**  
> *Course-Completion Project in Agentic AI Engineering*  
> **Candidates / Developers:** G. Rakesh Kumar and M.Harshitha

---

## 📌 Executive Overview

The **Agentic AI Study & Productivity Assistant** is an autonomous multi-agent platform engineered to transform high-level learning goals into verified, mathematically consistent study schedules, active recall quizzes, topic summaries, and assignment milestones.

Unlike conventional conversational chatbots that merely predict text without validation, this assistant incorporates:
- **Hierarchical Goal Planning:** Decomposing user requests into ordered, typed subtasks (`TaskPlan`).
- **Grounding Without Hallucination:** Querying local curriculum documents with explicit source attribution.
- **Safe Allowlisted Tool Calling:** Preventing arbitrary code execution through an AST-based arithmetic parser.
- **Closed-Loop Critic Auditing:** Evaluating arithmetic consistency ($Total = Days \times DailyHours$), quiz structures, and triggering bounded revisions.
- **Persistent Episodic Memory:** Local SQLite repository with automated API key redaction.
- **Dual Operating Modes:** Cloud LLMs (Gemini, OpenAI, Anthropic) or 100% offline deterministic demonstration.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    User([User: Goal & Constraints]) --> Orch[Study Orchestrator]
    
    subgraph Planning Phase
        Orch --> Planner[Planner Agent]
        Planner -->|Decomposes Intent| PlanObj[(Structured TaskPlan)]
    end
    
    subgraph Knowledge & Execution Phase
        PlanObj --> KA[Knowledge & Research Agent]
        KA -->|Local Curriculum Query| KB[(Local Knowledge Base)]
        KB -->|Attributed Excerpts| KA
        
        PlanObj --> Exec[Executor Agent]
        Exec --> Tools{Safe Allowlisted Tools}
        Tools --> T1[Study Timetable Generator]
        Tools --> T2[Active Recall Quiz Maker]
        Tools --> T3[Safe AST Calculator]
        Tools --> T4[Doc Summarizer]
    end
    
    subgraph Verification & Memory Loop
        KA --> Critic[Critic & Verification Agent]
        Exec --> Critic
        Critic -->|Math & Structure Audit| Eval[(Critic Evaluation)]
        Eval -.->|Revision Requested (Budget <= 2)| Exec
        Eval --> Orch
        Orch --> SQLiteDB[(Persistent SQLite Memory)]
        Orch --> UI([Streamlit Dashboard UI])
    end
```

---

## 🤖 Specialized Agent Matrix

| Agent | Module | Primary Responsibility | Guardrails & Safety |
|---|---|---|---|
| **Planner Agent** | `agents/planner.py` | Interprets user goals, extracts constraints, formulates subtasks. | Bounded subtasks (3–5); assigned agent verification. |
| **Knowledge Agent** | `agents/knowledge_agent.py` | Retrieves verified local curriculum snippets with attribution. | Zero live web scraping; transparent disclaimers. |
| **Executor Agent** | `agents/executor.py` | Dispatches allowlisted tools for timetables, quizzes, calculations. | Strict allowlist; no `eval()` or arbitrary shell commands. |
| **Critic Agent** | `agents/critic.py` | Audits math consistency, quiz options, and output completeness. | Bounded revision loop (max 2 attempts); transparent deficiency flags. |
| **Memory Manager** | `memory/manager.py` | CRUD operations for approved tasks & user preferences. | Parameterized SQLite queries (`?`); auto-redacts API keys. |
| **Orchestrator** | `core/orchestrator.py` | End-to-end lifecycle, step telemetry callbacks, report generation. | Timeout handling; fallback to offline demo. |

---

## ⚙️ Prerequisites & Installation (Windows)

### 1. Prerequisites
- **Operating System:** Windows 10 or 11 (64-bit)
- **Python:** Version 3.11, 3.12, 3.13, or 3.14 (Verified on Python 3.14.5)
- **Git:** Git for Windows (Verified on Git 2.55.0)

### 2. Setup Virtual Environment
Open PowerShell and navigate to the project directory:

```powershell
# Navigate to workspace
cd D:\AI-Projects\agentic-ai-study-productivity-assistant

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Copy the example template to create your `.env` file:

```powershell
copy .env.example .env
```

Edit `.env` if you wish to use live LLMs (Optional — **Offline Demonstration Mode runs out of the box with zero API keys**):

```ini
# LLM Provider: "gemini", "openai", or "anthropic"
LLM_PROVIDER=gemini

# Provider API Keys (Leave blank to use Offline Demo Mode)
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Model Names
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Safety Settings
MAX_REVISION_ATTEMPTS=2
```

---

## 🚀 Running the Application

Launch the Streamlit web dashboard:

```powershell
streamlit run app.py
```
*The browser will open automatically at `http://localhost:8501`.*

### Application Features:
1. **Interactive Dashboard:** Input study goals, run plans, and inspect real-time agent execution timelines.
2. **Approved Task Memory:** View, search, and delete approved study plans stored in local SQLite.
3. **Direct Tool Sandbox:** Independently test the Pacing Calculator, Timetable Generator, and Quiz Maker.
4. **Architecture & Documentation:** Full course specifications, security guardrails, and system limits.

---

## 🧪 Running Automated Tests

Run the full automated test suite using `pytest`:

```powershell
pytest -v
```

### Actual Verified Test Results (24/24 Passed):
```text
tests/test_critic.py::test_critic_all_passed PASSED                      [  4%]
tests/test_critic.py::test_critic_catches_calculation_inconsistency PASSED [  8%]
tests/test_critic.py::test_critic_catches_tool_failures PASSED           [ 12%]
tests/test_memory.py::test_save_and_retrieve_memory PASSED               [ 16%]
tests/test_memory.py::test_search_memory PASSED                          [ 20%]
tests/test_memory.py::test_delete_memory PASSED                          [ 25%]
tests/test_memory.py::test_memory_sanitizes_api_keys PASSED              [ 29%]
tests/test_memory.py::test_preferences_persistence PASSED                [ 33%]
tests/test_orchestrator.py::test_orchestrator_offline_mode_success PASSED [ 37%]
tests/test_orchestrator.py::test_orchestrator_quiz_workflow PASSED       [ 41%]
tests/test_orchestrator.py::test_orchestrator_empty_input PASSED         [ 45%]
tests/test_orchestrator.py::test_orchestrator_step_callback PASSED       [ 50%]
tests/test_planner.py::test_planner_basic_goal PASSED                    [ 54%]
tests/test_planner.py::test_planner_quiz_goal PASSED                     [ 58%]
tests/test_planner.py::test_planner_empty_goal PASSED                    [ 62%]
tests/test_planner.py::test_planner_preserves_constraints PASSED         [ 66%]
tests/test_tools.py::test_generate_study_timetable_valid PASSED          [ 70%]
tests/test_tools.py::test_generate_study_timetable_invalid_inputs PASSED [ 75%]
tests/test_tools.py::test_generate_practice_quiz_structure PASSED        [ 79%]
tests/test_tools.py::test_safe_calculate_arithmetic PASSED               [ 83%]
tests/test_tools.py::test_safe_calculate_zero_division PASSED            [ 87%]
tests/test_tools.py::test_safe_calculate_blocks_code_execution PASSED    [ 91%]
tests/test_tools.py::test_calculate_study_schedule_valid PASSED          [ 95%]
tests/test_tools.py::test_summarize_text_document_validation PASSED      [100%]

============================= 24 passed in 1.54s ==============================
```

---

## 📂 Academic Submission Materials

- **Project Report (Markdown):** [`docs/project_report.md`](file:///D:/AI-Projects/agentic-ai-study-productivity-assistant/docs/project_report.md)
- **Technical Architecture Document:** [`docs/architecture.md`](file:///D:/AI-Projects/agentic-ai-study-productivity-assistant/docs/architecture.md)
- **Viva Voce Preparation (20+ Q&A):** [`docs/viva_questions.md`](file:///D:/AI-Projects/agentic-ai-study-productivity-assistant/docs/viva_questions.md)
- **Word Document (.docx):** `artifacts/project_report.docx`
- **PowerPoint Presentation (.pptx):** `artifacts/project_presentation.pptx`

*Project Team Members & Roll Numbers:*
- **G. Rakesh Kumar** — Roll No: `[ROLL_NO_1]`
- **M. Harshitha** — Roll No: `[ROLL_NO_2]`
- **Team Member 3** — Roll No: `[ROLL_NO_3]`
- **Team Member 4** — Roll No: `[ROLL_NO_4]`
- **Team Member 5** — Roll No: `[ROLL_NO_5]`

---

## 🔒 Security & Privacy Guarantees

1. **Zero Secret Leakage:** The local SQLite database automatically redacts API keys matching `sk-...` or Google API tokens.
2. **SQL Injection Defense:** All queries use parameterized statements (`?`).
3. **No Arbitrary Code Execution:** The calculator tool uses Abstract Syntax Tree (`ast`) evaluation. Malicious code such as `__import__('os').system()` is blocked.
4. **Isolated Workstation Operation:** Operates completely within `D:\AI-Projects\agentic-ai-study-productivity-assistant` without modifying other projects or operating system settings.

---

## 📄 License & Academic Integrity

This project is created for academic course-completion evaluation. The implementation is original, with all external dependencies cited and verifiable through automated tests.
