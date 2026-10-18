import pytest
from agents.critic import CriticAgent
from agents.planner import PlannerAgent
from core.models import TaskPlan, SubTask

def test_critic_all_passed():
    critic = CriticAgent()
    plan = TaskPlan(
        goal="Test Goal",
        target_outcome="Outcome",
        subtasks=[
            SubTask(id=1, title="Sub 1", description="", assigned_agent="Executor Agent", status="completed"),
            SubTask(id=2, title="Sub 2", description="", assigned_agent="Executor Agent", status="completed")
        ]
    )
    subtask_results = [{"type": "output", "data": "valid"}]
    tool_outputs = [
        {"success": True, "tool": "safe_calculate", "result": {"total_study_hours": 10.0, "total_days": 5, "hours_per_day": 2.0}}
    ]
    eval_res = critic.evaluate("Test Goal", plan, subtask_results, tool_outputs)
    assert eval_res.is_valid is True
    assert eval_res.score >= 0.75
    assert len(eval_res.deficiencies) == 0

def test_critic_catches_calculation_inconsistency():
    critic = CriticAgent()
    plan = TaskPlan(
        goal="Inconsistent Math Goal",
        target_outcome="Outcome",
        subtasks=[
            SubTask(id=1, title="Sub 1", description="", assigned_agent="Executor Agent", status="completed")
        ]
    )
    subtask_results = [{"type": "output", "data": "valid"}]
    # 5 days * 2.0 hrs = 10.0, but total_study_hours reported as 99.0
    tool_outputs = [
        {"success": True, "tool": "study_timetable", "result": {"total_study_hours": 99.0, "total_days": 5, "hours_per_day": 2.0}}
    ]
    eval_res = critic.evaluate("Inconsistent Math Goal", plan, subtask_results, tool_outputs)
    assert any("Calculation Inconsistency" in d for d in eval_res.deficiencies)

def test_critic_catches_tool_failures():
    critic = CriticAgent()
    plan = TaskPlan(
        goal="Failed Tool Goal",
        target_outcome="Outcome",
        subtasks=[
            SubTask(id=1, title="Sub 1", description="", assigned_agent="Executor Agent", status="failed")
        ]
    )
    subtask_results = []
    tool_outputs = [{"success": False, "tool": "test_tool", "error": "Disk Error"}]
    eval_res = critic.evaluate("Failed Tool Goal", plan, subtask_results, tool_outputs)
    assert any("Tool Failure" in d for d in eval_res.deficiencies)
