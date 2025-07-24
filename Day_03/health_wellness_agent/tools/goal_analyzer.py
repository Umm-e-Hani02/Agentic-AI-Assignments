# tools/goal_analyzer.py

from agents import function_tool
from pydantic import BaseModel
import re

class GoalOutput(BaseModel):
    goal_type: str
    quantity: float
    metric: str
    duration: str

@function_tool
async def GoalAnalyzerTool(input: str) -> GoalOutput:
    input = input.lower()

    # Determine goal type
    if "lose" in input or "weight" in input:
        goal_type = "weight_loss"
    elif "gain" in input:
        goal_type = "weight_gain"
    elif "muscle" in input or "build" in input:
        goal_type = "muscle_gain"
    else:
        raise ValueError("❌ Unable to determine goal type from input.")

    # Extract quantity and metric
    quantity_match = re.search(r"(\d+(?:\.\d+)?)\s*(kg|kilos|kilograms|pounds|lbs)", input)
    if quantity_match:
        quantity = float(quantity_match.group(1))
        metric = quantity_match.group(2)
    else:
        raise ValueError("❌ Please specify a quantity and unit (e.g., 5kg or 10 pounds).")

    # Extract duration
    duration_match = re.search(r"in\s+(\d+)\s*(weeks|months|days)", input)
    if duration_match:
        duration = f"{duration_match.group(1)} {duration_match.group(2)}"
    else:
        raise ValueError("❌ Please specify a time duration like 'in 2 months'.")

    return GoalOutput(
        goal_type=goal_type,
        quantity=quantity,
        metric=metric,
        duration=duration
    )
