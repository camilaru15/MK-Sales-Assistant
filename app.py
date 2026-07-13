import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import time
from google.genai.errors import ServerError

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document

from langchain_core.prompts import ChatPromptTemplate

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="MK Sales Assistant",
    page_icon="💄",
    layout="wide"
)

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ==================================================
# ESTILOS
# ==================================================

st.markdown("""
<style>

.main{
background:#FFF8FB;
}

.stButton>button{
background:#D81B60;
color:white;
font-weight:bold;
border-radius:10px;
height:50px;
width:100%;
}

.stButton>button:hover{
background:#AD1457;
color:white;
}

.block{
padding:20px;
border-radius:15px;
background:white;
box-shadow:0px 0px 10px rgba(0,0,0,.1);
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CABECERA
# ==================================================

st.title("💄 MK Sales Assistant")

st.markdown("""
## Bienvenida

Soy tu asistente inteligente especializado en productos Mary Kay.

Puedo ayudarte con:

- 💄 Recomendación de productos
- 🧴 Rutinas de cuidado facial
- 👩 Información de clientes
- 📖 Consulta del catálogo
""")

# ==================================================
# MODELO
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
    max_retries=5,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==================================================
# CARGAR BASE (solo una vez)
# ==================================================

@st.cache_resource
def cargar_base():

    documentos = []

    pdfs = [
        "data/catalogo.pdf",
        "data/experta_producto.pdf"
    ]

    for archivo in pdfs:

        loader = PyPDFLoader(archivo)

        documentos.extend(loader.load())

    clientes = pd.read_excel("data/clientes.xlsx")

    docs_clientes = []

    for _, fila in clientes.iterrows():

        texto = f"""
        
Cliente: {fila['NOMBRE']}

Celular: {fila['CELULAR']}

Ciudad: {fila['CIUDAD']}

Tipo de piel: {fila['TIPO PIEL']}

Tono de base: {fila['TONO BASE']}
"""

        docs_clientes.append(
            Document(page_content=texto)
        )

    documentos.extend(docs_clientes)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documentos)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="db"
    )

vector_db = cargar_base()

retriever = vector_db.as_retriever(
    search_kwargs={"k":4}
)

# ==================================================
# PROMPT
# ==================================================

prompt = ChatPromptTemplate.from_messages([
(
"system",
"""
Eres MK Sales Assistant.

Responde únicamente utilizando el contexto.

Si no encuentras la respuesta responde:

"No encontré información suficiente en la base de conocimiento."

Responde siempre en español.
"""
),
(
"human",
"""
Contexto:

{context}

Pregunta:

{question}
"""
)
])

# ==================================================
# FUNCIÓN
# ==================================================

def responder(pregunta):

    documentos = retriever.invoke(pregunta)

    contexto = "\n\n".join(
        doc.page_content
        for doc in documentos
    )

    historial = "\n".join(
        f"{rol}: {mensaje}"
        for rol, mensaje in st.session_state.history
    )

    mensajes = prompt.invoke({

        "context": contexto + "\n\nHistorial:\n" + historial,

        "question": pregunta

    })

    for intento in range(5):

        try:

            respuesta = llm.invoke(mensajes)
            break

        except ServerError:

            if intento == 4:
                return "⚠️ Gemini está temporalmente saturado. Intenta nuevamente en unos segundos."

            time.sleep(2 ** intento)

    if isinstance(respuesta.content, list):
        texto = ""

        for bloque in respuesta.content:
            if isinstance(bloque, dict) and "text" in bloque:
                texto += bloque["text"]

    else:
        texto = str(respuesta.content)

    return texto

# ==================================================
# CHAT
# ==================================================

if "history" not in st.session_state:
    st.session_state.history=[]

pregunta = st.chat_input(
    "Escribe tu pregunta..."
)

if pregunta:

    st.session_state.history.append(
        ("user",pregunta)
    )

    with st.spinner("Buscando la mejor respuesta para ti..."):

        try:
            respuesta = responder(pregunta)

        except Exception as e:
            st.error(str(e))
            respuesta = "No fue posible generar una respuesta."

    st.session_state.history.append(
        ("assistant",respuesta)
    )

for rol,mensaje in st.session_state.history:

    with st.chat_message(rol):

        st.markdown(mensaje)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/56/Mary_Kay_logo.svg",
        width=180
    )

    st.markdown("## MK Sales Assistant")

    st.success("IA especializada en Mary Kay")

    st.markdown("---")

    st.write("### Tecnologías")

    st.write("Gemini 2.5 Flash")

    st.write("LangChain")

    st.write("ChromaDB")

    st.write("LangGraph")

    st.write("RAG")

    st.write("Streamlit")

    st.markdown("---")

    st.caption("Proyecto Final - IA Generativa")