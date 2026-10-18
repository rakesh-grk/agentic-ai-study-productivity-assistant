import pytest
from core.orchestrator import StudyOrchestrator
from core.models import OrchestrationResult

def test_orchestrator_offline_mode_success():
    orchestrator = StudyOrchestrator(force_offline=True)
    res = orchestrator.run("Create a 7-day study timetable for Agentic AI Architecture with 3 hours daily")
    assert isinstance(res, OrchestrationResult)
    assert res.success is True
    assert "Offline Demo" in res.mode
    assert len(res.steps) >= 3
    assert res.verification is not None
    assert res.verification.score >= 0.7
    assert len(res.final_output) > 100
    assert "Agentic AI" in res.final_output

def test_orchestrator_quiz_workflow():
    orchestrator = StudyOrchestrator(force_offline=True)
    res = orchestrator.run("Generate an active recall practice quiz on Python data structures")
    assert res.success is True
    assert any("quiz" in to.get("tool", "").lower() for to in res.tool_calls)
    assert "Practice Quiz" in res.final_output

def test_orchestrator_empty_input():
    orchestrator = StudyOrchestrator(force_offline=True)
    res = orchestrator.run("   ")
    assert res.success is False
    assert "Empty study goal" in (res.error_message or "")

def test_orchestrator_step_callback():
    orchestrator = StudyOrchestrator(force_offline=True)
    captured_steps = []
    
    def on_step(rec):
        captured_steps.append(rec)
        
    res = orchestrator.run("Study Python", on_step_callback=on_step)
    assert len(captured_steps) == len(res.steps)
    assert captured_steps[0].step_number == 1
