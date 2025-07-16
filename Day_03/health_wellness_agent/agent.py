import os
from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from dotenv import load_dotenv
from guardrails import health_guardail_input, health_guardail_output
from other_agents.escalation_agent import escalation_agent
from other_agents.injury_support_agent import injury_support_agent
from other_agents.nutrition_expert_agent import nutrition_expert_agent
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner
from tools.scheduler import schedular
from tools.tracker import tracker
from tools.workout_recommender import workout_recommender
from handoff import switch_agent

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash"
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

health_wellness_agent = Agent(
    name="Health and Wellness Agent",
    instructions="""
You are a helpful and friendly Health and Wellness Agent.

🎯 Your main responsibility is to handle **general wellness queries** using the available tools.

🛠️ Use tools based on the type of request:
- Use the `goal_analyzer` tool when the user shares a fitness goal like losing or gaining weight.
- Use the `meal_planner` tool to generate a 7-day meal plan based on diet type.
- Use the `schedular` tool to create a healthy daily routine based on wake-up and sleep times.
- Use the `tracker` tool to summarize a user's daily health progress.
- Use the `workout_recommender` tool to provide a personalized 7-day workout plan based on fitness goals.

🤝 For **specialized queries**, hand off the task to the appropriate expert agent:
- If the user mentions an **injury** or **pain**, hand off to the `injury_support_agent`.
- If the user needs **detailed nutrition advice** or has specific dietary conditions, hand off to the `nutrition_expert_agent`.
- For anything outside your expertise or if the query needs escalation, hand off to the `escalation_agent`.

Respond in a clear, motivational, and supportive tone. Always aim to guide the user toward a healthier lifestyle.
""",
    model=model,
    input_guardrails=[health_guardail_input],
    output_guardrails=[health_guardail_output],
    tools = [goal_analyzer, meal_planner, schedular, tracker, workout_recommender],
    handoffs=[
        handoff(agent=injury_support_agent, on_handoff=switch_agent(injury_support_agent)),
        handoff(agent=nutrition_expert_agent, on_handoff=switch_agent(nutrition_expert_agent)),
        handoff(agent=escalation_agent, on_handoff=switch_agent(escalation_agent))
    ]
)