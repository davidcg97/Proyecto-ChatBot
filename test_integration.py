from src.tools.freescout_integration import get_freescout_db

print("🔄 Probando conexión con FreeScout...\n")

db = get_freescout_db()

result = db.create_ticket(
    subject="Prueba de integración desde Python",
    body="Este es un ticket de prueba para validar la integración con FreeScout."
)

print("="*60)
if result["success"]:
    print("✅ ÉXITO - Ticket creado correctamente")
    print(f"📋 Ticket ID: {result['ticket_id']}")
    print(f"📌 Asunto: {result['subject']}")
    print(f"⏰ Creado: {result['created_at']}")
    print(f"\n🌐 Ver en: http://localhost:8080/conversation/{result['ticket_id']}")
else:
    print("❌ ERROR al crear el ticket")
    print(f"Error: {result.get('error')}")
print("="*60)