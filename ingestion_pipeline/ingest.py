from ingestion_pipeline.loader import load_pdfs
from ingestion_pipeline.splitter import split_documents
from ingestion_pipeline.embedder import get_embeddings
from ingestion_pipeline.vector_store import create_vector_store
from utils.logger import logger
import os

PDF_FOLDER = "all_pdfs"


def run_ingestion():

    logger.info("Starting ingestion pipeline")

    print("Loading PDFs...")
    docs = load_pdfs(PDF_FOLDER)

    print("Splitting documents...")
    chunks = split_documents(docs)

    print("Creating embeddings...")
    embeddings = get_embeddings()

    print("Creating vector database...")
    create_vector_store(chunks, embeddings)

    logger.info("Ingestion completed successfully")

    print("✅ Ingestion Completed!")


if __name__ == "__main__":
    run_ingestion()