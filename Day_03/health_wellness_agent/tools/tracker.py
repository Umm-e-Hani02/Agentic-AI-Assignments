from agents import function_tool, AsyncOpenAI, RunContextWrapper
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class HealthLog(TypedDict):
    name: str
    steps_walked: int
    water_intake_liters: float
    sleep_hours: float
    mood: str

@function_tool
async def tracker(ctx: RunContextWrapper, data: HealthLog) -> str:
    """
    Generates a motivating summary based on user's health inputs.
    Output is friendly, short, and highlights key activities.
    """

    try:
        message = (
            f"{data['name']} had the following health data today:\n"
            f"- 👣 Steps walked: {data['steps_walked']}\n"
            f"- 💧 Water intake: {data['water_intake_liters']} L\n"
            f"- 🛌 Sleep duration: {data['sleep_hours']} hours\n"
            f"- 🙂 Mood: {data['mood']}\n\n"
            "Write a 3-5 line friendly summary to encourage them based on today's progress."
        )

        reply = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": message}]
        )

        summary = reply.candidates[0].content.parts[0].text.strip()
        

        return summary

    except Exception as error:
        return "⚠️ Couldn't create summary. Please try again later."
