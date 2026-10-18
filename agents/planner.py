import json
import re
from typing import Dict, Any, Optional
from core.models import TaskPlan, SubTask
from core.llm_client import LLMClient

class PlannerAgent:
    """Interprets user study goals, extracts constraints, and synthesizes structured multi-step execution plans."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
        self.agent_name = "Planner Agent"

    def plan(self, goal: str, constraints: Optional[list] = None) -> TaskPlan:
        """Generates an actionable, ordered TaskPlan with assigned agents and required tools."""
        cleaned_goal = goal.strip()
        user_constraints = constraints or []
        
        if not cleaned_goal:
            return TaskPlan(
                goal="[Empty Goal]",
                target_outcome="No goal specified.",
                constraints=[],
                subtasks=[],
                required_tools=[],
                required_agents=[self.agent_name]
            )

        # Check if live LLM mode can be used
        if not self.llm.is_offline:
            plan = self._llm_plan(cleaned_goal, user_constraints)
            if plan:
                return plan

        # Deterministic offline planner fallback
        return self._deterministic_plan(cleaned_goal, user_constraints)

    def _llm_plan(self, goal: str, constraints: list) -> Optional[TaskPlan]:
        system_prompt = (
            "You are the Planner Agent in an Agentic AI Study Assistant. "
            "Decompose the user's study goal into 3-5 ordered subtasks. "
            "Respond ONLY with valid JSON conforming to this schema:\n"
            "{\n"
            "  \"target_outcome\": \"string\",\n"
            "  \"constraints\": [\"string\"],\n"
            "  \"required_tools\": [\"string\"],\n"
            "  \"required_agents\": [\"string\"],\n"
            "  \"subtasks\": [\n"
            "    {\"id\": 1, \"title\": \"string\", \"description\": \"string\", \"assigned_agent\": \"Knowledge Agent|Executor Agent|Critic Agent\", \"tool_required\": \"tool_name or null\", \"input_parameters\": {}}\n"
            "  ]\n"
            "}"
        )
        prompt = f"Goal: {goal}\nConstraints: {constraints}"
        try:
            raw = self.llm.generate(prompt, system_prompt, json_mode=True)
            # Find JSON block if wrapped in markdown
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                subtasks = [SubTask(**st) for st in data.get("subtasks", [])]
                return TaskPlan(
                    goal=goal,
                    target_outcome=data.get("target_outcome", "Complete specified study goal"),
                    constraints=data.get("constraints", constraints),
                    subtasks=subtasks,
                    required_tools=data.get("required_tools", []),
                    required_agents=data.get("required_agents", ["Knowledge Agent", "Executor Agent", "Critic Agent"])
                )
        except Exception:
            pass
        return None

    def _deterministic_plan(self, goal: str, constraints: list) -> TaskPlan:
        """Decomposes goal using rule-based pattern matching."""
        lower = goal.lower()
        subtasks = []
        required_tools = []
        
        # 1. Study Timetable or Pacing Request
        if any(w in lower for w in ["timetable", "schedule", "routine", "hours", "days", "plan"]):
            subtasks = [
                SubTask(
                    id=1,
                    title="Retrieve Curriculum Principles & Pacing Standards",
                    description="Consult local knowledge repository for optimal study distribution rules.",
                    assigned_agent="Knowledge Agent",
                    tool_required="search_local_knowledge",
                    input_parameters={"query": "study methodologies spaced repetition pomodoro"}
                ),
                SubTask(
                    id=2,
                    title="Calculate Daily Hour Allocation & Breaks",
                    description="Compute daily required hours and pomodoro intervals based on timeline.",
                    assigned_agent="Executor Agent",
                    tool_required="calculate_study_schedule",
                    input_parameters={"total_hours": 20.0, "available_days": 7}
                ),
                SubTask(
                    id=3,
                    title="Synthesize Comprehensive Study Timetable",
                    description="Generate structured day-by-day timetable with topic milestones.",
                    assigned_agent="Executor Agent",
                    tool_required="generate_study_timetable",
                    input_parameters={"subject": goal, "total_days": 7, "hours_per_day": 3.0}
                ),
                SubTask(
                    id=4,
                    title="Critique and Validate Schedule Feasibility",
                    description="Verify that study time calculations and daily workloads are realistic and balanced.",
                    assigned_agent="Critic Agent",
                    tool_required="validate_schedule",
                    input_parameters={"target": "timetable"}
                )
            ]
            required_tools = ["search_local_knowledge", "calculate_study_schedule", "generate_study_timetable"]

        # 2. Practice Quiz or Self-Assessment Request
        elif any(w in lower for w in ["quiz", "test", "exam", "questions", "mcq"]):
            subtasks = [
                SubTask(
                    id=1,
                    title="Extract Topic Core Knowledge & Concepts",
                    description="Gather authoritative curriculum notes for question synthesis.",
                    assigned_agent="Knowledge Agent",
                    tool_required="search_local_knowledge",
                    input_parameters={"query": goal}
                ),
                SubTask(
                    id=2,
                    title="Generate Formative Practice Quiz",
                    description="Synthesize multiple-choice and conceptual assessment questions.",
                    assigned_agent="Executor Agent",
                    tool_required="generate_practice_quiz",
                    input_parameters={"topic": goal, "num_questions": 3}
                ),
                SubTask(
                    id=3,
                    title="Audit Quiz Questions and Explanations",
                    description="Ensure answer keys are unambiguous and explanations are educationally sound.",
                    assigned_agent="Critic Agent",
                    tool_required="validate_quiz",
                    input_parameters={"target": "quiz"}
                )
            ]
            required_tools = ["search_local_knowledge", "generate_practice_quiz"]

        # 3. Default Comprehensive Study & Summary Plan
        else:
            subtasks = [
                SubTask(
                    id=1,
                    title="Retrieve Domain Knowledge & Foundations",
                    description="Search local knowledge repository for authoritative foundational concepts.",
                    assigned_agent="Knowledge Agent",
                    tool_required="search_local_knowledge",
                    input_parameters={"query": goal}
                ),
                SubTask(
                    id=2,
                    title="Generate Synthesized Topic Breakdown",
                    description="Structure key pillars, practical applications, and conceptual summaries.",
                    assigned_agent="Executor Agent",
                    tool_required="generate_topic_summary",
                    input_parameters={"topic": goal}
                ),
                SubTask(
                    id=3,
                    title="Generate Review Quiz Questions",
                    description="Create active recall questions to reinforce learned concepts.",
                    assigned_agent="Executor Agent",
                    tool_required="generate_practice_quiz",
                    input_parameters={"topic": goal, "num_questions": 3}
                ),
                SubTask(
                    id=4,
                    title="Verify Synthesized Results",
                    description="Audit outputs for factual consistency, completeness, and clarity.",
                    assigned_agent="Critic Agent",
                    tool_required="verify_synthesis",
                    input_parameters={"target": "topic_summary"}
                )
            ]
            required_tools = ["search_local_knowledge", "generate_topic_summary", "generate_practice_quiz"]

        return TaskPlan(
            goal=goal,
            target_outcome=f"Deliver verified, actionable study assistance for '{goal}'",
            constraints=constraints or ["Maintain strict factual grounding", "Include actionable checkpoints"],
            subtasks=subtasks,
            required_tools=required_tools,
            required_agents=["Knowledge Agent", "Executor Agent", "Critic Agent"]
        )
