# Agentic AI Study & Productivity Assistant

> **A course-completion project demonstrating agentic AI planning, specialized agents, tool calling, memory, task execution, and result verification.**

---

## 🎯 Project Overview & Goals

The **Agentic AI Study & Productivity Assistant** is an autonomous multi-agent system designed to assist students and knowledge workers in synthesizing study materials, generating structured learning roadmaps, tracking progress, and accelerating task execution. 

Rather than acting as a standard conversational chatbot, this system implements end-to-end agentic workflows:
1. **Goal Formulation & Planning**: Decomposing complex study goals or projects into directed acyclic graphs (DAGs) of executable subtasks.
2. **Specialized Agent Delegation**: Routing discrete subtasks to specialized subagents (e.g., Curriculum Planner, Note Synthesizer, Flashcard & Quiz Generator, Code Verifier).
3. **Tool Calling & Execution**: Dynamically invoking external APIs, vector databases, file parsers, and web scrapers.
4. **Episodic & Semantic Memory**: Maintaining contextual recall across sessions using vector indexing and structured relational storage.
5. **Critique & Result Verification**: Self-evaluating generated content and task outcomes before returning final results to the user.

---

## 🚀 Planned Features

- **Autonomous Study Planner Agent**: Breaks large syllabi, textbooks, or research topics into modular, step-by-step study schedules.
- **Synthesizer & Knowledge Extraction Agent**: Extracts key concepts, summaries, formulas, and actionable takeaways from PDFs, markdown notes, and lectures.
- **Active Recall & Quiz Generator**: Automatically creates spaced repetition flashcards and self-assessment quizzes with automated grading and explanations.
- **Productivity & Task Tracker**: Manages task states (Pending, In-Progress, Blocked, Done) with automated milestone validation.
- **Multi-Turn Memory & State Persistence**: Retains user progress, mastery levels, and preferences across study sessions.
- **Verification & Self-Correction Loop**: Ensures generated answers, citations, and summaries are factually consistent with source materials.

---

## 🛠️ Technology Stack

- **Language & Runtime**: Python 3.11+
- **Agent Framework**: LangChain / LangGraph / Custom Agent Orchestration
- **LLM Foundation Models**: Gemini / OpenAI / Anthropic APIs (configurable)
- **Vector Database & Embeddings**: ChromaDB / FAISS for semantic document search
- **Metadata & State Store**: SQLite / Pydantic models for structured state persistence
- **Validation & Environment**: `pydantic-settings`, `pytest` for unit & agentic integration testing
- **Interface / CLI**: Rich CLI / Streamlit or FastAPI web dashboard

---

## 🗺️ Development Roadmap

- [x] **Phase 0: Workspace Initialization & Environment Setup**
  - [x] Dedicated project folder structure
  - [x] Python-focused `.gitignore` and `.env.example`
  - [x] Initial documentation and baseline Git repository setup
- [ ] **Phase 1: Architecture & Data Schemas**
  - [ ] Define core Agent state representations (Pydantic models)
  - [ ] Tool registry and abstract agent interfaces
- [ ] **Phase 2: Core Agent Capabilities & Tool Integration**
  - [ ] Document ingestion and text chunking pipeline
  - [ ] Vector database indexing and retrieval tools
  - [ ] Planner and Task Execution engine
- [ ] **Phase 3: Multi-Agent Orchestration & Memory**
  - [ ] Supervisor / Orchestrator agent implementation
  - [ ] Feedback loops and validation checks
  - [ ] Short-term and long-term memory integration
- [ ] **Phase 4: User Interface & Verification**
  - [ ] Interactive CLI / Web dashboard
  - [ ] End-to-end evaluation suite and benchmark test cases
- [ ] **Phase 5: Course Completion Documentation & Demo**
  - [ ] Architecture diagrams, recorded demonstrations, and final submission report

---

## 🔒 Security & Best Practices

- Secret keys, API tokens, and local cache data are excluded via `.gitignore`.
- All credentials should be provided through a local `.env` file based on `.env.example`.
- Source code and agent executions are isolated within this dedicated repository.
