from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import CHROMA_DIR, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL

def load_vectordb():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings
    )
    return vectordb

def get_relevant_docs(query, k=3):
    vectordb = load_vectordb()
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    return docs