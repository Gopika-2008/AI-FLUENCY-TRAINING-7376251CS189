"""Day 3: ReAct agent with safety guards."""

import json
import sys
import os

# Allow Python to find config.py in the parent folder
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college assistant. Use read_webpage to read any page or file "
    "the user mentions, and use calculator for every arithmetic step. "
    "Never guess a number that should come from a page. "
    "If no tool is needed, answer directly."
)


MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    seen_calls = set()
    total_chars = 0

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # Stop when the model gives a final answer
        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        for call in message.tool_calls:

            name = call.function.name
            raw_arguments = call.function.arguments or "{}"

            # Guard 1: detect repeated tool calls
            call_signature = (name, raw_arguments)

            if call_signature in seen_calls:
                result = (
                    "Stopped: repeated identical tool call detected."
                )

                if verbose:
                    print(
                        f"   step {step}: {name} -> {result}"
                    )

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })

                return result

            seen_calls.add(call_signature)

            try:

                arguments = json.loads(raw_arguments)

                function = TOOL_FUNCTIONS.get(name)

                if function is None:
                    result = (
                        f"Unknown tool: {name}. "
                        f"Available: {list(TOOL_FUNCTIONS)}"
                    )

                else:
                    result = function(**arguments)

            except json.JSONDecodeError as error:

                result = (
                    f"Argument error: {error}. "
                    "Send valid JSON."
                )

            except TypeError as error:

                result = f"Argument error: {error}"

            # Guard 2: limit individual tool output
            result = str(result)

            if len(result) > MAX_TOOL_CHARS:
                result = (
                    result[:MAX_TOOL_CHARS]
                    + "\n[Tool output truncated by guard.]"
                )

            # Guard 3: total character budget
            total_chars += len(result)

            if total_chars > CHAR_BUDGET:
                result = (
                    "Stopped: total tool-output character budget exceeded."
                )

                if verbose:
                    print(
                        f"   step {step}: {name} -> {result}"
                    )

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })

                return result

            if verbose:
                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> "
                    f"{result[:120]}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("MY FIXED AGENT")

    question = (
    "Read big.html several times and compare the contents each time. "
    "Keep checking until you are certain."
)
    print("Q:", question)
    print("A:", agent(question))