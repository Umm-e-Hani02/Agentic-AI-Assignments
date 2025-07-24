import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

# Set up Gemini Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# AI Agent setup
agent = Agent(
    name="Story Generator Bot",
    instructions="You are a story generator. You generate stories based on the topic provided by the user in English.",
    model=model,
)

# Friendly intro from bot
print("🤖 Hello! I am your Story Generator Bot.")
print("🎭 I can write short stories based on any genre or topic you give me.")

# Ask user for input
genre = input("📚 Which topic you want to write a story about? (e.g., horror, fantasy, adventure or any other topic): ")
prompt = f"Write a short paragraph about {genre}"

# Generate and print story
result = Runner.run_sync(agent, prompt, run_config=config)
print("\n📝 Here is your story:\n")
print(result.final_output)