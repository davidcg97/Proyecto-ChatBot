"""
🤖 IT Support Chatbot - Interfaz Gradio
Chatbot con agente LangGraph + RAG para soporte IT
"""

import gradio as gr
from src.config import (
    GRADIO_SERVER_NAME, 
    GRADIO_SERVER_PORT, 
    GRADIO_SHARE,
    print_config
)

# Mostrar configuración al iniciar
print_config()

def chatbot_response(message: str, history: list) -> str:
    """
    Función que procesa el mensaje del usuario y devuelve la respuesta del agente.
    
    Args:
        message: Mensaje del usuario
        history: Historial de conversación en formato Gradio [(user, bot), ...]
    
    Returns:
        Respuesta del agente
    """
    try:
        # Importación lazy del agente (solo cuando se necesita)
        from src.agent.agent import query_agent
        
        # Convertir historial de Gradio a formato más simple si es necesario
        # Por ahora, solo procesamos el mensaje actual
        response = query_agent(message, chat_history=history)
        return response
    except Exception as e:
        error_msg = f"❌ Error al procesar la consulta: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg

# Ejemplos predefinidos para que el usuario pruebe
examples = [
    ["¿Cómo reseteo mi contraseña?"],
    ["¿Cómo me conecto a la VPN?"],
    ["No puedo acceder a FreeScout, ¿está funcionando?"],
    ["Mi PC va muy lento, ¿puedes revisarlo?"],
    ["¿Cuál es el estado de los contenedores Docker?"],
    ["Crea un ticket: Mi ordenador no arranca"],
    ["¿Cuál es el estado del ticket #1?"],
    ["¿Hay errores recientes en el sistema?"],
]

# Crear la interfaz de Gradio
with gr.Blocks(
    title="🤖 IT Support Assistant",
    theme=gr.themes.Soft(),
    css="""
        .gradio-container {
            max-width: 900px !important;
            margin: auto !important;
        }
        #chatbot {
            height: 500px !important;
        }
    """
) as demo:
    
    # Header
    gr.Markdown(
        """
        # 🤖 IT Support Assistant
        
        Asistente inteligente de soporte IT con:
        - 📚 Consulta de documentación (RAG)
        - 🎫 Creación y seguimiento de tickets
        - 🐳 Monitoreo de contenedores Docker
        - 🖥️ Diagnóstico del sistema Windows
        - 🔧 Verificación de servicios
        
        **¿En qué puedo ayudarte hoy?**
        """
    )
    
    # Chatbot interface
    chatbot = gr.Chatbot(
        label="Conversación",
        elem_id="chatbot",
        height=500,
        show_copy_button=True,
        type="messages"  # Nuevo formato OpenAI-style
    )
    
    # Input area
    with gr.Row():
        msg = gr.Textbox(
            label="Tu mensaje",
            placeholder="Escribe tu consulta aquí... (Ej: ¿Cómo reseteo mi contraseña?)",
            scale=4,
            lines=2,
        )
        submit_btn = gr.Button("Enviar 📤", variant="primary", scale=1)
    
    # Action buttons
    with gr.Row():
        clear_btn = gr.Button("🗑️ Limpiar Chat")
        retry_btn = gr.Button("🔄 Reintentar")
    
    # Examples
    gr.Examples(
        examples=examples,
        inputs=msg,
        label="💡 Ejemplos de consultas"
    )
    
    # Footer info
    gr.Markdown(
        """
        ---
        ### 📊 Información del Sistema
        - **LLM**: Llama 3.3 70B (Groq)
        - **Base de Conocimiento**: RAG con ChromaDB
        - **Tickets**: FreeScout Integration
        - **Monitoreo**: Docker + Windows System Diagnostics
        
        ℹ️ *Puedo ayudarte con problemas técnicos, verificar servicios, diagnosticar el sistema y crear tickets automáticamente.*
        """
    )
    
    # Event handlers
    def respond(message, chat_history):
        """Maneja la respuesta del chatbot"""
        if not message.strip():
            return "", chat_history
        
        # Obtener respuesta del agente
        bot_response = chatbot_response(message, chat_history)
        
        # Añadir al historial en formato OpenAI-style
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_response})
        
        return "", chat_history
    
    def clear_chat():
        """Limpia el historial del chat"""
        return None, []
    
    def retry_last():
        """Reintenta la última consulta"""
        return None  # Por ahora solo limpia, se puede mejorar
    
    # Conectar eventos
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(clear_chat, None, [msg, chatbot])
    
    # Welcome message
    demo.load(
        lambda: [{"role": "assistant", "content": "👋 ¡Hola! Soy tu asistente de soporte IT. ¿En qué puedo ayudarte hoy?"}],
        None,
        chatbot
    )

# Configuración de lanzamiento
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Iniciando IT Support Chatbot...")
    print("="*60)
    print(f"📍 URL Local: http://{GRADIO_SERVER_NAME}:{GRADIO_SERVER_PORT}")
    if GRADIO_SHARE:
        print("🌐 Compartido públicamente: Sí")
    print("="*60 + "\n")
    
    # Lanzar la aplicación
    demo.launch(
        server_name=GRADIO_SERVER_NAME,
        server_port=GRADIO_SERVER_PORT,
        share=GRADIO_SHARE,
        show_error=True,
        show_api=False,
    )
