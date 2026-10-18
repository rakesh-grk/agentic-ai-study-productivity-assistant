from typing import Dict, Any, Callable
from tools.study_tools import (
    generate_study_timetable,
    generate_topic_summary,
    generate_practice_quiz,
    break_down_assignment,
    summarize_text_document
)
from tools.calculator import safe_calculate, calculate_study_schedule
from tools.knowledge_base import search_local_knowledge

class ExecutorAgent:
    """Safely dispatches and executes allowlisted tools for timetable creation,

    summaries, quiz generation, calculations, and document processing.
    """
    
    def __init__(self):
        self.agent_name = "Executor Agent"
        # Strict security allowlist: NEVER execute arbitrary shell commands or code
        self._allowlist: Dict[str, Callable] = {
            "generate_study_timetable": generate_study_timetable,
            "generate_topic_summary": generate_topic_summary,
            "generate_practice_quiz": generate_practice_quiz,
            "break_down_assignment": break_down_assignment,
            "summarize_text_document": summarize_text_document,
            "safe_calculate": safe_calculate,
            "calculate_study_schedule": calculate_study_schedule,
            "search_local_knowledge": search_local_knowledge,
        }

    @property
    def available_tools(self) -> list:
        return list(self._allowlist.keys())

    def execute(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Safely invokes an allowlisted tool with validated parameters."""
        if tool_name not in self._allowlist:
            return {
                "success": False,
                "tool": tool_name,
                "error": f"Security Violation: Tool '{tool_name}' is not in the approved safety allowlist."
            }

        tool_func = self._allowlist[tool_name]
        try:
            # Filter parameters to match accepted signatures
            result = tool_func(**parameters)
            return {
                "success": True,
                "tool": tool_name,
                "parameters": parameters,
                "result": result
            }
        except TypeError as te:
            return {
                "success": False,
                "tool": tool_name,
                "error": f"Invalid tool arguments: {te}"
            }
        except Exception as e:
            return {
                "success": False,
                "tool": tool_name,
                "error": f"Tool execution failed: {e}"
            }
