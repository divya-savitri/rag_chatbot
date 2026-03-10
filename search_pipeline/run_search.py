import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion_pipeline.vector_store import load_vectorstore
from search_pipeline.rag_chain import build_rag_chain


vectorstore = load_vectorstore()

rag_chain = build_rag_chain(vectorstore)


def run_query(query, history, allow_general=False):

    result = rag_chain({
        "query": query,
        "history": history,
        "allow_general": allow_general
    })

    return result