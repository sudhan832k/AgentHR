
import os
from langchain.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

def policy_query_tool(query: str) -> str:
    print("[INFO] policy_query_tool invoked.")
    # Path to the FAISS index
    faiss_index_path = os.path.join(os.path.dirname(__file__), '../data/policy_faiss_index')

    # Only load FAISS vectorstore; do not create it here
    if not os.path.exists(faiss_index_path):
        return "Policy vectorstore not found. Please run policy_vectorstore.py to create it first."
    db = FAISS.load_local(faiss_index_path, OllamaEmbeddings(model="mistral"), allow_dangerous_deserialization=True)

    # Retrieve relevant chunks
    print("[INFO] Performing similarity search.")
    relevant_docs = db.similarity_search(query, k=3)
    print(f"[INFO] Found {len(relevant_docs)} relevant documents.")
    context = "\n".join([doc.page_content for doc in relevant_docs])

    # Use LLM to answer based on context
    llm = OllamaLLM(model="mistral")
    prompt = f"Answer the following question using only the context below. If the answer is not in the context, say you don't know.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    answer = llm.invoke(prompt)
    return answer.strip()
