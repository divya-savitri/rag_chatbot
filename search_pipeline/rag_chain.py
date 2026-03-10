from langchain.prompts import PromptTemplate
from search_pipeline.llm import get_llm


def build_rag_chain(vectorstore):

    llm = get_llm()

    rag_prompt = PromptTemplate(
        input_variables=["context", "question", "history"],
        template="""
You are an academic assistant.

Use the document context and conversation history to answer.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer in this structure:

### Definition
Clear definition.

### Explanation
Explain in 3–4 sentences.

### Key Points
- point
- point
- point

### Example
Provide example if possible.

### Conclusion
One sentence summary.
"""
    )

    def rag_pipeline(inputs):

        query = inputs["query"]
        history = inputs.get("history", "")
        previous_status = inputs.get("previous_status", None)

        # ================= GENERAL MODE CONTINUATION =================

        if previous_status == "general":

            response = llm.invoke(
                f"""
Continue the conversation naturally.

Conversation history:
{history}

User question:
{query}
"""
            )

            return {
                "status": "general",
                "answer": response.content,
                "sources": []
            }

        # ================= RETRIEVAL =================

        results = vectorstore.similarity_search_with_score(query, k=5)

        docs = [r[0] for r in results]
        scores = [r[1] for r in results]

        best_score = scores[0] if scores else 999

        SIMILARITY_THRESHOLD = 1.2

        # ================= OUTSIDE DOCUMENT =================

        if best_score > SIMILARITY_THRESHOLD:

            response = llm.invoke(
                f"""
Answer the question using general knowledge.

Conversation history:
{history}

User question:
{query}
"""
            )

            return {
                "status": "general",
                "answer": f"**This question is outside the uploaded documents.**\n\n{response.content}",
                "sources": []
            }

        # ================= RAG ANSWER =================

        context = "\n\n".join([doc.page_content for doc in docs])

        sources = []

        for i, doc in enumerate(docs):

            sources.append({
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "N/A"),
                "content": doc.page_content[:400],
                "score": scores[i]
            })

        prompt = rag_prompt.format(
            context=context,
            question=query,
            history=history
        )

        response = llm.invoke(prompt)

        return {
            "status": "rag",
            "answer": response.content,
            "sources": sources
        }

    return rag_pipeline