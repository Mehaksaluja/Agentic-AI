from retrieval.retriever import (
    Retriever
)
from prompts.rag_prompt import (
    build_prompt
)
from llm.groq_client import (
    GroqClient
)

class RAGService:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = GroqClient()
    def ask(
        self,
        question
    ):
        chunks = self.retriever.retrieve(
            question
        )
        prompt = build_prompt(
            chunks,
            question
        )

        return self.llm.generate(
            prompt
        )