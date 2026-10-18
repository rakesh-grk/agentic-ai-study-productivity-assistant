# System Architecture & Technical Specification

## Agentic AI Study & Productivity Assistant

### 1. Architectural Philosophy
The system is designed around the principles of **modular agent autonomy**, **bounded plan-and-solve execution**, **strict tool safety**, and **closed-loop verification**. Unlike single-prompt conversational bots, it divides complex user intentions into formal subtasks and dispatches them across specialized autonomous roles.

---

### 2. End-to-End Workflow Diagram

```mermaid
flowchart TD
    User([User Goal & Constraints]) --> Orch[Study Orchestrator]
    
    subgraph Planning Phase
        Orch --> Planner[Planner Agent]
        Planner -->|Goal Decomposition| PlanObj[(Structured TaskPlan)]
    end
    
    subgraph Knowledge & Execution Phase
        PlanObj --> KA[Knowledge & Research Agent]
        KA -->|Local Curriculum Query| KB[(Local Knowledge Base)]
        KB -->|Attributed Excerpts| KA
        
        PlanObj --> Exec[Executor Agent]
        Exec --> Tools{Safe Allowlisted Tools}
        Tools --> T1[generate_study_timetable]
        Tools --> T2[generate_practice_quiz]
        Tools --> T3[calculate_study_schedule]
        Tools --> T4[generate_topic_summary]
        Tools --> T5[safe_calculate]
        Tools --> T6[summarize_text_document]
    end
    
    subgraph Critique & Verification Loop
        KA --> Critic[Critic & Verification Agent]
        Exec --> Critic
        Critic -->|Arithmetic Audit & Completeness Check| Eval[(CriticEvaluation)]
        Eval -.->|Revision Requested (Budget <= 2)| Exec
    end
    
    subgraph Persistence & User Interface
        Eval -->|Validated Result| Orch
        Orch --> FinalReport[Consolidated Final Deliverable]
        FinalReport --> StreamlitUI([Streamlit Dashboard UI])
        StreamlitUI -.->|User Approval| SQLiteDB[(Persistent SQLite Memory)]
    end
```

---

### 3. Agent Responsibilities & Protocols

| Agent Name | Primary Responsibility | Input Protocol | Output Deliverable | Guardrails & Constraints |
|---|---|---|---|---|
| **Planner Agent** | Interprets intentions, extracts constraints, generates ordered subtasks. | Natural language goal + constraint strings. | `TaskPlan` (Pydantic model with typed subtasks). | Bounded subtask count (3–5); assigned agent verification. |
| **Knowledge Agent** | Retrieves factual grounding from curated local curriculum. | Search query string. | Structured findings with source attribution. | Zero live external scraping; transparent disclaimer. |
| **Executor Agent** | Dispatches allowlisted tools for timetables, quizzes, calculations, summaries. | Tool name + strictly typed parameter dict. | Typed JSON result structure. | Strict allowlist; no `eval()`, no shell executions. |
| **Critic Agent** | Audits outputs for math consistency, completeness, and structure. | Full plan, subtask deliverables, tool outputs. | `CriticEvaluation` (score, checks passed, deficiencies). | Bounded revision ceiling (`MAX_REVISIONS = 2`). |
| **Memory Manager** | Retains approved task summaries and preferences. | Approved goal, summary, metadata dict. | SQLite row ID. | Parameterized queries (`?`); auto-redacts API keys. |
| **Orchestrator** | Coordinates agent lifecycle, tracks execution timelines, catches faults. | User goal and runtime flags. | `OrchestrationResult`. | Safe execution timeout handling; fallback to offline demo. |

---

### 4. Database Schema (SQLite)

```sql
CREATE TABLE IF NOT EXISTS task_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT NOT NULL,
    summary TEXT NOT NULL,
    tags TEXT NOT NULL,
    created_at TEXT NOT NULL,
    details_json TEXT
);

CREATE TABLE IF NOT EXISTS user_preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

---

### 5. Mathematical Pacing & Validation Algorithms

#### A. Study Pacing Formula
$$\text{Daily Target (hrs)} = \frac{\text{Total Study Hours}}{\text{Available Days}}$$
$$\text{Daily Pomodoro Blocks} = \max\left(1, \text{round}\left(\frac{\text{Daily Minutes}}{\text{Pomodoro Length} + \text{Break Length}}\right)\right)$$

#### B. Verification Consistency Equation
The Critic agent asserts that:
$$\left| \text{Total Study Hours} - (\text{Available Days} \times \text{Hours Per Day}) \right| \le 0.05$$
Any violation triggers an immediate `Calculation Inconsistency` deficiency flag.
