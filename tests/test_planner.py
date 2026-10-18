import pytest
from agents.planner import PlannerAgent
from core.models import TaskPlan

def test_planner_basic_goal():
    planner = PlannerAgent()
    plan = planner.plan("Create a 7-day study timetable for Machine Learning")
    assert isinstance(plan, TaskPlan)
    assert len(plan.subtasks) >= 3
    assert plan.target_outcome != ""
    assert "Executor Agent" in [st.assigned_agent for st in plan.subtasks]
    assert any("timetable" in (st.tool_required or "").lower() for st in plan.subtasks)

def test_planner_quiz_goal():
    planner = PlannerAgent()
    plan = planner.plan("Generate an active recall quiz on Python data structures")
    assert isinstance(plan, TaskPlan)
    assert any("quiz" in (st.tool_required or "").lower() for st in plan.subtasks)
    assert "Critic Agent" in [st.assigned_agent for st in plan.subtasks]

def test_planner_empty_goal():
    planner = PlannerAgent()
    plan = planner.plan("   ")
    assert isinstance(plan, TaskPlan)
    assert len(plan.subtasks) == 0

def test_planner_preserves_constraints():
    planner = PlannerAgent()
    constraints = ["Max 2 hours per day", "Include Pomodoro breaks"]
    plan = planner.plan("Study algorithms", constraints=constraints)
    assert "Max 2 hours per day" in plan.constraints
