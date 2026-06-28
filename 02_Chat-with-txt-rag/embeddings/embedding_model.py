from sentence_transformers import SentenceTransformer
from config import Config


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            documents,
            convert_to_tensor=False,
            convert_to_numpy=True
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        embedding = self.model.encode(
            query,
            convert_to_tensor=False,
            convert_to_numpy=True
        )
        return embedding.tolist()