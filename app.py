"""
NovaPay AI Agent — Agente de IA Corporativo
============================================
Agente inteligente que responde preguntas de colaboradores
basándose en documentos internos de NovaPay SpA.

Soporta: PDF, Markdown, CSV, JSON
Stack: LangChain + Google Gemini + FAISS + Gradio
"""

import os
import json
import glob
import pandas as pd
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

import gradio as gr

load_dotenv()

# ---------------------------------------------------------------------------
# 1. CARGA Y PROCESAMIENTO DE DOCUMENTOS
# ---------------------------------------------------------------------------

def load_markdown(filepath: str) -> list[Document]:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": os.path.basename(filepath), "format": "markdown"})]


def load_csv_as_text(filepath: str) -> list[Document]:
    df = pd.read_csv(filepath)
    filename = os.path.basename(filepath)
    documents = []
    summary = f"Archivo: {filename}\nColumnas: {', '.join(df.columns.tolist())}\nTotal de registros: {len(df)}\n\n"
    documents.append(Document(page_content=summary, metadata={"source": filename, "format": "csv", "type": "summary"}))
    for idx, row in df.iterrows():
        row_text = f"Registro del archivo {filename}:\n"
        for col in df.columns:
            row_text += f"- {col}: {row[col]}\n"
        documents.append(Document(page_content=row_text, metadata={"source": filename, "format": "csv", "row": idx}))
    return documents


def load_json_as_text(filepath: str) -> list[Document]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    filename = os.path.basename(filepath)
    documents = []
    def flatten_json(obj, prefix=""):
        texts = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix} > {key}" if prefix else key
                if isinstance(value, (dict, list)):
                    texts.extend(flatten_json(value, new_prefix))
                else:
                    texts.append(f"{new_prefix}: {value}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_prefix = f"{prefix}[{i}]"
                if isinstance(item, (dict, list)):
                    texts.extend(flatten_json(item, new_prefix))
                else:
                    texts.append(f"{new_prefix}: {item}")
        return texts
    if isinstance(data, dict):
        for key, value in data.items():
            section_text = f"Sección '{key}' del archivo {filename}:\n"
            flat = flatten_json(value, key)
            section_text += "\n".join(flat)
            documents.append(Document(page_content=section_text, metadata={"source": filename, "format": "json", "section": key}))
    else:
        full_text = "\n".join(flatten_json(data))
        documents.append(Document(page_content=full_text, metadata={"source": filename, "format": "json"}))
    return documents


def load_pdf(filepath: str) -> list[Document]:
    try:
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return [Document(page_content=text, metadata={"source": os.path.basename(filepath), "format": "pdf"})]
    except Exception as e:
        print(f"Error cargando PDF {filepath}: {e}")
        return []


def load_all_documents(docs_dir: str) -> list[Document]:
    all_docs = []
    loaders = {".md": load_markdown, ".csv": load_csv_as_text, ".json": load_json_as_text, ".pdf": load_pdf}
    for ext, loader_fn in loaders.items():
        for filepath in glob.glob(os.path.join(docs_dir, f"*{ext}")):
            print(f"  📄 Cargando: {os.path.basename(filepath)}")
            docs = loader_fn(filepath)
            all_docs.extend(docs)
    print(f"\n✅ Total de documentos cargados: {len(all_docs)}")
    return all_docs


# ---------------------------------------------------------------------------
# 2. VECTOR STORE (FAISS)
# ---------------------------------------------------------------------------

def create_vector_store(documents: list[Document], api_key: str) -> FAISS:
    print("\n🔧 Creando vector store...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
    )
    splits = text_splitter.split_documents(documents)
    print(f"  📦 Fragmentos generados: {len(splits)}")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", google_api_key=api_key
    )
    vector_store = FAISS.from_documents(splits, embeddings)
    print("✅ Vector store creado exitosamente")
    return vector_store


# ---------------------------------------------------------------------------
# 3. HERRAMIENTAS DEL AGENTE
# ---------------------------------------------------------------------------

_vector_store = None
_docs_dir = None

def setup_tools(vector_store: FAISS, docs_dir: str):
    global _vector_store, _docs_dir
    _vector_store = vector_store
    _docs_dir = docs_dir

@tool
def buscar_documentos(query: str) -> str:
    """Busca información relevante en los documentos internos de NovaPay.
    Usa esta herramienta para responder preguntas sobre políticas, términos,
    servicios, seguridad, productos o cualquier información corporativa.
    Input: la pregunta o tema a buscar.
    """
    if _vector_store is None:
        return "Error: Vector store no inicializado."
    results = _vector_store.similarity_search(query, k=5)
    if not results:
        return "No se encontró información relevante en los documentos."
    context = ""
    sources = set()
    for doc in results:
        context += doc.page_content + "\n\n---\n\n"
        sources.add(doc.metadata.get("source", "desconocido"))
    return f"Información encontrada (fuentes: {', '.join(sources)}):\n\n{context}"

@tool
def consultar_datos_csv(pregunta: str) -> str:
    """Consulta datos estructurados del archivo CSV de tarifas y comisiones de NovaPay.
    Usa esta herramienta cuando la pregunta sea sobre precios, costos, comisiones,
    tarifas o datos numéricos específicos de servicios.
    Input: la pregunta sobre tarifas o datos.
    """
    csv_path = os.path.join(_docs_dir, "tarifas_comisiones.csv")
    if not os.path.exists(csv_path):
        return "No se encontró el archivo de tarifas."
    df = pd.read_csv(csv_path)
    pregunta_lower = pregunta.lower()
    results = []
    for _, row in df.iterrows():
        row_text = " ".join(str(v).lower() for v in row.values)
        keywords = [w for w in pregunta_lower.split() if len(w) > 3]
        if any(kw in row_text for kw in keywords):
            row_info = " | ".join(f"{col}: {row[col]}" for col in df.columns)
            results.append(row_info)
    if not results:
        summary = f"Archivo de tarifas con {len(df)} registros.\n"
        summary += f"Categorías disponibles: {', '.join(df['categoria'].unique())}\n"
        for _, row in df.head(10).iterrows():
            summary += f"- {row['servicio']} ({row['tipo_cuenta']}): "
            if row['comision_porcentaje'] > 0:
                summary += f"{row['comision_porcentaje']}%"
            if row['comision_fija_clp'] > 0:
                summary += f" + ${int(row['comision_fija_clp']):,} CLP"
            if row['comision_porcentaje'] == 0 and row['comision_fija_clp'] == 0:
                summary += "Gratis"
            summary += f" — {row['observaciones']}\n"
        return summary
    return f"Resultados encontrados ({len(results)}):\n\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# 4. AGENTE
# ---------------------------------------------------------------------------

def create_agent(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=api_key,
        temperature=0.3, max_output_tokens=2048,
    )
    tools = [buscar_documentos, consultar_datos_csv]
    system_prompt = """Eres el Asistente Virtual de NovaPay, una fintech chilena. Tu rol es ayudar
a los colaboradores de la empresa respondiendo preguntas basadas en los documentos internos.

INSTRUCCIONES:
- Responde SIEMPRE en español.
- Basa tus respuestas ÚNICAMENTE en la información de los documentos internos.
- Si no encuentras la información, indica que no está disponible en los documentos consultados.
- Sé preciso, profesional y amigable.
- Cuando cites datos numéricos (tarifas, plazos, límites), sé específico.
- Menciona la fuente del documento cuando sea relevante."""

    agent_executor = create_react_agent(model=llm, tools=tools, prompt=system_prompt)
    print("✅ Agente listo")
    return agent_executor


# ---------------------------------------------------------------------------
# 5. INTERFAZ GRADIO
# ---------------------------------------------------------------------------

def create_ui(agent_executor):
    def chat(message, history):
        try:
            response = agent_executor.invoke({"messages": [("user", message)]})
            content = response["messages"][-1].content
            if isinstance(content, list):
                return "".join([block.get("text", "") for block in content if isinstance(block, dict)])
            return content
        except Exception as e:
            return f"⚠️ Error al procesar la consulta: {str(e)}\nPor favor, intenta reformular tu pregunta."

    examples = [
        "¿Cuál es la política de privacidad de NovaPay respecto a datos biométricos?",
        "¿Cuánto cuesta una transferencia internacional a Europa?",
        "¿Qué productos de inversión ofrece NovaPay y cuál es la rentabilidad?",
        "¿Cuáles son los límites de transferencia para una cuenta verificada?",
        "¿Qué medidas de seguridad implementa NovaPay?",
        "¿Cómo funciona el sistema de detección de fraudes?",
        "¿Qué planes ofrece NovaPay Business y cuánto cuestan?",
        "¿Cuántos usuarios tiene NovaPay actualmente?",
        "¿Qué hago si detecto una transacción no reconocida?",
        "¿Cuáles son los derechos de los usuarios sobre sus datos personales?",
    ]

    demo = gr.ChatInterface(
        fn=chat,
        title="🏦 NovaPay — Asistente IA Corporativo",
        description=(
            "Agente de Inteligencia Artificial para consultas sobre documentos internos de NovaPay SpA.\n\n"
            "📄 **Documentos indexados:** Política de Privacidad, Términos y Condiciones, FAQ, "
            "Política de Seguridad, Tarifas y Comisiones, Productos y Servicios.\n\n"
            "💡 Escribe tu pregunta en lenguaje natural."
        ),
        examples=examples,
        theme=gr.themes.Soft(),
    )
    return demo


# ---------------------------------------------------------------------------
# 6. MAIN
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("🏦 NovaPay — Asistente IA Corporativo")
    print("=" * 60)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("\n🔑 Ingresa tu Google API Key: ").strip()
        os.environ["GOOGLE_API_KEY"] = api_key

    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
    if not os.path.exists(docs_dir):
        docs_dir = "documents"

    print(f"\n📂 Directorio de documentos: {docs_dir}")
    print("\n📥 Cargando documentos...")
    documents = load_all_documents(docs_dir)

    if not documents:
        print("❌ No se encontraron documentos. Verifica el directorio.")
        return

    vector_store = create_vector_store(documents, api_key)
    setup_tools(vector_store, docs_dir)

    print("\n🤖 Inicializando agente...")
    agent_executor = create_agent(api_key)

    print("\n🚀 Iniciando interfaz web...")
    demo = create_ui(agent_executor)
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)


if __name__ == "__main__":
    main()
