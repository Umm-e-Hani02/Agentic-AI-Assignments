from typing import TypedDict
from agents import function_tool, RunContextWrapper, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class SimpleMealPlanInput(TypedDict):
    diet_type: str

@function_tool
async def meal_planner(wrapper: RunContextWrapper, input: SimpleMealPlanInput) -> dict:
    prompt = (
        f"Create a 7-day meal plan for a {input['diet_type']} diet.\n"
        "Each day should include:\n- Breakfast\n- Lunch\n- Dinner\n- Healthy Snack"
    )

    try:
        response = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        meal_plan = response.choices[0].message.content

        return {"meal_plan": meal_plan}

    except Exception as e:
        return {"error": f"Meal planner failed: {str(e)}"}
