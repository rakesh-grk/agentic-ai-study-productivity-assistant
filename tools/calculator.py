import re
import ast
import operator
from typing import Dict, Any, Union

# Safe AST-based mathematical expression evaluator (NO eval / NO exec)
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _eval_ast_node(node: ast.AST) -> Union[int, float]:
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)
    elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported math operator: {op_type.__name__}")
        left = _eval_ast_node(node.left)
        right = _eval_ast_node(node.right)
        if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
            raise ZeroDivisionError("Cannot divide by zero in study calculation")
        return _ALLOWED_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_ast_node(node.operand)
        return _ALLOWED_OPERATORS[op_type](operand)
    else:
        raise ValueError("Invalid mathematical expression. Only basic arithmetic numbers and operators are allowed.")

def safe_calculate(expression: str) -> Dict[str, Any]:
    """Safely evaluates an arithmetic expression using AST parsing without arbitrary code execution."""
    cleaned = expression.strip()
    # Guard against excessively long strings or malicious code patterns
    if len(cleaned) > 200 or not re.match(r"^[\d\s\+\-\*\/\(\)\.\%]+$", cleaned):
        return {
            "success": False,
            "error": "Expression contains invalid characters. Only digits and arithmetic operators (+, -, *, /, %, parenthesis) are allowed."
        }
    try:
        parsed = ast.parse(cleaned, mode='eval')
        result = _eval_ast_node(parsed)
        return {
            "success": True,
            "expression": cleaned,
            "result": round(result, 4) if isinstance(result, float) else result
        }
    except Exception as e:
        return {
            "success": False,
            "expression": cleaned,
            "error": str(e)
        }

def calculate_study_schedule(total_hours: float, available_days: int, pomodoro_length_min: int = 25) -> Dict[str, Any]:
    """Calculates daily study hours, pomodoro blocks, and rest intervals."""
    if available_days <= 0:
        return {"success": False, "error": "Available days must be greater than zero."}
    if total_hours <= 0:
        return {"success": False, "error": "Total study hours must be greater than zero."}
    
    daily_hours = round(total_hours / available_days, 2)
    daily_minutes = daily_hours * 60
    pomodoro_sessions_per_day = max(1, round(daily_minutes / (pomodoro_length_min + 5)))
    recommended_break_minutes = round(pomodoro_sessions_per_day * 5, 1)
    
    return {
        "success": True,
        "total_hours": total_hours,
        "available_days": available_days,
        "daily_hours_target": daily_hours,
        "daily_minutes_target": daily_minutes,
        "pomodoro_length_min": pomodoro_length_min,
        "recommended_pomodoros_per_day": pomodoro_sessions_per_day,
        "recommended_daily_break_min": recommended_break_minutes,
        "pace_assessment": "Intensive" if daily_hours > 4 else "Moderate" if daily_hours >= 2 else "Light"
    }
