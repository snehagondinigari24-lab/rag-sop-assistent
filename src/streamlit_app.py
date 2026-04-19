import streamlit as st
import tempfile
import os
from query import ask_question_from_docs, build_db_from_pdf

st.set_page_config(page_title="Chat with PDF", page_icon="📄")
st.title("📄 Chat with PDF")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "db" not in st.session_state:
    st.session_state.db = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# Sidebar upload
st.sidebar.title("📂 Upload PDF")
uploaded_file = st.sidebar.file_uploader(
    "Choose any PDF", type=["pdf"]
)

if uploaded_file:
    if st.sidebar.button("📥 Process PDF"):
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".pdf"
            ) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            db = build_db_from_pdf(tmp_path)
            st.session_state.db = db
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.messages = []
            st.session_state.input_key += 1
            os.unlink(tmp_path)

        st.sidebar.success(
            f"✅ Ready! Ask questions about "
            f"{uploaded_file.name}"
        )

# Main area
if not st.session_state.db:
    st.info(
        "👈 Upload a PDF from the sidebar to start."
    )
else:
    st.caption(
        f"📖 Chatting with: **{st.session_state.pdf_name}**"
    )

    # Show chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(
                f"**🤖 Assistant:** {msg['content']}"
            )
        st.markdown("---")

    # Input
    query = st.text_input(
        "Ask your question:",
        key=f"q_{st.session_state.input_key}",
        placeholder="e.g. What are the working hours?"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        search = st.button("🔍 Search")
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.input_key += 1
            st.rerun()

    if search and query.strip():
        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.spinner("Searching..."):
            result = ask_question_from_docs(
                query, st.session_state.db
            )
            answer = result.get("answer", "Not found in  document")

        if "Not found in document" in answer:
            response = "⚠️ Not found in document"
        elif answer.startswith("Error:"):
            response = f"❌ {answer}"
        else:
            response = f"✅ {answer}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.input_key += 1
        st.rerun()