import argparse
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_document(path):
    ext = path.lower()

    if ext.endswith(".pdf"):
        return PyPDFLoader(path).load()
    elif ext.endswith(".txt"):
        return TextLoader(path).load()
    elif ext.endswith(".md"):
        return UnstructuredMarkdownLoader(path).load()
    else:
        raise ValueError("Formato no soportado. Usa PDF, TXT o MD.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Ruta del documento IT")
    parser.add_argument("--chroma-dir", default="CHROMA_DB", help="Directorio donde guardar Chroma")
    parser.add_argument("--collection-name", default="manual_it", help="Nombre de la colección")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--chunk-overlap", type=int, default=50)
    args = parser.parse_args()

    print("📄 Cargando documento...")
    docs = load_document(args.source)

    print("✂️ Dividiendo en chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )
    chunks = splitter.split_documents(docs)

    print("🧠 Cargando embeddings locales (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("📦 Creando base vectorial Chroma...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=args.collection_name,
        persist_directory=args.chroma_dir
    )

    db.persist()
    print("✅ Índice creado correctamente en:", args.chroma_dir)

if __name__ == "__main__":
    main()