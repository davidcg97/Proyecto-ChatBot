import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.tools.agent_tools import create_support_ticket, get_ticket_status
from src.tools.system_tools import get_system_performance, check_disk_space, check_network_connection
from src.rag.rag_retriever import get_relevant_docs
from src.config import LANGFUSE_ENABLED

load_dotenv()

# Verificar que existe la API key
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("❌ GROQ_API_KEY no encontrada en el archivo .env")

# Inicializar Langfuse CallbackHandler si está habilitado
langfuse_handler = None
if LANGFUSE_ENABLED:
    from langfuse.langchain import CallbackHandler
    langfuse_handler = CallbackHandler()
    print("✅ Langfuse tracing habilitado para LangChain")

# Configuración del LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=2048
)

# Tools disponibles
tools = [
    # Tickets
    create_support_ticket,
    get_ticket_status,
    # Sistema Windows
    get_system_performance,
    check_disk_space,
    check_network_connection
]

# System prompt
SYSTEM_PROMPT = """Eres un asistente de soporte IT llamado **IT Assistant** para una empresa.

**Tu misión**: Ayudar a los empleados con problemas técnicos, consultas sobre procedimientos IT y crear tickets cuando sea necesario.

**Capacidades**:
1. 📚 **Consultar documentación**: Tienes acceso a manuales y guías IT de la empresa
2. 🎫 **Gestión de tickets**: Puedes crear y consultar el estado de tickets en FreeScout
3. 🖥️ **Diagnóstico del sistema**: Puedes obtener información de CPU, RAM, disco y red del sistema Windows

**Herramientas disponibles**:
- **Tickets**: 
  * create_support_ticket(subject, description, priority) - Crea un nuevo ticket
  * get_ticket_status(ticket_number) - Consulta estado de un ticket. **MUY IMPORTANTE**: ticket_number debe ser un número entero (1, 2, 3), NO texto ("1", "#1")
- **Sistema**: get_system_performance, check_disk_space, check_network_connection

**IMPORTANTE sobre tickets**:
- Cuando el usuario pregunte por "mis tickets" o "estado de tickets", pregúntale el número específico
- SIEMPRE usa números enteros para get_ticket_status: get_ticket_status(1) ✅, NO get_ticket_status("1") ❌
- Si el usuario dice "ticket 1" o "ticket #1", extrae solo el número: 1

**Comportamiento**:
- Sé amable, profesional y claro
- Primero intenta resolver el problema con la información del manual
- Si el usuario reporta lentitud, usa get_system_performance para diagnosticar
- Si reporta problemas de espacio, usa check_disk_space
- Si hay problemas de red, usa check_network_connection
- **Cuando crees un ticket, SIEMPRE destaca el número de ticket** para que el usuario lo pueda consultar después
- Si no puedes resolver el problema, crea un ticket con toda la información recopilada
- Siempre confirma al usuario cuando realices acciones
- Responde en español de España

**Flujo de trabajo recomendado**:
1. **Lentitud del sistema** → get_system_performance → interpretar resultados
2. **Problemas de red** → check_network_connection → diagnosticar
3. **Consulta general** → Busca en el manual IT (RAG)
4. **Problema no resuelto** → create_support_ticket con toda la info recopilada

¡Adelante, ayuda a los usuarios!"""

# Crear el agente usando LangGraph
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

from langgraph.prebuilt import create_react_agent

# Crear agente sin modificador de estado (lo añadiremos en el mensaje)
agent_executor = create_react_agent(
    model=llm,
    tools=tools
)

def query_agent(user_message: str, chat_history: list = None) -> str:
    """
    Procesa una consulta del usuario usando el agente.
    
    Args:
        user_message: Mensaje del usuario
        chat_history: Historial de conversación (opcional)
    
    Returns:
        Respuesta del agente
    """
    # Primero intenta buscar en el RAG
    try:
        relevant_docs = get_relevant_docs(user_message, k=2)
        if relevant_docs:
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            enhanced_message = f"""Usuario pregunta: {user_message}

Contexto del manual IT:
{context}

Si la respuesta está en el contexto, úsala. Si no, usa tus herramientas."""
        else:
            enhanced_message = user_message
    except Exception as e:
        print(f"⚠️ Error al consultar RAG: {e}")
        enhanced_message = user_message
    
    # Invocar al agente con el system prompt
    try:
        # Preparar configuración con callbacks de Langfuse si está habilitado
        config = {}
        if langfuse_handler:
            config["callbacks"] = [langfuse_handler]
        
        response = agent_executor.invoke(
            {
                "messages": [
                    ("system", SYSTEM_PROMPT),
                    ("user", enhanced_message)
                ]
            },
            config=config
        )
        
        # Extraer la respuesta final
        if "messages" in response and len(response["messages"]) > 0:
            last_message = response["messages"][-1]
            # Manejar diferentes tipos de mensajes
            if hasattr(last_message, 'content'):
                return last_message.content
            else:
                return str(last_message)
        else:
            return "Lo siento, no pude procesar tu solicitud. Por favor, intenta de nuevo."
            
    except Exception as e:
        print(f"❌ Error en el agente: {e}")
        import traceback
        traceback.print_exc()
        return f"Ocurrió un error al procesar tu solicitud: {str(e)}"

if __name__ == "__main__":
    # Test del agente
    print("🤖 IT Assistant - Test")
    print("="*50)
    
    tests = [
        "¿Cómo reseteo mi contraseña?",
        "¿Está funcionando el servidor VPN?",
        "No puedo conectarme a la VPN, ayuda",
    ]
    
    for test in tests:
        print(f"\n👤 Usuario: {test}")
        response = query_agent(test)
        print(f"🤖 Asistente: {response}")
        print("-"*50)