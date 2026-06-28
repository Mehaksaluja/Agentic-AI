from loaders.txt_loader import TextLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.splitter import TextSplitter

from embeddings.embedding_model import EmbeddingModel

from vectordb.chroma_manager import ChromaManager

from services.rag_service import RAGService

from utils.logger import logger


DATA_PATH = "data/notes.txt"


def build_vector_database():

    logger.info("Loading document...")

    loader = TextLoader(DATA_PATH)

    document = loader.load()

    logger.info("Cleaning document...")

    cleaned_text = TextCleaner.clean(
        document.page_content
    )

    logger.info("Splitting document...")

    splitter = TextSplitter()

    chunks = splitter.split(cleaned_text)

    logger.info(
        f"Generated {len(chunks)} chunks."
    )

    embedding_model = EmbeddingModel()

    logger.info("Creating embeddings...")

    embeddings = embedding_model.embed_documents(
        chunks
    )

    logger.info("Connecting ChromaDB...")

    vector_db = ChromaManager()

    existing_docs = vector_db.collection.count()

    if existing_docs == 0:

        logger.info(
            "Indexing document..."
        )

        vector_db.add_documents(

            chunks,

            embeddings,

            document.metadata

        )

        logger.info(
            "Document indexed successfully."
        )

    else:

        logger.info(
            "Database already indexed."
        )


def main():

    build_vector_database()

    rag = RAGService()

    print("\n")

    print("=" * 60)

    print("      CHAT WITH TXT (RAG FROM SCRATCH)")

    print("=" * 60)

    print()

    print("Type 'exit' to quit.\n")

    while True:

        question = input("You : ")

        if question.lower() == "exit":
            break

        answer = rag.ask(question)

        print()

        print("Assistant :")

        print(answer)

        print()


if __name__ == "__main__":
    main()