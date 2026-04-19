import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore", "faiss_index")

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

query = "what are the working hours"
results = db.similarity_search_with_score(query, k=8)

print("\n=== TOP CHUNKS FOUND ===")
for i, (doc, score) in enumerate(results):
    print(f"\n--- Chunk {i+1} | Score: {score:.4f} ---")
    print(doc.page_content)
    print()