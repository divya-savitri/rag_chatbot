import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from search_pipeline.run_search import run_query


st.set_page_config(layout="wide")

PDF_FOLDER = "all_pdfs"


if "messages" not in st.session_state:
    st.session_state.messages = []


# ================= SIDEBAR =================

with st.sidebar:

    st.title("📚 Assistant Menu")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")

    with st.expander("📄 Source Files"):

        if os.path.exists(PDF_FOLDER):

            for f in os.listdir(PDF_FOLDER):

                if f.endswith(".pdf"):
                    st.write(f"📑 {f}")

    st.markdown("---")

    with st.expander("ℹ️ About System"):

        st.markdown("""
### 🤖 Intelligent Teacher Assistant

This system uses **Retrieval Augmented Generation (RAG)**.

### ⚙️ Workflow

1️⃣ Question → converted into embeddings  
2️⃣ Retriever → finds relevant document chunks  
3️⃣ LLM → generates structured answer  

### 📌 Features

✔ Document based answers  
✔ Shows sources and chunks  
✔ Maintains conversation context  
✔ General knowledge fallback
""")


# ================= MAIN TITLE =================

st.title("🤖 Intelligent Teacher Assistant")


# ================= FORMAT ANSWER =================

def format_answer(answer):

    sections = answer.split("###")

    html = ""

    for sec in sections:

        if sec.strip() == "":
            continue

        lines = sec.strip().split("\n")

        title = lines[0]
        body = "\n".join(lines[1:])

        html += f"""
<div style="margin-top:18px;color:black">

<div style="font-size:22px;font-weight:bold;">
📌 {title}
</div>

<div style="font-size:17px;margin-top:6px;line-height:1.6;">
{body}
</div>

</div>
"""

    return html


# ================= DISPLAY CHAT =================

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(f"""
<div style="display:flex; justify-content:flex-end; margin-top:25px">

<div style="font-size:30px;margin-right:10px">👤</div>

<div style="padding:14px;
font-size:17px;
max-width:60%;
color:black;">
{msg["content"]}
</div>

</div>
""", unsafe_allow_html=True)

    else:

        if msg["status"] == "rag":
            formatted = format_answer(msg["content"])
        else:
            formatted = f"<div style='font-size:17px;color:black'>{msg['content']}</div>"

        st.markdown(f"""
<div style="display:flex; justify-content:flex-start; margin-top:25px">

<div style="font-size:32px;margin-right:10px">🤖</div>

<div style="padding:16px;
max-width:70%;">
{formatted}
</div>

</div>
""", unsafe_allow_html=True)

        if msg["status"] == "rag" and msg["sources"]:

            with st.expander("📚 Sources"):

                for s in msg["sources"]:
                    st.write(f"📄 {s['source']} — page {s['page']}")

            with st.expander("📑 Top Retrieved Chunks"):

                for s in msg["sources"]:

                    st.write(f"📄 Source: {s['source']}")
                    st.write(f"📍 Page: {s['page']}")
                    st.write(f"📊 Similarity Score: {round(s['score'],4)}")
                    st.write(s["content"])
                    st.markdown("---")


# ================= USER INPUT =================

prompt = st.chat_input("💬 Ask your question...")


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
    )

    # detect previous assistant status
    previous_status = None

    for m in reversed(st.session_state.messages):
        if m["role"] == "assistant":
            previous_status = m.get("status")
            break

    result = run_query(prompt, history, previous_status)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
        "status": result["status"]
    })

    st.rerun()


# ================= AUTO SCROLL =================

st.markdown(
"""
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
""",
unsafe_allow_html=True
)