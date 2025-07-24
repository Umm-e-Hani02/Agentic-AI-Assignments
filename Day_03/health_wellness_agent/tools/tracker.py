from agents import function_tool
from datetime import datetime

@function_tool
async def ProgressTrackerTool(input: str) -> str:
    timestamp = datetime.now().isoformat()
    return f"✅ Progress update saved: {input} at {timestamp}"
