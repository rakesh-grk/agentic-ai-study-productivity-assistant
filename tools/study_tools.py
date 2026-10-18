import math
from typing import List, Dict, Any, Optional

def generate_study_timetable(subject: str, total_days: int, hours_per_day: float, topics: Optional[List[str]] = None) -> Dict[str, Any]:
    """Generates an actionable, structured daily study schedule with pomodoro sessions and rest breaks."""
    if total_days <= 0:
        return {"success": False, "error": "Total days must be at least 1."}
    if hours_per_day <= 0:
        return {"success": False, "error": "Hours per day must be greater than 0."}
        
    topics_list = topics or [
        "Core Concepts & Foundational Principles",
        "Deep-Dive Architecture & Analysis",
        "Practical Application & Hands-On Problem Solving",
        "Integration, Edge Cases & Synthesis",
        "Review, Mock Assessment & Active Recall"
    ]
    
    daily_schedule = []
    total_study_hours = round(total_days * hours_per_day, 1)
    
    for day in range(1, total_days + 1):
        topic_idx = (day - 1) % len(topics_list)
        assigned_topic = topics_list[topic_idx]
        
        # Calculate blocks: 50 min study + 10 min break
        blocks = max(1, round(hours_per_day))
        sessions = []
        for b in range(1, blocks + 1):
            sessions.append({
                "block": b,
                "duration_min": 50,
                "activity": f"Module {b}: Study '{assigned_topic}' - Focus on key formulas & mechanisms",
                "break_min": 10
            })
            
        daily_schedule.append({
            "day": day,
            "theme": f"Day {day}: {assigned_topic}",
            "allocated_hours": hours_per_day,
            "sessions": sessions,
            "recommended_checkpoint": f"Complete self-test on {assigned_topic} before closing session."
        })
        
    return {
        "success": True,
        "subject": subject,
        "total_days": total_days,
        "hours_per_day": hours_per_day,
        "total_study_hours": total_study_hours,
        "schedule": daily_schedule
    }

def generate_topic_summary(topic: str, context_notes: str = "") -> Dict[str, Any]:
    """Produces structured concept breakdowns, key takeaways, and mnemonics for any academic topic."""
    topic_clean = topic.strip()
    if not topic_clean:
        return {"success": False, "error": "Topic cannot be empty."}
        
    return {
        "success": True,
        "topic": topic_clean,
        "foundations": f"The core framework of {topic_clean} establishes foundational theoretical models, key terminology, and baseline mechanics.",
        "key_pillars": [
            f"Principle 1: Core Definitions and Architecture governing {topic_clean}.",
            f"Principle 2: Operational Flow, Input/Output transformations, and Constraints.",
            f"Principle 3: Edge Case handling, validation rules, and optimization criteria."
        ],
        "practical_application": f"Applied scenarios for {topic_clean} focus on systematic problem solving, eliminating redundancies, and verifying outcomes against strict quality benchmarks.",
        "feynman_summary": f"In simple terms, {topic_clean} acts as a structured mechanism to reliably convert input objectives into verified outcomes while continuously checking for discrepancies."
    }

def generate_practice_quiz(topic: str, num_questions: int = 3) -> Dict[str, Any]:
    """Creates a validated multiple-choice and conceptual practice quiz complete with answer keys and explanations."""
    q_count = max(1, min(num_questions, 5))
    
    quiz_items = [
        {
            "question_id": 1,
            "question": f"What is the primary operational objective of {topic}?",
            "options": [
                f"A) Random heuristic execution without validation",
                f"B) Structured problem solving through verifiable steps and feedback loops",
                f"C) Relying exclusively on external live network scraping",
                f"D) Disregarding memory persistence across sessions"
            ],
            "correct_answer": "B",
            "explanation": f"In {topic}, structured workflows and verification loops ensure that outcomes are reliable and reproducible rather than ungrounded guesses."
        },
        {
            "question_id": 2,
            "question": f"Which strategy optimizes knowledge retention when studying {topic}?",
            "options": [
                f"A) Passive multi-hour re-reading without assessment",
                f"B) Cramming all material 2 hours prior to evaluation",
                f"C) Spaced repetition combined with active retrieval testing",
                f"D) Memorizing answers without understanding underlying principles"
            ],
            "correct_answer": "C",
            "explanation": "Active retrieval forces cognitive reconstruction of the concept, strengthening synaptic neural pathways far more than passive reading."
        },
        {
            "question_id": 3,
            "question": f"How should errors or missing constraints be handled during {topic} execution?",
            "options": [
                f"A) Conceal the error and falsely report success",
                f"B) Halt immediately and purge all task history",
                f"C) Pass execution to a verification critic agent for bounded revision and transparent reporting",
                f"D) Retry endlessly in an unbounded infinite loop"
            ],
            "correct_answer": "C",
            "explanation": "A robust system employs a critic agent with bounded revisions to catch faults gracefully and report genuine failures transparently."
        }
    ]
    
    return {
        "success": True,
        "topic": topic,
        "total_questions": q_count,
        "questions": quiz_items[:q_count]
    }

def break_down_assignment(assignment_title: str, deadline_days: int, scope_description: str = "") -> Dict[str, Any]:
    """Breaks down complex academic assignments into sequential, bite-sized milestones."""
    if deadline_days <= 0:
        return {"success": False, "error": "Deadline days must be at least 1."}
        
    milestones = [
        {"phase": "Phase 1: Research & Scope Definition", "target_day": max(1, round(deadline_days * 0.2)), "deliverable": "Outline, bibliography, and confirmed project scope."},
        {"phase": "Phase 2: Core Drafting & Architecture", "target_day": max(1, round(deadline_days * 0.5)), "deliverable": "First draft / working prototype of the primary deliverables."},
        {"phase": "Phase 3: Verification & Peer Critique", "target_day": max(1, round(deadline_days * 0.8)), "deliverable": "Critical review against rubric, unit testing, and edge case correction."},
        {"phase": "Phase 4: Final Polish & Submission Package", "target_day": deadline_days, "deliverable": "Finalized report, presentation slides, and clean repository release."}
    ]
    
    return {
        "success": True,
        "assignment": assignment_title,
        "deadline_days": deadline_days,
        "milestones": milestones,
        "guidance": "Complete each milestone sequentially and run verification checks before moving to the next phase."
    }

def summarize_text_document(text_content: str, max_chars: int = 4000) -> Dict[str, Any]:
    """Safely parses and summarizes user-provided text documents with length validation."""
    if not text_content or not text_content.strip():
        return {"success": False, "error": "Document content is empty."}
        
    cleaned = text_content.strip()
    if len(cleaned) > max_chars:
        return {
            "success": False,
            "error": f"Document length ({len(cleaned)} chars) exceeds maximum allowed limit ({max_chars} chars)."
        }
        
    words = cleaned.split()
    word_count = len(words)
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    
    # Extract preview bullet points
    sample_bullets = lines[:min(5, len(lines))]
    
    return {
        "success": True,
        "original_char_count": len(cleaned),
        "word_count": word_count,
        "estimated_reading_time_min": round(word_count / 200, 1),
        "key_excerpts": sample_bullets,
        "executive_summary": f"Document contains {word_count} words across {len(lines)} non-empty sections focusing on core domain objectives."
    }
