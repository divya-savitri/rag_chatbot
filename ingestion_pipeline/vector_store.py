from langchain_community.vectorstores import FAISS
from utils.logger import logger

FAISS_INDEX_PATH = "faiss_index"


def create_vector_store(documents, embeddings):
    """
    Creates FAISS vector store from document chunks
    Used during ingestion
    """

    logger.info("Creating FAISS vector store")

    vectorstore = FAISS.from_documents(documents, embeddings)

    vectorstore.save_local(FAISS_INDEX_PATH)

    logger.info("FAISS index saved successfully")

    return vectorstore


def load_vectorstore():
    """
    Loads FAISS vector store
    Used during search pipeline
    """

    from langchain_community.embeddings import HuggingFaceEmbeddings

    logger.info("Loading FAISS vector store")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    logger.info("Vector store loaded successfully")

    return vectorstore