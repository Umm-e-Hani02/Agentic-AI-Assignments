import chainlit as cl
from agent import health_and_wellness_agent
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from guardrails import contains_sensitive_keywords


@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="""👋 Hello! I'm your Health & Wellness Assistant. How can I help you today?"""
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    input_text = message.content.strip().lower()

    if contains_sensitive_keywords(input_text):
        await cl.Message(
            content="⚠️ It seems like you're going through something serious. Connecting you to a human wellness coach..."
        ).send()
        return  

    msg = cl.Message(content="")
    await msg.send()

    history.append({"role": "user", "content": message.content})
    result = Runner.run_streamed(
        health_and_wellness_agent,
        input=history,
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
