import os
import json

from groq import Groq
from dotenv import load_dotenv

from tools import calculator, get_time

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI Assistant.

Available tools:

1. calculator
Description: Perform mathematical calculations.

Arguments:
{
  "a": number,
  "b": number,
  "operation": "+|-|*|/"
}

2. get_time
Description: Returns current system time.

When a tool is required respond ONLY in JSON.

Calculator Example:

{
  "tool": "calculator",
  "arguments": {
    "a": 20,
    "b": 5,
    "operation": "*"
  }
}

Time Example:

{
  "tool": "get_time",
  "arguments": {}
}

If no tool is required, answer normally.
"""

def execute_tool(tool_name, arguments):
    if tool_name == "calculator":
        return calculator(
            arguments["a"],
            arguments["b"],
            arguments["operation"]
        )

    elif tool_name == "get_time":
        return get_time()
    
    return "Unknown Tool"


print("\nAI Developer Assistant Started")
print("Type 'exit' to quit\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    try:

        tool_call = json.loads(content)

        tool_name = tool_call["tool"]
        arguments = tool_call["arguments"]

        result = execute_tool(
            tool_name,
            arguments
        )

        print(f"\nTool Result: {result}\n")

    except Exception:

        print(f"\nAssistant: {content}\n")