from prompts.chatbot_prompt import (
    ChatbotPrompt
)
from models.llm import (
    LLMFactory
)
from chains.parser import (
    OutputParserFactory
)

class ChatbotChain:

    @staticmethod
    def create():
        prompt = ChatbotPrompt.create()
        llm = LLMFactory.create()
        parser = OutputParserFactory.create()
        chain = ( prompt | llm | parser )
        return chain