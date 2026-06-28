import chromadb
from config import Config

class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PATH
        )
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME
        )
    def add_documents(
        self,
        chunks,
        embeddings,
        metadata
    ):

        ids = [
            f"doc_{i}"
            for i in range(len(chunks))
        ]
        metadatas = [
            metadata
            for _ in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding,
        top_k=3
    ):

        return self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )