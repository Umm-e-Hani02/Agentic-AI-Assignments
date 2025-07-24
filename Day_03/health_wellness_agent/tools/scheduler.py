from agents import function_tool

@function_tool
async def CheckinSchedulerTool(input: str) -> str:
    return "🕒 Weekly progress check scheduled every Sunday at 7 PM."
