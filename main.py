import os
import openai
from rag import ask_question

# Import open-telemetry dependencies
from arize.otel import register

space_id = os.environ.get("ARIZE_SPACE_ID")
api_key = os.environ.get("ARIZE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup OTel via our convenience function
tracer_provider = register(
    space_id = space_id, # in app space settings page
    api_key = api_key, # in app space settings page
    project_name = "gears_of_war", # name this to whatever you would like
)

# Import the automatic instrumentor from OpenInference
from openinference.instrumentation.openai import OpenAIInstrumentor

# Finish automatic instrumentation
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

def main():
    print("Welcome to the COG, Gear!\n")

    history = []

    while True:
        question = input("Enter your question (type 'quit' or 'exit' to leave):\n")

        if question.lower() in ["quit", "exit"]:
            print("\nYou did good, Gear.")
            break

        try:
            answer = ask_question(question, history=history)
            
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})

            print(f"\nAnswer:\n{answer}\n")

        except Exception as e:
            print(f"\nError processing question: {e}\n")

if __name__ == "__main__":
    main()