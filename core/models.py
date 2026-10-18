from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class SubTask(BaseModel):
    id: int
    title: str
    description: str
    assigned_agent: str
    tool_required: Optional[str] = None
    input_parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None

class TaskPlan(BaseModel):
    goal: str
    target_outcome: str
    constraints: List[str] = Field(default_factory=list)
    subtasks: List[SubTask] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    required_agents: List[str] = Field(default_factory=list)

class AgentStepRecord(BaseModel):
    step_number: int
    agent_name: str
    action: str
    details: str
    timestamp: float = Field(default_factory=time.time)
    duration_seconds: float = 0.0
    is_error: bool = False

class CriticEvaluation(BaseModel):
    is_valid: bool
    score: float = Field(ge=0.0, le=1.0)
    checks_passed: List[str] = Field(default_factory=list)
    deficiencies: List[str] = Field(default_factory=list)
    revision_requested: bool = False
    critique_notes: str

class OrchestrationResult(BaseModel):
    task_id: str
    goal: str
    mode: str  # "LLM" or "Offline Demo"
    plan: Optional[TaskPlan] = None
    steps: List[AgentStepRecord] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    verification: Optional[CriticEvaluation] = None
    final_output: str = ""
    execution_time_seconds: float = 0.0
    success: bool = True
    error_message: Optional[str] = None

class MemoryRecord(BaseModel):
    id: Optional[int] = None
    goal: str
    summary: str
    tags: str = "general"
    created_at: str
    details_json: Optional[str] = None
