# AGENTIC AI STUDY & PRODUCTIVITY ASSISTANT
## Comprehensive Course-Completion Project Report

---

### [TITLE PAGE]

**PROJECT TITLE:** Agentic AI Study & Productivity Assistant  
**COURSE:** Autonomous Agentic AI Systems & Engineering  
**ACADEMIC YEAR:** 2025–2026  

| **Submitted By:** | **Under the Guidance Of:** |
|---|---|
| **Student Names:** G. Rakesh Kumar and M.Harshitha | **Mentor / Evaluator:** `[MENTOR_NAME]` |
| **Roll / Student ID:** `[STUDENT_ID]` | **Designation:** `[MENTOR_DESIGNATION]` |
| **Department:** `[DEPARTMENT_NAME]` | **Institution / Provider:** `[INSTITUTION_OR_PROVIDER]` |
| **Submission Date:** `[SUBMISSION_DATE]` | **Location:** `[CITY_COUNTRY]` |

---

### [CERTIFICATE OF COMPLETION]

This is to certify that the project entitled **"Agentic AI Study & Productivity Assistant"** submitted by **G. Rakesh Kumar and M.Harshitha** (`[STUDENT_ID]`) in partial fulfillment of the requirements for the completion of the course **Agentic AI Engineering** is a bonafide record of independent software development carried out under my supervision.

The results embodied in this report have been thoroughly evaluated, tested via automated test suites, and verified in accordance with modern agentic AI safety, planning, and orchestration benchmarks.

<br><br>
______________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ______________________________  
**Course Mentor / Instructor** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of Department / Director**  
Date: `[SUBMISSION_DATE]` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Institution Seal: `[SEAL]`

---

### [DECLARATION]

We, **G. Rakesh Kumar and M.Harshitha**, hereby declare that the project entitled **"Agentic AI Study & Productivity Assistant"** submitted to `[INSTITUTION_OR_PROVIDER]` is an original piece of software engineering and research authored by us. 

All external libraries, references, and frameworks utilized during the development of this project have been duly cited and acknowledged. This codebase contains strictly genuine algorithmic implementations, verified test outcomes, and no fabricated credentials or external results.

<br>
**Signatures of the Candidates:** ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ___________________________  
**Names:** G. Rakesh Kumar and M.Harshitha  
**Date:** `[SUBMISSION_DATE]`  

---

### [ACKNOWLEDGEMENTS]

We express our deepest gratitude to our course instructor `[MENTOR_NAME]` and the faculty of `[INSTITUTION_OR_PROVIDER]` for their indispensable guidance, technical critiques, and encouragement throughout the duration of this project.

We are also thankful to the open-source community for developing high-grade developer tools including Streamlit, Python, Pydantic, and Pytest, which enabled the construction of a robust, verifiable agentic application.

---

### [ABSTRACT]

Traditional conversational AI models often operate as passive next-token predictors, lacking goal-driven decomposition, explicit verification loops, and bounded tool execution. This report presents the **Agentic AI Study & Productivity Assistant**, an autonomous multi-agent architecture specifically engineered for academic study planning, knowledge synthesis, active recall evaluation, and task management.

The system incorporates five specialized components: a **Planner Agent** utilizing hierarchical goal decomposition; a **Knowledge and Research Agent** retrieving factual grounding from a curated local curriculum; an **Executor Agent** dispatching safe allowlisted tools (timetables, quizzes, AST-parsed arithmetic calculators); a **Critic and Verification Agent** performing post-execution consistency audits with bounded revision budgets; and a **Memory Manager** persisting user-approved task traces in a sanitized SQLite repository. 

Operating under both live configurable LLM APIs and an offline deterministic demonstration mode, the system was validated via 24 automated unit and integration tests achieving 100% pass rates. The resulting application demonstrates a production-grade, secure, and reproducible implementation of modern agentic AI engineering.

---

### [TABLE OF CONTENTS]

1. Introduction
2. Problem Statement
3. Objectives and Scope
4. Literature and Background Overview
5. Existing System vs. Proposed System
6. Requirements Analysis
7. System Architecture and Workflow
8. Specialized Agent Responsibilities
9. Algorithms and Mathematical Modeling
10. Database Design and Persistence
11. Security and Safety Guardrails
12. Testing Methodology and Actual Results
13. Limitations and Future Enhancements
14. Conclusion
15. References

---

### 1. INTRODUCTION

The evolution of artificial intelligence has transitioned rapidly from static discriminative classifiers to generative language models, and most recently, to **agentic AI systems**. While standard Large Language Models (LLMs) can produce persuasive textual answers, they struggle with sustained focus, multi-step problem solving, deterministic mathematical calculations, and self-auditing.

The **Agentic AI Study & Productivity Assistant** addresses these limitations by structuring agent behavior around the Plan-and-Solve paradigm. By separating cognitive concerns into specialized functional units, the system transforms broad user learning objectives into actionable, mathematically verified study deliverables.

---

### 2. PROBLEM STATEMENT

Modern learners and knowledge workers frequently face cognitive overload when planning complex study schedules, preparing for comprehensive examinations, or synthesizing vast syllabi. Existing digital assistants suffer from critical shortcomings:
- **Hallucinated Guidance:** Generative models often fabricate schedules with mathematically impossible daily study hours or provide inaccurate quiz answer keys.
- **Passive Interaction:** Single-turn chat interfaces require repetitive prompting and cannot self-correct or orchestrate subtasks autonomously.
- **Unchecked Tool Execution:** Arbitrary code interpreters and unsafe eval() scripts pose severe security risks to host operating systems.
- **Lack of Memory Persistence:** Conventional chat sessions reset on page refresh, discarding approved study plans and learner history.

---

### 3. OBJECTIVES AND SCOPE

#### Primary Objectives:
1. **Autonomous Planning:** Interpret user study goals and automatically formulate ordered, typed subtasks with designated agent assignments.
2. **Deterministic Calculations:** Implement safe AST-based arithmetic parsers to accurately distribute study hours, pacing, and Pomodoro intervals without arbitrary code execution.
3. **Active Recall Generation:** Automatically synthesize structured multiple-choice quizzes with verified answers and cognitive rationales.
4. **Critic Verification Loop:** Deploy an independent evaluator to audit deliverables against arithmetic, structural, and factual criteria before presentation.
5. **Dual Operation Modes:** Support both live cloud-based LLM APIs (Gemini, OpenAI, Anthropic) and a 100% offline deterministic demonstration mode.
6. **Local Persistence:** Provide secure SQLite storage for user-approved task milestones while enforcing strict key-redaction sanitizers.

#### Project Scope:
The scope encompasses local educational planning, computer science and engineering curriculum synthesis, document summarization within 4,000-character windows, and structured interactive assessment. The system is designed to operate on standard Windows workstations without requiring external cloud databases or paid subscriptions.

---

### 4. LITERATURE AND BACKGROUND OVERVIEW

The conceptual foundation of this project is informed by recent breakthroughs in agentic reasoning:
- **ReAct (Reasoning and Acting):** Yao et al. (2022) established that interleaving thought traces with tool interactions significantly reduces hallucination rates.
- **Plan-and-Solve Prompting:** Wang et al. (2023) demonstrated that generating an explicit multi-step plan prior to execution dramatically improves accuracy on multi-step reasoning tasks compared to zero-shot Chain-of-Thought.
- **Self-Refine / Critic Architectures:** Madaan et al. (2023) showed that autonomous agents equipped with iterative feedback and bounded self-critique loops achieve superior output quality.
- **Cognitive Study Science:** Principles derived from Ebbinghaus (Spaced Repetition) and Dunlosky et al. (2013) demonstrate that active retrieval testing dramatically outperforms passive reading.

---

### 5. EXISTING SYSTEM VS. PROPOSED SYSTEM

| Dimension | Existing Conversational Systems | Proposed Agentic Study Assistant |
|---|---|---|
| **Architecture** | Single monolithic LLM prompt | Modular Multi-Agent Orchestration |
| **Planning** | Implicit or absent | Explicit Pydantic-typed `TaskPlan` |
| **Math & Calculation** | Probabilistic token guessing (frequent errors) | Deterministic AST-parsed arithmetic evaluation |
| **Verification** | None (user must manually spot errors) | Automated Critic Agent with bounded retry loop |
| **Security** | Potential arbitrary code execution vulnerabilities | Strict allowlisted tool dispatch (zero eval/exec) |
| **Offline Capability** | Non-functional without active API credits | Full deterministic offline demonstration mode |
| **State Persistence** | Transient chat session buffers | Parameterized SQLite storage with API key redaction |

---

### 6. REQUIREMENTS ANALYSIS

#### Functional Requirements:
- **FR-1:** The user must be able to input learning objectives, timeframe, and study constraints.
- **FR-2:** The Planner Agent must return structured subtasks with designated agent assignments.
- **FR-3:** The Knowledge Agent must retrieve verified local curriculum documentation with explicit citations.
- **FR-4:** The Executor Agent must produce daily study timetables, practice quizzes, and document summaries.
- **FR-5:** The Critic Agent must evaluate arithmetic consistency ($Total = Days \times DailyHours$) and quiz answer integrity.
- **FR-6:** The user must be able to view real-time agent execution timelines, approved memories, and search history.

#### Non-Functional Requirements:
- **NFR-1 (Security):** Zero leakage of environment variables, passwords, or tokens in logs or databases.
- **NFR-2 (Reliability):** Automated test suite coverage with 100% test pass rates on Python 3.11+.
- **NFR-3 (Performance):** Complete multi-agent pipeline execution in less than 3 seconds in offline mode.
- **NFR-4 (Usability):** Responsive dark navy UI built with Streamlit adhering to accessibility and visual clarity.

---

### 7. SYSTEM ARCHITECTURE & WORKFLOW

The architecture coordinates five distinct agentic subsystems managed by `StudyOrchestrator`:

1. **User Request Reception:** User enters a natural language goal and optional constraints.
2. **Decomposition:** `PlannerAgent` formulates an ordered `TaskPlan` with typed subtasks.
3. **Knowledge Grounding:** `KnowledgeAgent` queries `search_local_knowledge` for domain context.
4. **Execution:** `ExecutorAgent` invokes strictly allowlisted tools.
5. **Auditing:** `CriticAgent` evaluates deliverables, checks arithmetic integrity, and triggers bounded revisions if deficiencies exist.
6. **Consolidation:** `StudyOrchestrator` generates a markdown report and renders real-time telemetry.
7. **Storage:** The user approves and saves task traces to SQLite.

---

### 8. SPECIALIZED AGENT RESPONSIBILITIES

- **Planner Agent (`agents/planner.py`):** Acts as the strategic director. Converts unstructured goals into an ordered dependency tree.
- **Knowledge Agent (`agents/knowledge_agent.py`):** Serves as the factual anchor. Retrieves local curriculum documents and ensures citations are genuine.
- **Executor Agent (`agents/executor.py`):** The operational muscle. Safely routes parameters to allowlisted utility functions.
- **Critic & Verification Agent (`agents/critic.py`):** The quality auditor. Verifies outputs against rubrics and mathematical identities.
- **Memory Manager (`memory/manager.py`):** The episodic store. Manages CRUD operations over past approved tasks using SQLite.
- **Orchestrator (`core/orchestrator.py`):** The executive coordinator. Manages timeouts, state transitions, and step callbacks.

---

### 9. ALGORITHMS AND IMPLEMENTATION DETAILS

#### Safe AST Arithmetic Parsing
To completely eliminate code injection risks, mathematical expressions are evaluated by traversing the Python Abstract Syntax Tree:

```python
# Allowed AST operators dictionary:
_ALLOWED_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow, ast.USub: operator.neg
}
```
Any AST node not matching this strict allowlist raises an immediate `ValueError`, preventing any access to `__import__`, `os`, or `eval()`.

---

### 10. DATABASE DESIGN

The SQLite schema utilizes two normalized tables:
- `task_memory`: Tracks `id`, `goal`, `summary`, `tags`, `created_at`, and `details_json`.
- `user_preferences`: Stores key-value runtime configuration settings.

All queries use parameterized placeholders (`?`), neutralizing SQL injection attacks.

---

### 11. TESTING METHODOLOGY & ACTUAL RESULTS

Testing was executed using `pytest 9.1.1` under Python 3.14.5. All 24 automated unit and integration tests passed unconditionally:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\AI-Projects\agentic-ai-study-productivity-assistant

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

### 12. LIMITATIONS

1. **Document Window Size:** Input document summarization is intentionally constrained to 4,000 characters to prevent excessive buffer allocation.
2. **Offline Knowledge Scope:** When operating in offline demonstration mode, research questions are answered strictly from the local pre-indexed curriculum.
3. **Single User Focus:** The local SQLite storage is optimized for single-user desktop deployment rather than distributed multi-tenant concurrency.

---

### 13. FUTURE ENHANCEMENTS

1. **Local Embeddings & RAG:** Integrating `sentence-transformers` and ChromaDB for semantic retrieval over user-uploaded PDF textbooks.
2. **Speech Interface:** Incorporating local Whisper models for voice-guided study questioning.
3. **Calendar Integration:** Exporting generated timetables directly to `.ics` and Google Calendar formats.

---

### 14. CONCLUSION

The **Agentic AI Study & Productivity Assistant** successfully implements the core competencies of modern agentic artificial intelligence: hierarchical planning, specialized multi-agent division of labor, safe tool dispatch, persistent memory, and closed-loop verification. By pairing live LLM capabilities with a deterministic offline demonstration fallback, the project ensures reliable, reproducible, and verifiable performance for academic evaluation.

---

### 15. REFERENCES

1. Yao, S., Zhao, J., Yu, D., et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv:2210.03629.
2. Wang, L., Xu, W., Lan, Y., et al. (2023). *Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models*. ACL 2023.
3. Madaan, A., Tandon, N., Gupta, P., et al. (2023). *Self-Refine: Iterative Refinement with Self-Feedback*. NeurIPS 2023.
4. Dunlosky, J., Rawson, K. A., Marsh, E. J., et al. (2013). *Improving Students' Learning With Effective Learning Techniques*. Psychological Science in the Public Interest, 14(1), 4-58.
5. Pydantic Documentation. (2024). *Data validation and settings management using Python type annotations*. https://docs.pydantic.dev/
6. Streamlit Documentation. (2024). *A faster way to build and share data apps*. https://docs.streamlit.io/
