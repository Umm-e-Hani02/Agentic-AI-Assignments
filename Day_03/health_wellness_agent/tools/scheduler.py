from agents import function_tool, AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class RoutineInput(BaseModel):
    start_time: str
    end_time: str

class RoutineOutput(BaseModel):
    day_plan: str

@function_tool
async def schedular(input: RoutineInput) -> RoutineOutput:
    """
    Creates a full-day wellness routine using provided wake-up and sleep times.
    Suggestions include meals, water breaks, movement, rest, and self-care activities.
    """
    try:
        query = (
            f"Design a full-day wellness routine for someone who wakes up at {input.start_time} "
            f"and sleeps at {input.end_time}. Include the following:\n"
            "- Meal timings: breakfast, lunch, dinner, snacks 🍽️\n"
            "- Water intake reminders 💧\n"
            "- Short workout or stretching suggestions 🏋️\n"
            "- Meditation or mindfulness break 🧘‍♀️\n"
            "- Wind-down and rest period at night 🌙\n"
            "Format: hour-by-hour bullet points with emojis for each activity."
        )

        result = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": query}]
        )

        plan = result.choices[0].message.content

        return RoutineOutput(day_plan=plan)

    except Exception as error:
        return RoutineOutput(day_plan="⚠️ Sorry, something went wrong while generating your routine.")
