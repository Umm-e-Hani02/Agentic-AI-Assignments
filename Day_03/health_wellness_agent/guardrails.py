from agents import GuardrailFunctionOutput, RunContextWrapper, Agent, input_guardrail, output_guardrail
from typing import Union, List


# ⛔️ Don't decorate this yet
async def _raw_input_safety_check(
    ctx: RunContextWrapper, agent: Agent, input: Union[str, List]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input_text = " ".join(str(i) for i in input)
    else:
        input_text = str(input)

    input_text = input_text.strip().lower()

    if not input_text:
        return GuardrailFunctionOutput(
            output_info="❌ Empty input is not allowed.",
            tripwire_triggered=True
        )

    if contains_sensitive_keywords(input_text):
        return GuardrailFunctionOutput(
            output_info="❌ Sensitive content detected. Please talk to a professional.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info="✅ Input safe.",
        tripwire_triggered=False
    )


# 🧠 Sensitive keywords
SENSITIVE_KEYWORDS = [
    "suicide", "end my life", "kill myself", "depressed", "i want to die",
    "self harm", "hurt myself", "i give up", "no reason to live"
]

def contains_sensitive_keywords(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in SENSITIVE_KEYWORDS)

# ✅ Universal Input Guardrail
@input_guardrail
async def input_safety_check(
    ctx: RunContextWrapper, agent: Agent, input: Union[str, List]
) -> GuardrailFunctionOutput:
    if isinstance(input, list):
        input_text = " ".join(str(i) for i in input)
    else:
        return GuardrailFunctionOutput(
            output_info="❌ Invalid input format.",
            tripwire_triggered=True
        )

    input_text = input_text.strip().lower()

    if not input_text:
        return GuardrailFunctionOutput(
            output_info="❌ Empty input is not allowed.",
            tripwire_triggered=True
        )

    if contains_sensitive_keywords(input_text):
        return GuardrailFunctionOutput(
            output_info="❌ Sensitive content detected. Please talk to a professional.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info="✅ Input safe.",
        tripwire_triggered=False
    )

# ✅ Universal Output Guardrail
@output_guardrail
async def output_safety_check(
    ctx: RunContextWrapper, agent: Agent, output: Union[str, dict]
) -> GuardrailFunctionOutput:
    if isinstance(output, str):
        response = output.strip()
    elif isinstance(output, dict):
        response = str(output)
    else:
        response = ""

    if not response:
        return GuardrailFunctionOutput(
            output_info="❌ Empty response not allowed.",
            tripwire_triggered=True
        )

    if contains_sensitive_keywords(response):
        return GuardrailFunctionOutput(
            output_info="❌ Unsafe response content detected.",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info="✅ Output safe.",
        tripwire_triggered=False
    )
