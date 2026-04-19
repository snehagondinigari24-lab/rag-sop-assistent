from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

NOT_FOUND = "Not found in document"

TYPO_MAP = {
    "attendence": "attendance",
    "attendace": "attendance",
    "recruitment": "recruitment",
    "employe": "employee",
    "emplyee": "employee",
    "leve": "leave",
    "sallary": "salary",
    "polcy": "policy",
    "poicy": "policy",
    "houres": "hours",
    "hourse": "hours",
    "stategies": "strategies",
    "startgies": "strategies",
    "prepration": "preparation",
    "resignation": "resignation",
    "terminaion": "termination",
    "exmas": "exams",
    "perfomance": "performance",
    "tpes": "types",
    "typ": "types"
}


def build_db_from_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". "]
    )

    docs = splitter.split_documents(documents)

    print(f"\n=== TOTAL CHUNKS: {len(docs)} ===")
    for i, d in enumerate(docs):
        print(f"Chunk {i}: {d.page_content[:100]}")

    db = FAISS.from_documents(docs, embeddings)
    return db


def fix_query(query: str) -> str:
    words = query.lower().strip().split()
    fixed = [TYPO_MAP.get(w, w) for w in words]
    return " ".join(fixed)


def clean_text(text: str) -> str:
    """Remove noise from chunk text."""
    lines = text.split("\n")
    clean = []

    for line in lines:
        line = line.strip()

        # Remove numbering like "1. "
        line = re.sub(r"^\d+\.\s*", "", line).strip()

        if not line or len(line) < 5:
            continue

        # Skip page headers
        if re.search(r"-\s*page\s*\d+", line.lower()):
            continue

        # Skip example lines
        if line.lower().startswith("example"):
            continue

        # Skip appendix garbage
        if "might ask" in line.lower():
            continue

        clean.append(line)

    return "\n".join(clean).strip()


def ask_question_from_docs(query: str, db) -> dict:
    try:
        # Step 1: Fix typos
        fixed = fix_query(query)
        print(f"\n=== QUERY: '{query}' -> '{fixed}' ===")

        # Step 2: Search
        results = db.similarity_search_with_score(fixed, k=5)

        print("\n=== ALL SCORES ===")
        for doc, score in results:
            print(f"{score:.4f} | {doc.page_content[:80]}")

        if not results:
            return {"answer": NOT_FOUND}

        # Step 3: Extract keywords
        query_words = [
            w for w in fixed.split()
            if len(w) > 2 and w not in {
                "what", "are", "the", "is", "how",
                "does", "for", "give", "tell", "about",
                "and", "or", "of", "in", "a", "an",
                "do", "me", "to", "at", "its"
            }
        ]

        print(f"=== SEARCH WORDS: {query_words} ===")

        best_doc = None
        best_score = None

        for doc, score in results:
            content_lower = doc.page_content.lower()

            word_hits = sum(
                1 for w in query_words if w in content_lower
            )

            print(f"Hits={word_hits} Score={score:.4f} | {doc.page_content[:60]}")

            if word_hits > 0:
                if best_doc is None:
                    best_doc = doc
                    best_score = score
                elif word_hits > sum(
                    1 for w in query_words
                    if w in best_doc.page_content.lower()
                ):
                    best_doc = doc
                    best_score = score

        # Step 4: No match
        if best_doc is None:
            print("=== NO MATCH FOUND ===")
            return {"answer": NOT_FOUND}

        # Step 5: Score filter
        if best_score > 1.9:
            print(f"=== SCORE {best_score} TOO HIGH ===")
            return {"answer": NOT_FOUND}

        # Step 6: Clean text
        cleaned = clean_text(best_doc.page_content)
        print(f"\n=== BEST CHUNK ===\n{cleaned}\n")

        if not cleaned or len(cleaned) < 15:
            return {"answer": NOT_FOUND}

        # Step 7: Sentence split
        sentences = [
            s.strip()
            for s in cleaned.replace("\n", " ").split(".")
            if len(s.strip()) > 5
        ]

        if not sentences:
            return {"answer": NOT_FOUND}

        # Step 8: Pick relevant
        relevant = []
        for s in sentences:
            hits = sum(1 for w in query_words if w in s.lower())
            if hits > 0:
                relevant.append((hits, s))

        if not relevant:
            answer = ". ".join(sentences[:2]) + "."
        else:
            relevant.sort(reverse=True)
            top = [s for _, s in relevant[:2]]
            answer = ". ".join(top) + "."

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}


def ask_question(query: str) -> dict:
    db = FAISS.load_local(
        "vectorstore/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return ask_question_from_docs(query, db)