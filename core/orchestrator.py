import time
import uuid
import json
from typing import List, Dict, Any, Optional, Callable
from core.models import (
    TaskPlan,
    SubTask,
    AgentStepRecord,
    CriticEvaluation,
    OrchestrationResult
)
from core.configuration import AppConfig
from core.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.executor import ExecutorAgent
from agents.critic import CriticAgent
from memory.manager import MemoryManager

class StudyOrchestrator:
    """Master multi-agent orchestrator that coordinates specialized agents,

    tracks execution traces, verifies deliverables, and produces consolidated reports.
    """
    
    def __init__(self, force_offline: bool = False):
        self.force_offline = force_offline
        self.llm = LLMClient(force_offline=force_offline)
        self.planner = PlannerAgent(self.llm)
        self.knowledge_agent = KnowledgeAgent(self.llm)
        self.executor = ExecutorAgent()
        self.critic = CriticAgent()
        self.memory = MemoryManager()

    def run(
        self,
        goal: str,
        constraints: Optional[List[str]] = None,
        on_step_callback: Optional[Callable[[AgentStepRecord], None]] = None
    ) -> OrchestrationResult:
        """Executes the complete end-to-end multi-agent workflow."""
        start_time = time.time()
        task_id = str(uuid.uuid4())[:8]
        steps: List[AgentStepRecord] = []
        tool_calls: List[Dict[str, Any]] = []
        subtask_results: List[Dict[str, Any]] = []

        def log_step(agent: str, action: str, details: str, duration: float = 0.0, is_err: bool = False):
            record = AgentStepRecord(
                step_number=len(steps) + 1,
                agent_name=agent,
                action=action,
                details=details,
                duration_seconds=round(duration, 3),
                is_error=is_err
            )
            steps.append(record)
            if on_step_callback:
                on_step_callback(record)

        # 1. Input Validation
        cleaned_goal = goal.strip()
        if not cleaned_goal:
            return OrchestrationResult(
                task_id=task_id,
                goal=goal,
                mode="Offline Demo" if self.llm.is_offline else "LLM",
                final_output="Error: Please enter a valid, non-empty study goal.",
                success=False,
                error_message="Empty study goal provided."
            )
        if len(cleaned_goal) > AppConfig.MAX_INPUT_LENGTH:
            return OrchestrationResult(
                task_id=task_id,
                goal=goal[:100] + "...",
                mode="Offline Demo" if self.llm.is_offline else "LLM",
                final_output=f"Error: Input exceeds maximum allowed length of {AppConfig.MAX_INPUT_LENGTH} characters.",
                success=False,
                error_message="Input too long."
            )

        active_mode = "Offline Demo (Deterministic)" if self.llm.is_offline else f"Live LLM ({self.llm.provider.upper()})"
        log_step("Orchestrator", "Task Initialization", f"Task ID #{task_id} registered. Mode: {active_mode}.")

        # 2. Planning Phase
        t0 = time.time()
        plan: TaskPlan = self.planner.plan(cleaned_goal, constraints)
        log_step(
            "Planner Agent",
            "Plan Formulation",
            f"Created plan with {len(plan.subtasks)} subtasks. Required agents: {', '.join(plan.required_agents)}.",
            duration=time.time() - t0
        )

        # 3. Execution Phase
        for subtask in plan.subtasks:
            t_sub = time.time()
            subtask.status = "in_progress"
            
            # Subtask routed to Knowledge Agent
            if "Knowledge" in subtask.assigned_agent:
                query = subtask.input_parameters.get("query", cleaned_goal)
                research_res = self.knowledge_agent.research(query)
                subtask.status = "completed"
                subtask.result = research_res.get("findings", "")
                subtask_results.append({"subtask_id": subtask.id, "type": "research", "data": research_res})
                log_step(
                    subtask.assigned_agent,
                    f"Subtask #{subtask.id}: Research Query",
                    f"Retrieved {len(research_res.get('sources', []))} reference source(s) for '{query}'.",
                    duration=time.time() - t_sub
                )
                
            # Subtask routed to Executor Agent
            elif "Executor" in subtask.assigned_agent:
                tool_name = subtask.tool_required or "generate_topic_summary"
                params = subtask.input_parameters or {"topic": cleaned_goal}
                
                # Dynamic fallback for common parameter names
                if tool_name == "generate_study_timetable" and "subject" not in params:
                    params["subject"] = cleaned_goal
                    params.setdefault("total_days", 7)
                    params.setdefault("hours_per_day", 3.0)
                elif tool_name == "generate_practice_quiz" and "topic" not in params:
                    params["topic"] = cleaned_goal
                elif tool_name == "generate_topic_summary" and "topic" not in params:
                    params["topic"] = cleaned_goal

                exec_res = self.executor.execute(tool_name, params)
                tool_calls.append(exec_res)
                
                if exec_res.get("success", False):
                    subtask.status = "completed"
                    subtask.result = json.dumps(exec_res.get("result", {}), indent=2)
                    subtask_results.append({"subtask_id": subtask.id, "type": "tool_output", "data": exec_res})
                    log_step(
                        subtask.assigned_agent,
                        f"Subtask #{subtask.id}: Tool Execution",
                        f"Executed allowlisted tool '{tool_name}' successfully.",
                        duration=time.time() - t_sub
                    )
                else:
                    subtask.status = "failed"
                    subtask.result = exec_res.get("error", "Execution failed")
                    log_step(
                        subtask.assigned_agent,
                        f"Subtask #{subtask.id}: Tool Failure",
                        f"Failed executing '{tool_name}': {exec_res.get('error')}",
                        duration=time.time() - t_sub,
                        is_err=True
                    )
            
            # Subtask assigned to Critic Agent (handled in verification loop)
            elif "Critic" in subtask.assigned_agent:
                subtask.status = "completed"
                subtask.result = "Reserved for post-execution verification."

        # 4. Critic & Verification Loop
        t_crit = time.time()
        evaluation = self.critic.evaluate(cleaned_goal, plan, subtask_results, tool_calls, current_revision=0)
        
        # Bounded revision loop if critic requests revision
        revision_count = 0
        while evaluation.revision_requested and revision_count < self.critic.max_revisions:
            revision_count += 1
            log_step(
                "Critic Agent",
                f"Revision #{revision_count} Triggered",
                f"Deficiencies detected: {'; '.join(evaluation.deficiencies)}. Initiating bounded corrective re-execution."
            )
            # Re-execute failed items
            for st in plan.subtasks:
                if st.status == "failed" and st.tool_required:
                    retry_res = self.executor.execute(st.tool_required, st.input_parameters)
                    tool_calls.append(retry_res)
                    if retry_res.get("success"):
                        st.status = "completed"
                        st.result = json.dumps(retry_res.get("result", {}), indent=2)
            # Re-evaluate
            evaluation = self.critic.evaluate(cleaned_goal, plan, subtask_results, tool_calls, current_revision=revision_count)

        log_step(
            "Critic Agent",
            "Verification Complete",
            f"Quality Score: {int(evaluation.score * 100)}%. Passed {len(evaluation.checks_passed)} checks.",
            duration=time.time() - t_crit
        )

        # 5. Final Consolidated Response Synthesis
        final_markdown = self._synthesize_final_output(cleaned_goal, plan, subtask_results, evaluation, active_mode)
        
        total_duration = time.time() - start_time
        log_step(
            "Orchestrator",
            "Consolidated Final Result",
            f"Workflow concluded in {round(total_duration, 2)}s with verification score {int(evaluation.score * 100)}%."
        )

        return OrchestrationResult(
            task_id=task_id,
            goal=cleaned_goal,
            mode=active_mode,
            plan=plan,
            steps=steps,
            tool_calls=tool_calls,
            verification=evaluation,
            final_output=final_markdown,
            execution_time_seconds=round(total_duration, 2),
            success=evaluation.is_valid
        )

    def _synthesize_final_output(
        self,
        goal: str,
        plan: TaskPlan,
        subtask_results: List[Dict[str, Any]],
        evaluation: CriticEvaluation,
        mode_str: str
    ) -> str:
        """Formats all agent deliverables into a clean, comprehensive markdown report."""
        lines = [
            f"# 🎓 Study & Productivity Plan: {goal}",
            f"> **Execution Mode:** {mode_str} | **Verification Score:** {int(evaluation.score * 100)}% | **Status:** {'✅ Verified' if evaluation.is_valid else '⚠️ Review Needed'}\n",
            "---",
            "## 📋 Executive Plan & Subtasks"
        ]
        
        for st in plan.subtasks:
            icon = "✅" if st.status == "completed" else "❌" if st.status == "failed" else "⏳"
            lines.append(f"- {icon} **Subtask {st.id} ({st.assigned_agent})**: {st.title}")
            
        lines.append("\n---")
        
        # Add Knowledge Research findings if available
        research_entries = [r["data"] for r in subtask_results if r["type"] == "research"]
        if research_entries:
            lines.append("## 📚 Foundational Curriculum & Research")
            for re in research_entries:
                lines.append(re.get("findings", ""))
                sources = re.get("sources", [])
                if sources:
                    lines.append(f"\n*Sources:* {', '.join(sources)}")
            lines.append("\n---")

        # Add Tool Deliverables
        tool_entries = [r["data"] for r in subtask_results if r["type"] == "tool_output"]
        for te in tool_entries:
            res = te.get("result", {})
            tool_name = te.get("tool", "")
            
            # Study Timetable
            if "schedule" in res and isinstance(res["schedule"], list):
                lines.append(f"## 📅 Personalized Study Timetable: {res.get('subject')}")
                lines.append(f"**Total Commitment:** {res.get('total_study_hours')} hours across {res.get('total_days')} days ({res.get('hours_per_day')} hrs/day)\n")
                lines.append("| Day | Focus Theme | Daily Allocated Hours | Recommended Checkpoint |")
                lines.append("|---|---|---|---|")
                for day_item in res["schedule"]:
                    lines.append(f"| Day {day_item['day']} | {day_item['theme']} | {day_item['allocated_hours']} hrs | {day_item['recommended_checkpoint']} |")
                lines.append("\n")

            # Practice Quiz
            elif "questions" in res and isinstance(res["questions"], list):
                lines.append(f"## 🧠 Practice Quiz & Active Recall Assessment: {res.get('topic')}")
                for q in res["questions"]:
                    lines.append(f"### Question {q.get('question_id')}: {q.get('question')}")
                    for opt in q.get("options", []):
                        lines.append(f"- {opt}")
                    lines.append(f"\n**Correct Answer:** {q.get('correct_answer')}")
                    lines.append(f"**Explanation:** {q.get('explanation')}\n")
                lines.append("\n")

            # Topic Summary Breakdown
            elif "key_pillars" in res:
                lines.append(f"## 📖 Concept Synthesis: {res.get('topic')}")
                lines.append(f"**Foundational Context:** {res.get('foundations')}\n")
                lines.append("**Key Pillars:**")
                for p in res.get("key_pillars", []):
                    lines.append(f"- {p}")
                lines.append(f"\n**Practical Application:** {res.get('practical_application')}")
                lines.append(f"**Feynman Plain-Language Summary:** {res.get('feynman_summary')}\n")

            # General Calculation / Milestone outputs
            elif "milestones" in res:
                lines.append(f"## 🎯 Assignment Milestones: {res.get('assignment')}")
                for ms in res.get("milestones", []):
                    lines.append(f"- **{ms['phase']}** (By Day {ms['target_day']}): {ms['deliverable']}")
                lines.append("\n")

        # Add Verification Panel
        lines.append("## 🔍 Agent Verification & Audit Notes")
        lines.append(f"**Audited by:** Critic and Verification Agent")
        lines.append(f"**Confidence Score:** {int(evaluation.score * 100)}%")
        lines.append("\n**Checks Passed:**")
        for cp in evaluation.checks_passed:
            lines.append(f"- ✅ {cp}")
        if evaluation.deficiencies:
            lines.append("\n**Flagged Deficiencies:**")
            for df in evaluation.deficiencies:
                lines.append(f"- ⚠️ {df}")
                
        return "\n".join(lines)
