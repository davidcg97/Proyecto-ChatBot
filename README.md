# 🤖 IT Support Chatbot con LangGraph y RAG

Sistema de asistente IT inteligente que combina:
- **LangGraph** para agentes conversacionales
- **RAG (Retrieval-Augmented Generation)** con ChromaDB
- **Groq + Llama 3.3 70B** como LLM (gratuito, rápido)
- **FreeScout** para gestión de tickets

## 📋 Características

- ✅ Consulta documentación IT mediante RAG
- ✅ Crea tickets automáticamente en FreeScout
- ✅ Consulta estado de tickets
- ✅ **🐳 Monitoreo y gestión de contenedores Docker**
- ✅ **🖥️ Diagnóstico del sistema Windows (CPU, RAM, disco, red)**
- ✅ **🔧 Verificación de servicios de Windows**
- ✅ **⚠️ Análisis de errores del sistema**
- ✅ Interfaz Gradio

## 🛠️ Requisitos

- Python 3.10+
- Docker y Docker Compose
- **API Key de Groq (gratis)** - [Obténla aquí](https://console.groq.com/)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repo>
cd Proyecto
```

### 2. Crear entorno virtual
```bash
python -m venv proyecto_chatbot
.\proyecto_chatbot\Scripts\Activate.ps1  # Windows
source proyecto_chatbot/bin/activate      # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

### 5. Levantar servicios Docker
```bash
docker-compose up -d
```

## 📁 Estructura del Proyecto

```
Proyecto/
├── src/
│   ├── agent/          # Agente LangGraph
│   ├── rag/            # Sistema RAG
│   ├── tools/          # Herramientas del agente
│   └── config.py       # Configuración centralizada
├── data/               # Datos de FreeScout
├── db_data/            # Datos de MySQL
├── docker-compose.yaml # Servicios Docker
├── requirements.txt    # Dependencias Python
└── .env                # Variables de entorno
```

## 🔧 Configuración

Edita el archivo `.env`:

```bash
# API Key de Groq (gratis en console.groq.com)
GROQ_API_KEY=gsk_tu_api_key_aqui

# LLM Configuration
LLM_MODEL=gemma2-9b-it
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2048

# MySQL / FreeScout
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=freescout
MYSQL_PASSWORD=freescout_password
MYSQL_DATABASE=freescout

# ChromaDB
CHROMA_DIR=./data/CHROMA_DB
CHROMA_COLLECTION_NAME=manual_it

# Gradio
GRADIO_SERVER_PORT=7860
```

## 📚 Crear índice RAG

Para indexar tu documentación IT:

```bash
python src/rag/build_index.py --source "ruta/a/tu/manual.pdf"
```

Formatos soportados: PDF, TXT, MD

## 🧪 Pruebas

### Test de integración
```bash
python test_integration.py
```

### Test del agente
```bash
python src/agent/agent.py
```

## 🌐 Acceso a FreeScout

- URL: http://localhost:8080
- Usuario: admin@example.com
- Contraseña: admin123

## 📊 Monitoreo (Opcional)

Para habilitar LangSmith tracing:

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=tu_langsmith_api_key
LANGSMITH_PROJECT=chatbot-it
```

## 🐛 Debugging

Activa el modo debug en `.env`:
```bash
DEBUG_MODE=true
```

## 📝 Uso del Agente

```python
from src.agent.agent import query_agent

# Hacer una consulta
respuesta = query_agent("¿Cómo reseteo mi contraseña?")
print(respuesta)
```

## 🔒 Seguridad

- ⚠️ **NUNCA** subas el archivo `.env` al repositorio
- ⚠️ Usa `.env.example` como plantilla
- ⚠️ Cambia las contraseñas por defecto en producción

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso interno.

## 👥 Autores

- David - Desarrollo principal

## 🆘 Soporte

Para problemas o preguntas, abre un issue en el repositorio.
