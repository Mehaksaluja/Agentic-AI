from agent.weather_agent import WeatherAgent


def main():
    agent = WeatherAgent()

    print("=" * 60)
    print("Weather Agent (LangGraph + Groq + OpenWeatherMap)")
    print("=" * 60)
    print("Ask about weather in any city. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        try:
            answer = agent.ask(question)
            print(f"\nAgent: {answer}\n")
        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    main()
