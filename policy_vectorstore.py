"""
Utility to create/load FAISS vectorstore for the policy PDF.
Run this file once to create the vectorstore. Later, just load it.
"""

import os
from langchain.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.document_loaders import PyPDFLoader

VECTORSTORE_PATH = "data/policy_faiss_index"
PDF_PATH = "data/leave_policy.pdf"


def create_and_save_vectorstore():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load_and_split()
    embeddings = OllamaEmbeddings(model="mistral")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"Vectorstore created and saved to {VECTORSTORE_PATH}")


def load_vectorstore():
    if not os.path.exists(VECTORSTORE_PATH):
        raise FileNotFoundError(f"Vectorstore not found: {VECTORSTORE_PATH}. Run create_and_save_vectorstore() first.")
    embeddings = OllamaEmbeddings(model="mistral")
    return FAISS.load_local(VECTORSTORE_PATH, embeddings)

if __name__ == "__main__":
    create_and_save_vectorstore()
