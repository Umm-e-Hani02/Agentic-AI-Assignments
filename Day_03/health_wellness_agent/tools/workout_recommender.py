from pydantic import BaseModel
from agents import function_tool, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class FitnessTarget(BaseModel):
    goal_type: str         
    amount: int           
    unit: str              
    duration: int          
    duration_unit: str     

class WeeklyWorkout(BaseModel):
    routine: str

@function_tool
async def workout_recommender(goal: FitnessTarget) -> WeeklyWorkout:
    """
    Builds a customized 7-day workout routine based on user's fitness objective.
    Output includes daily plans with a safe and motivating approach.
    """
    try:
        instructions = (
            f"A user aims to {goal.goal_type} {goal.amount} {goal.unit} in {goal.duration} {goal.duration_unit}.\n"
            "Design a beginner-friendly 7-day workout schedule to help them stay on track.\n"
            "Break it down day-wise using bullet points and include:\n"
            "- Cardio or strength workouts 💪\n"
            "- Recovery days 🧘\n"
            "- Motivation tips 📝"
        )

        reply = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": instructions}]
        )

        plan_text = reply.candidates[0].content.parts[0].text.strip()
        

        return WeeklyWorkout(routine=plan_text)

    except Exception as error:
        print("❌ Error in workout_recommender:", error)
        return WeeklyWorkout(routine="⚠️ Unable to generate your fitness plan at the moment. Please try again later.")
