from langchain_community.document_loaders import PyPDFLoader
import os
import re
from utils.logger import logger


def load_pdfs(pdf_folder):

    documents = []

    logger.info("Starting PDF loading")

    for file in os.listdir(pdf_folder):

        if file.endswith(".pdf"):

            path = os.path.join(pdf_folder, file)

            loader = PyPDFLoader(path)
            docs = loader.load()

            for doc in docs:

                # Clean text
                text = re.sub(r"\s+", " ", doc.page_content)
                doc.page_content = text.strip()

                # Add consistent metadata
                doc.metadata["source"] = file
                doc.metadata["page"] = doc.metadata.get("page", 0)

            documents.extend(docs)

            logger.info(f"Loaded {file} with {len(docs)} pages")

    logger.info(f"Total documents loaded: {len(documents)}")

    return documents