from agents import Agent, RunContextWrapper
import chainlit as cl

def switch_agent(agent: Agent):
    async def handler(ctx: RunContextWrapper[None]):
        # Inform the user about the handoff
        await cl.Message(f"🔄 Switching to **{agent.name}**...").send()
        
        # Change the session's current agent
        cl.user_session.set("agent", agent)

    return handler