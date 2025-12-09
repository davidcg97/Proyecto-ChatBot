from langchain.tools import tool
from typing import Union
from src.tools.freescout_integration import get_freescout_db

@tool
def create_support_ticket(subject: str, description: str, priority: str = "normal") -> str:
    """
    Crea un ticket de soporte en el sistema FreeScout.
    Utiliza esta herramienta cuando el usuario tenga un problema que no puedas resolver 
    directamente o cuando necesite ayuda técnica especializada.
    
    Args:
        subject: Título breve y descriptivo del problema (máximo 100 caracteres)
        description: Descripción detallada del problema del usuario
        priority: Prioridad del ticket: "low", "normal", "high" (por defecto "normal")
    
    Returns:
        Confirmación con el número de ticket creado y enlace
    """
    priority_map = {"low": 1, "normal": 2, "high": 3}
    priority_num = priority_map.get(priority.lower(), 2)
    
    db = get_freescout_db()
    result = db.create_ticket(subject, description, priority=priority_num)
    
    if result["success"]:
        return f"""✅ **Ticket creado exitosamente**

╔══════════════════════════════════════╗
║  🎫 NÚMERO DE TICKET: #{result['number']}  ║
╚══════════════════════════════════════╝

📋 **Resumen del Ticket:**
• **Asunto**: {result['subject']}
• **ID Interno**: {result['ticket_id']}
• **Fecha de Creación**: {result['created_at']}
• **Estado**: Activo
• **Prioridad**: {priority.upper()}

📝 **Descripción**: 
{description[:200]}{'...' if len(description) > 200 else ''}

🔗 **Ver en FreeScout**: http://localhost:8080/conversation/{result['ticket_id']}

✨ **Para consultar el estado de este ticket**, pregúntame:
   "¿Cuál es el estado del ticket {result['number']}?"

Un técnico del equipo de IT revisará tu solicitud pronto. Recibirás actualizaciones por correo electrónico."""
    else:
        return f"❌ Error al crear el ticket: {result.get('error', 'Error desconocido')}. Por favor, contacta directamente con IT."


@tool
def get_ticket_status(ticket_number: int) -> str:
    """
    Consulta el estado de un ticket existente en el sistema.
    IMPORTANTE: El ticket_number debe ser un número entero (ejemplo: 1, 2, 3), NO texto.
    
    Args:
        ticket_number: Número del ticket a consultar (debe ser un entero como 1, 2, 3, etc.)
    
    Returns:
        Estado actual del ticket con todos sus detalles
    
    Ejemplo de uso correcto:
        - get_ticket_status(1)  ✅
        - get_ticket_status(42) ✅
    
    Ejemplo de uso incorrecto:
        - get_ticket_status("1")  ❌
        - get_ticket_status("#1") ❌
    """
    db = get_freescout_db()
    ticket = db.get_ticket_by_number(ticket_number)
    
    if ticket:
        status_emoji = {
            "Activo": "🔵",
            "Pendiente": "🟡",
            "Cerrado": "🟢"
        }
        emoji = status_emoji.get(ticket['status'], "⚪")
        
        return f"""📋 **Estado del Ticket #{ticket['number']}**:

{emoji} **Estado**: {ticket['status']}
📌 **Asunto**: {ticket['subject']}
📝 **Descripción**: {ticket['description']}
📧 **Email**: {ticket['customer_email']}
⏰ **Creado**: {ticket['created_at']}
🔄 **Última actualización**: {ticket['updated_at']}

🔗 Ver detalles completos: http://localhost:8080/conversation/{ticket['ticket_id']}
"""
    else:
        return f"❌ No se encontró el ticket #{ticket_number}. Verifica el número e intenta nuevamente."