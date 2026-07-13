# 💄 MK Sales Assistant

## Proyecto Final – IA Generativa

**Autor:** María Camila Rueda Cano

**UUID:** 13b680f7-1453-4155-a4d7-6b066c804b20

---

# Descripción

MK Sales Assistant es un asistente inteligente especializado en productos Mary Kay, desarrollado utilizando Inteligencia Artificial Generativa.

El proyecto implementa la arquitectura **Retrieval-Augmented Generation (RAG)** para responder preguntas utilizando únicamente la información almacenada en una base de conocimiento construida a partir de documentos oficiales y una base de clientes.

El asistente es capaz de:

- Recomendar productos Mary Kay.
- Consultar información del catálogo.
- Responder preguntas sobre rutinas de cuidado facial.
- Consultar información de clientes almacenada en la base de conocimiento.
- Mantener conversaciones utilizando memoria mediante LangGraph.

---

# Dominio elegido

El dominio seleccionado corresponde a **productos Mary Kay y gestión de clientes**.

La base de conocimiento fue construida utilizando:

- Catálogo de productos Mary Kay.
- Documento con información de productos.
- Base de datos de clientes en formato Excel.

---

# Tecnologías utilizadas

- Python
- Google Gemini
- LangChain
- LangGraph
- ChromaDB
- HuggingFace Embeddings
- Streamlit
- Pandas

---

# Arquitectura del proyecto

El flujo general del sistema es el siguiente:

1. Carga de documentos PDF y Excel.
2. División del contenido mediante Chunking.
3. Generación de Embeddings.
4. Almacenamiento en ChromaDB.
5. Recuperación de información (Retriever).
6. Construcción del contexto.
7. Consulta al modelo Gemini.
8. Generación de la respuesta.
9. Memoria conversacional mediante LangGraph.

---

# Estructura del proyecto

```
MK-Sales-Assistant/

│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── catalogo.pdf
│   ├── experta_producto.pdf
│   └── clientes.xlsx
│
├── chroma_db/
│
└── Proyecto_Final_IA.ipynb
```

---

# Instalación

Clonar el repositorio:

```bash
git clone https://github.com/camilaru15/MK-Sales-Assistant.git

cd MK-Sales-Assistant
```

Crear entorno virtual:

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# Configuración

Crear un archivo llamado:

```
.env
```

Agregar la API Key de Google Gemini:

```env
GOOGLE_API_KEY=TU_API_KEY
```

**Importante:** Nunca subir este archivo al repositorio.

---

# Ejecución del Notebook

Abrir Jupyter Notebook y ejecutar todas las celdas:

```
Proyecto_Final_IA.ipynb
```

---

# Ejecución de la aplicación

Desde la terminal ejecutar:

```bash
streamlit run app.py
```

La aplicación abrirá automáticamente en:

```
http://localhost:8501
```

---

# Justificación del System Prompt

El agente fue diseñado para actuar como una asesora virtual especializada en productos Mary Kay.

El System Prompt establece que el modelo debe:

- Responder únicamente utilizando el contexto recuperado desde la base vectorial.
- No inventar información.
- Responder en español.
- Mantener un tono profesional y amable.
- Indicar cuando la información solicitada no está disponible en la base de conocimiento.

Estas restricciones permiten disminuir las alucinaciones del modelo y asegurar que las respuestas estén fundamentadas en la información disponible.

---

# Funcionalidades implementadas

✅ Base vectorial con ChromaDB

✅ Recuperación de información mediante RAG

✅ Modelo Gemini

✅ Agente construido con LangGraph

✅ Memoria conversacional

✅ Chat interactivo

✅ Aplicación en Streamlit

---

# Dependencias principales

- streamlit
- langchain
- langgraph
- langchain-google-genai
- langchain-chroma
- langchain-community
- langchain-text-splitters
- langchain-huggingface
- chromadb
- pandas
- python-dotenv
- sentence-transformers
- openpyxl
- pypdf

---

# Resultados

El asistente permite consultar información relacionada con:

- Productos Mary Kay.
- Beneficios de las líneas de cuidado facial.
- Información de clientes.
- Rutinas de belleza.
- Catálogo de productos.

Además, mantiene el contexto de la conversación gracias a la memoria implementada con LangGraph.

---

# Autor

**María Camila Rueda Cano**

Proyecto Final – IA Generativa

2026