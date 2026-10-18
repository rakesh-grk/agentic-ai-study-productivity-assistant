import pytest
from tools.study_tools import (
    generate_study_timetable,
    generate_topic_summary,
    generate_practice_quiz,
    break_down_assignment,
    summarize_text_document
)
from tools.calculator import safe_calculate, calculate_study_schedule

def test_generate_study_timetable_valid():
    res = generate_study_timetable("Computer Networks", total_days=5, hours_per_day=2.5)
    assert res["success"] is True
    assert res["total_study_hours"] == 12.5
    assert len(res["schedule"]) == 5
    assert res["schedule"][0]["allocated_hours"] == 2.5

def test_generate_study_timetable_invalid_inputs():
    res = generate_study_timetable("Networking", total_days=0, hours_per_day=2.0)
    assert res["success"] is False
    res2 = generate_study_timetable("Networking", total_days=5, hours_per_day=-1.0)
    assert res2["success"] is False

def test_generate_practice_quiz_structure():
    res = generate_practice_quiz("Operating Systems", num_questions=3)
    assert res["success"] is True
    assert len(res["questions"]) == 3
    for q in res["questions"]:
        assert len(q["options"]) >= 2
        assert q["correct_answer"] in ["A", "B", "C", "D"]
        assert len(q["explanation"]) > 10

def test_safe_calculate_arithmetic():
    res = safe_calculate("(10 + 5) * 2 - 4 / 2")
    assert res["success"] is True
    assert res["result"] == 28.0

def test_safe_calculate_zero_division():
    res = safe_calculate("100 / 0")
    assert res["success"] is False
    assert "divide by zero" in res["error"].lower()

def test_safe_calculate_blocks_code_execution():
    res = safe_calculate("__import__('os').system('dir')")
    assert res["success"] is False
    assert "invalid characters" in res["error"].lower()

def test_calculate_study_schedule_valid():
    res = calculate_study_schedule(total_hours=21.0, available_days=7, pomodoro_length_min=25)
    assert res["success"] is True
    assert res["daily_hours_target"] == 3.0
    assert res["recommended_pomodoros_per_day"] >= 5

def test_summarize_text_document_validation():
    # Valid short text
    res = summarize_text_document("First line.\nSecond line.\nThird line.")
    assert res["success"] is True
    assert res["word_count"] > 0
    # Overly long text
    huge_text = "word " * 2000
    res_huge = summarize_text_document(huge_text, max_chars=500)
    assert res_huge["success"] is False
    assert "exceeds maximum" in res_huge["error"]
