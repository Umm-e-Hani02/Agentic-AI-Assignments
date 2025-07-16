import chainlit as cl
from agent import health_wellness_agent
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent

@cl.on_chat_start
async def handle_start_chat():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Hello! I am your Health & Wellness Assistant. How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    # Prepare message for streaming
    msg = cl.Message(content="")
    await msg.send()

    # Add user message to history
    history.append({"role": "user", "content": message.content})

    # Start streaming
    result = Runner.run_streamed(
        health_wellness_agent,
        input=history,
    )

    final_output = ""

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            token = event.data.delta
            final_output += token
            await msg.stream_token(token)

    # Update history
    history.append({"role": "assistant", "content": final_output})
    cl.user_session.set("history", history)
