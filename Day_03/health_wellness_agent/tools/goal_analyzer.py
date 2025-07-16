import re
from typing import TypedDict
from pydantic import BaseModel
from agents import function_tool, RunContextWrapper

class GoalInput(TypedDict):
    input_text: str

class StructuredGoal(BaseModel):
    goal_type: str      
    amount: int         
    unit: str           
    duration: int       
    duration_unit: str 

@function_tool
async def goal_analyzer(wrapper: RunContextWrapper, input: GoalInput) -> StructuredGoal:
    text = input["input_text"].lower().strip()

    pattern = r"(lose|gain)\s+(\d+)\s*(kg|pounds)\s+(?:in|within)\s+(\d+)\s*(days|weeks|months)"
    match = re.search(pattern, text)

    if not match:
        raise ValueError("Please use this format: 'Lose 5kg in 2 months' or 'Gain 10 pounds within 3 weeks'.")

    goal_type, amount, unit, duration, duration_unit = match.groups()

    return StructuredGoal(
        goal_type=goal_type,
        amount=int(amount),
        unit=unit,
        duration=int(duration),
        duration_unit=duration_unit
    )
