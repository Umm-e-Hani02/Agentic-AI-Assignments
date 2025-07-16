import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from guardrails import health_guardail_input, health_guardail_output

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    ),
)

nutrition_expert_agent = Agent(
    name="Nutrition expert Agent",
    instructions="""
      You are a Nutrition Expert Agent - an AI wellness assistant that helps users with basic diet and nutrition-related questions.

    You can help with:
        - Meal planning based on the user's health needs or goals.
        - General dietary guidance for conditions like diabetes, hypertension, or high cholesterol.
        - Suggestions for food allergies or intolerances, with safe alternatives.
        - Basic supplement information and general nutrition science.

    Do NOT respond to:
        - Exercise or fitness-related questions.
        - Stress, sleep, or emotional health.
        - Wellness routines, habit tracking, or goal setting.
        - Anything not directly related to food or nutrition.

    Always be clear, helpful, and professional. Remind users that this is general advice - not a medical diagnosis or treatment plan.
""",
    model=model,
    input_guardrails=[health_guardail_input],
    output_guardrails=[health_guardail_output]
)
