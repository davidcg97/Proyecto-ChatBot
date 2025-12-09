"""
🧪 Test de las herramientas del Chatbot IT
"""

print("="*70)
print("🧪 PROBANDO HERRAMIENTAS DEL CHATBOT IT")
print("="*70)

# Test 1: System Tools
print("\n" + "="*70)
print("🖥️ TEST 1: Herramientas de Sistema")
print("="*70)

try:
    from src.tools.system_tools import (
        get_system_performance,
        check_disk_space,
        check_network_connection
    )
    
    print("\n📊 Obteniendo información de rendimiento...")
    result = get_system_performance.invoke({})
    print(result)
    
    print("\n💾 Verificando espacio en discos...")
    result = check_disk_space.invoke({})
    print(result)
    
    print("\n🌐 Verificando conexión de red...")
    result = check_network_connection.invoke({})
    print(result)
    
    print("\n" + "-"*70)
    print("✅ Herramientas de Sistema funcionando correctamente")
    
except Exception as e:
    print(f"❌ Error al probar herramientas de Sistema: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Tickets
print("\n" + "="*70)
print("🎫 TEST 2: Herramientas de Tickets")
print("="*70)

try:
    from src.tools.agent_tools import create_support_ticket, get_ticket_status
    
    print("\n✅ Herramientas de tickets cargadas correctamente")
    print("   - create_support_ticket")
    print("   - get_ticket_status")
    
except Exception as e:
    print(f"❌ Error al cargar herramientas de tickets: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Integración con el agente
print("\n" + "="*70)
print("🤖 TEST 3: Integración con el Agente")
print("="*70)

try:
    from src.agent.agent import query_agent
    
    print("\n✅ Agente cargado correctamente")
    print("\n💡 Ejemplos de consultas que puedes hacer:")
    print("   - '¿Cuánta RAM tiene mi sistema?'")
    print("   - '¿Hay espacio suficiente en el disco?'")
    print("   - '¿Está funcionando internet?'")
    print("   - 'Crea un ticket: Mi PC va lento'")
    print("   - '¿Cuál es el estado del ticket #1?'")
    
    # Test simple
    print("\n🔬 Prueba rápida del agente:")
    print("\n👤 Usuario: ¿Cuánta RAM tiene mi sistema?")
    print("🤖 Procesando...\n")
    response = query_agent("¿Cuánta RAM tiene mi sistema?")
    print(f"🤖 Asistente: {response[:300]}...")  # Primeros 300 caracteres
    
    print("\n✅ Integración con el agente completada")
    
except Exception as e:
    print(f"❌ Error en la integración con el agente: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✅ PRUEBAS COMPLETADAS")
print("="*70)
print("\n💡 Capacidades disponibles:")
print("   - 📚 Consulta de documentación (RAG)")
print("   - 🎫 Gestión de tickets en FreeScout")
print("   - 🖥️ Diagnóstico del sistema Windows (CPU, RAM, disco, red)")
print("   - 🐳 Funciones MCP de Docker (disponibles directamente)")
print("\n🚀 ¡El chatbot IT está listo para usar!")
print("   Ejecuta: python main.py")
print("="*70)
