
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("API Key is not found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError("No usage response.")

        message = response.choices[0].message

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        # Add the assistant's response to conversation history
        messages.append(message)

        # If there are no tool calls, the agent has finished
        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        # Execute each requested tool and add its result to history
        for tool_call in message.tool_calls:
            result_message = call_function(
                tool_call,
                verbose=args.verbose,
            )

            if not result_message.get("content"):
                raise RuntimeError(
                    "Function call returned empty content"
                )

            messages.append(result_message)

            if args.verbose:
                print(f"-> {result_message['content']}")

    print("Error: Maximum number of iterations (20) reached.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
