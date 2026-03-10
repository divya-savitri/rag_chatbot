from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import logger

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=120,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = i
        chunk.metadata["length"] = len(chunk.page_content)

    logger.info(f"Total chunks created: {len(chunks)}")

    return chunks