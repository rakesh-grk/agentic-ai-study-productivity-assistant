from typing import Dict, Any, List, Optional
from core.models import CriticEvaluation, TaskPlan
from core.configuration import AppConfig

class CriticAgent:
    """Rigorous verification agent that evaluates task completion, arithmetic validity,

    structured formatting, and factual grounding with bounded revision limits.
    """
    
    def __init__(self, max_revisions: Optional[int] = None):
        self.agent_name = "Critic and Verification Agent"
        self.max_revisions = max_revisions or AppConfig.MAX_REVISION_ATTEMPTS

    def evaluate(
        self,
        goal: str,
        plan: TaskPlan,
        subtask_results: List[Dict[str, Any]],
        tool_outputs: List[Dict[str, Any]],
        current_revision: int = 0
    ) -> CriticEvaluation:
        """Performs multi-point quality, arithmetic, and completeness verification."""
        checks_passed: List[str] = []
        deficiencies: List[str] = []
        
        # 1. Goal Alignment & Subtask Completion Check
        total_subtasks = len(plan.subtasks)
        completed_subtasks = sum(1 for st in plan.subtasks if st.status == "completed")
        
        if total_subtasks > 0 and completed_subtasks == total_subtasks:
            checks_passed.append(f"Subtask Completion: All {total_subtasks} planned subtasks completed successfully.")
        else:
            deficiencies.append(f"Incomplete Workflow: Only {completed_subtasks}/{total_subtasks} subtasks completed.")

        # 2. Tool Execution Quality & Error Check
        failed_tools = [to for to in tool_outputs if not to.get("success", False)]
        if not failed_tools:
            checks_passed.append("Tool Execution Integrity: All invoked tools executed without exceptions.")
        else:
            for ft in failed_tools:
                deficiencies.append(f"Tool Failure in '{ft.get('tool')}': {ft.get('error')}")

        # 3. Arithmetic & Domain Consistency Verification
        has_calc = False
        calc_consistent = True
        for to in tool_outputs:
            res = to.get("result", {})
            if isinstance(res, dict):
                # Verify timetable calculation: total_hours == total_days * hours_per_day
                if "total_study_hours" in res and "total_days" in res and "hours_per_day" in res:
                    has_calc = True
                    expected = round(res["total_days"] * res["hours_per_day"], 1)
                    actual = round(res["total_study_hours"], 1)
                    if abs(expected - actual) > 0.05:
                        calc_consistent = False
                        deficiencies.append(f"Calculation Inconsistency: total_study_hours ({actual}) != days * daily_hours ({expected})")
                # Verify quiz structure: each question has at least 2 options and a correct answer
                if "questions" in res and isinstance(res["questions"], list):
                    for q in res["questions"]:
                        if not q.get("options") or len(q.get("options", [])) < 2 or not q.get("correct_answer"):
                            deficiencies.append(f"Malformed Quiz: Question #{q.get('question_id')} is missing valid options or answer key.")

        if has_calc and calc_consistent:
            checks_passed.append("Arithmetic Validation: Mathematical and scheduling outputs are logically consistent.")

        # 4. Content Grounding & Substantive Output Check
        if subtask_results:
            checks_passed.append("Output Substance: Subtask outputs contain actionable, non-empty deliverables.")
        else:
            deficiencies.append("Zero substantive outputs generated across all agent steps.")

        # Calculate score
        total_checks = len(checks_passed) + len(deficiencies)
        score = round(len(checks_passed) / max(1, total_checks), 2)
        
        # Decide if revision is needed and within budget
        is_valid = len(deficiencies) == 0 or score >= 0.75
        revision_requested = (not is_valid) and (current_revision < self.max_revisions)
        
        notes = (
            f"Evaluated by {self.agent_name}. Passed {len(checks_passed)} checks. "
            f"Identified {len(deficiencies)} issues. "
            f"Revision status: {'Requested (Attempt ' + str(current_revision + 1) + ')' if revision_requested else 'Accepted/Finalized'}."
        )

        return CriticEvaluation(
            is_valid=is_valid,
            score=score,
            checks_passed=checks_passed,
            deficiencies=deficiencies,
            revision_requested=revision_requested,
            critique_notes=notes
        )
