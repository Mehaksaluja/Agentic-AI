from embeddings.embedding_model import (
    EmbeddingModel
)
from vectordb.chroma_manager import (
    ChromaManager
)


class Retriever:
    def __init__(self):
        self.embedding_model = (
            EmbeddingModel()
        )
        self.vector_db = (
            ChromaManager()
        )
    def retrieve(
        self,
        query,
        top_k=3
    ):

        query_embedding = (
            self.embedding_model
            .embed_query(query)
        )

        results = self.vector_db.search(
            query_embedding,
            top_k
        )
        return results["documents"][0]