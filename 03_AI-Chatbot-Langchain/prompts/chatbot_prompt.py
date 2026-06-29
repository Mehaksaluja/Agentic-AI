from langchain_core.prompts import ChatPromptTemplate

class ChatbotPrompt:
    @staticmethod
    def create():
        return ChatPromptTemplate.from_messages(
            [
             (

                    "system",
                    """
                    You are a helpful AI Assistant.
                    Answer in a simple and professional way.

                    If you don't know something,
                    simply say you don't know.
                    """
                ),
                (
                    "human",
                    "{question}"
                )   
            ]
        )