"""
Configuración centralizada del proyecto
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ==================== API KEYS ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validación de API keys requeridas
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY no encontrada en el archivo .env")

# ==================== LLM CONFIGURATION (GROQ + GEMMA) ====================
LLM_MODEL = os.getenv("LLM_MODEL", "gemma2-9b-it")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))

# ==================== MYSQL / FREESCOUT ====================
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "freescout")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "freescout_password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "freescout")

# ==================== CHROMADB / RAG ====================
CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/CHROMA_DB")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "manual_it")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# ==================== RAG PARAMETERS ====================
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "2"))

# ==================== GRADIO ====================
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"

# ==================== LANGFUSE (OPCIONAL) ====================
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", None)
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", None)
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
LANGFUSE_ENABLED = bool(LANGFUSE_SECRET_KEY and LANGFUSE_PUBLIC_KEY)

if LANGFUSE_ENABLED:
    print("✅ Langfuse tracing habilitado")

# ==================== DEFAULT CUSTOMER ====================
DEFAULT_CUSTOMER_EMAIL = os.getenv("DEFAULT_CUSTOMER_EMAIL", "usuario@empresa.local")
DEFAULT_CUSTOMER_NAME = os.getenv("DEFAULT_CUSTOMER_NAME", "Usuario IT")

# ==================== SISTEMA ====================
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

def print_config():
    """Muestra la configuración actual (sin datos sensibles)"""
    print("="*60)
    print("🔧 CONFIGURACIÓN DEL SISTEMA")
    print("="*60)
    print(f"🤖 LLM: {LLM_MODEL} (Groq)")
    print(f"🌡️  Temperatura: {LLM_TEMPERATURE}")
    print(f"🗄️  MySQL Host: {MYSQL_HOST}:{MYSQL_PORT}")
    print(f"📦 ChromaDB: {CHROMA_DIR}")
    print(f"🧠 Embedding Model: {EMBEDDING_MODEL}")
    print(f"📊 RAG Top-K: {RAG_TOP_K}")
    print(f"🌐 Gradio: {GRADIO_SERVER_NAME}:{GRADIO_SERVER_PORT}")
    print(f"🔍 Langfuse: {'Habilitado' if LANGFUSE_ENABLED else 'Deshabilitado'}")
    print(f"🐛 Debug Mode: {'Habilitado' if DEBUG_MODE else 'Deshabilitado'}")
    print("="*60)

if __name__ == "__main__":
    print_config()
