from typing import Union, List
from pydantic import BaseModel
# Agent components
from agents import (
    Agent, Runner, GuardrailFunctionOutput, RunContextWrapper,
    input_guardrail, output_guardrail, TResponseInputItem
)
from config import gemini_config

class HealthCheck(BaseModel):
    is_safe: bool         
    reason: str          

model = gemini_config.model

# Agent to analyze user input
input_checker = Agent(
    name="HealthInputChecker",
    instructions=(
        "Judge if the user input is health-related and safe."
        " Flag issues like self-harm, illegal drugs, or medical emergencies."
    ),
    output_type=HealthCheck,  
    model=model,              
)

# Agent to analyze assistant's output
output_checker = Agent(
    name="HealthOutputChecker",
    instructions=(
        "Evaluate the assistant's output. "
        "If it's unsafe or medical advice, add disclaimer or warning."
    ),
    output_type=HealthCheck,
    model=model,
)


def contains_health_keywords(text: str, keywords: List[str]) -> bool:
    """
    Check if the given text contains any health-related keywords.
    Used to decide if a medical disclaimer should be added.
    """
    text = text.lower()
    return any(keyword in text for keyword in keywords)


@input_guardrail
async def health_guardail_input(
    ctx: RunContextWrapper,              
    agent: Agent,                         
    user_input: Union[str, List[TResponseInputItem]],
) -> GuardrailFunctionOutput:
    """
    This function checks if the user's input is safe or not.
    It runs the input_checker agent and returns a guardrail result.
    """
    result = await Runner.run(
        starting_agent=input_checker,
        input=user_input,
        context=ctx.context,
        run_config=gemini_config,
    )

    is_safe = result.final_output.is_safe

    return GuardrailFunctionOutput(
        output_info=result.final_output,        # Final result from the agent
        tripwire_triggered=not is_safe,         # If unsafe, trigger tripwire to block input
    )

# ---------- Step 6: Output Guardrail Function ----------

@output_guardrail
async def health_guardail_output(
    ctx: RunContextWrapper,
    agent: Agent,
    assistant_reply: str,   # Assistant's output text
) -> GuardrailFunctionOutput:
    """
    This function checks if the assistant's reply is safe.
    If not, it adds a warning. If medical-related, adds a disclaimer.
    """
    result = await Runner.run(
        starting_agent=output_checker,
        input=assistant_reply,
        context=ctx.context,
        run_config=gemini_config,
    )

    mod_reply = assistant_reply              # Start with original output
    safe_flag = result.final_output.is_safe  # Get safety check result

    # Keywords that trigger medical disclaimers
    keywords = ["health", "treatment", "medical", "doctor", "symptom"]

    # If output is unsafe, add a warning (but don't block — just notify)
    if not safe_flag:
        mod_reply += "\n\n⚠️ *Please review this response with a professional.*"

    # If output contains medical-related words, add disclaimer
    elif contains_health_keywords(assistant_reply, keywords):
        mod_reply += "\n\n⚠️ *Medical Disclaimer: This is AI-generated and not a substitute for professional advice.*"

    return GuardrailFunctionOutput(
        output_info=mod_reply,          # Final modified output with any warning/disclaimer
        tripwire_triggered=False        # Don't block assistant's reply — just modify it
    )
