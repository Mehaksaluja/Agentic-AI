from services.chatbot_service import ChatbotService
from utils.logger import logger
def main():
    logger.info("Starting LangChain Chatbot...")
    chatbot = ChatbotService()
    print("=" * 70)
    print("AI Chatbot (LangChain + Groq)")
    print("=" * 70)
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You : ")
        if question.lower() == "exit":
            print("\nGoodbye")
            break
        try:
            response = chatbot.ask(question)
            print(f"\nAI : {response}\n")
        except Exception as e:
            logger.exception(e)
            print("\nSomething went wrong.\n")

if __name__ == "__main__":
    main()