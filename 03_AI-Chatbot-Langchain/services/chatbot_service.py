from chains.chatbot_chain import (
    ChatbotChain
)

class ChatbotService:
    def __init__(self):
        self.chain = ChatbotChain.create()
    def ask(self, question: str):
        return self.chain.invoke(
            {
                "question": question
            }
        )