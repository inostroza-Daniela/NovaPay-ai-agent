# 🏦 NovaPay — Agente IA Corporativo

Agente de inteligencia artificial corporativo para **NovaPay SpA**, una fintech chilena ficticia. Responde preguntas de los colaboradores de la empresa basándose en documentos internos, procesando múltiples formatos de archivo y cubriendo diferentes dominios organizacionales.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange?logo=google)
![OCI](https://img.shields.io/badge/Deploy-Oracle_Cloud-red?logo=oracle)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Documentos Indexados](#-documentos-indexados)
- [Ejemplos de Preguntas y Respuestas](#-ejemplos-de-preguntas-y-respuestas)
- [Instalación y Ejecución Local](#-instalación-y-ejecución-local)
- [Deploy en Oracle Cloud (OCI)](#-deploy-en-oracle-cloud-oci)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Autor](#-autor)

---

## 📝 Descripción

NovaPay es una empresa ficticia de tecnología financiera que ofrece billetera digital, transferencias, tarjeta de débito, inversiones y soluciones para empresas. Este proyecto construye un **agente de IA conversacional** que permite a cualquier colaborador de la empresa hacer preguntas en lenguaje natural y obtener respuestas precisas extraídas directamente de los documentos internos.

### Características principales:

- **Soporte multi-formato:** Markdown (.md), CSV (.csv), JSON (.json) y PDF (.pdf)
- **Agente ReAct:** Decide automáticamente qué herramienta usar según la pregunta
- **Búsqueda semántica:** Encuentra información relevante incluso con preguntas formuladas de diferentes maneras
- **Consulta de datos estructurados:** Responde preguntas numéricas sobre tarifas y comisiones
- **Interfaz web intuitiva:** Accesible desde cualquier navegador
- **Desplegado en la nube:** Disponible 24/7 en Oracle Cloud Infrastructure

---

## 🏗️ Arquitectura

```
📄 Documentos Internos (MD, CSV, JSON, PDF)
        │
        ▼
🔧 Loaders Multi-formato
   ├── Markdown → texto directo
   ├── CSV → texto descriptivo por fila
   ├── JSON → texto aplanado por sección
   └── PDF → extracción con PyPDF
        │
        ▼
✂️ Text Splitter
   RecursiveCharacterTextSplitter
   (chunks: 1000 chars, overlap: 200)
        │
        ▼
🧮 Embeddings
   Google gemini-embedding-001
        │
        ▼
🗃️ Vector Store (FAISS)
   Índice de similitud semántica
        │
        ▼
🤖 Agente ReAct (LangGraph + Gemini 2.5 Flash)
   ├── 🔍 buscar_documentos
   │   Búsqueda semántica en FAISS
   │   (políticas, FAQ, seguridad, productos)
   │
   └── 📊 consultar_datos_csv
       Consulta directa al CSV de tarifas
       (precios, comisiones, costos)
        │
        ▼
🌐 Interfaz Web (Gradio)
   ChatInterface con ejemplos predefinidos
        │
        ▼
☁️ Oracle Cloud Infrastructure
   VM Compute (Always Free Tier)
```

---

## 🛠️ Tecnologías

| Componente | Tecnología | Descripción |
|---|---|---|
| Lenguaje | Python 3.11 | Lenguaje principal del proyecto |
| Framework de Agentes | LangChain + LangGraph | Orquestación del agente ReAct con herramientas |
| LLM | Google Gemini 2.5 Flash | Modelo de lenguaje para razonamiento y respuestas |
| Embeddings | Google gemini-embedding-001 | Vectorización de documentos para búsqueda semántica |
| Orquestación | LangGraph | Agente ReAct con herramientas |
| Vector Store | FAISS | Índice de vectores para búsqueda por similitud |
| Lectura de documentos | PyPDF, Pandas | Procesamiento de PDF y CSV |
| Interfaz Web | Gradio 4.x | Chat web interactivo |
| Deploy | OCI Compute | Máquina virtual en Oracle Cloud |

---

## 📄 Documentos Indexados

| Documento | Formato | Descripción | Dominio |
|---|---|---|---|
| `politica_privacidad.md` | Markdown | Política de privacidad y protección de datos personales | Legal / Compliance |
| `terminos_condiciones.md` | Markdown | Términos y condiciones de uso de la plataforma | Legal |
| `faq_transacciones.md` | Markdown | Preguntas frecuentes sobre cuenta, pagos, tarjeta, inversiones | Soporte |
| `politica_seguridad.md` | Markdown | Política de seguridad de la información y prevención de fraudes | Ciberseguridad |
| `tarifas_comisiones.csv` | CSV | Tabla completa de tarifas y comisiones por servicio | Financiero |
| `productos_servicios.json` | JSON | Catálogo de productos, métricas y equipo directivo | Estratégico |

---

## 💬 Ejemplos de Preguntas y Respuestas

### Pregunta 1: Datos biométricos
> **Pregunta:** ¿Cuál es la política de NovaPay respecto a los datos biométricos?
>
> **Respuesta:** Según la Política de Privacidad de NovaPay, los datos biométricos (huella dactilar o reconocimiento facial) se recopilan únicamente para verificación de identidad y autenticación en la aplicación móvil. Estos datos se almacenan cifrados con AES-256 y nunca se comparten con terceros. En caso de cierre de cuenta, los datos biométricos se eliminan inmediatamente.

### Pregunta 2: Transferencias internacionales
> **Pregunta:** ¿Cuánto cuesta enviar dinero a Europa?
>
> **Respuesta:** Una transferencia internacional a Estados Unidos y Europa tiene una comisión del 2.0% sobre el monto + $4.990 CLP de cargo fijo (+ IVA). El plazo estimado es de 2-3 días hábiles. El tipo de cambio aplicado es el publicado por NovaPay al momento de la confirmación, que incluye un margen operacional.

### Pregunta 3: Productos de inversión
> **Pregunta:** ¿Qué productos de inversión ofrece NovaPay y cuál tiene mejor rentabilidad?
>
> **Respuesta:** NovaPay Invest ofrece 5 productos: Fondo Conservador (renta fija, 5.2% anual, riesgo bajo), Fondo Balanceado (mixto, 8.7% anual, riesgo moderado), Fondo Crecimiento (renta variable, 14.3% anual, riesgo alto), Depósito a Plazo (4.8% anual, riesgo muy bajo) y Cuenta de Ahorro (3.1% anual, riesgo muy bajo). El de mayor rentabilidad es el Fondo NovaPay Crecimiento con un 14.3% en los últimos 12 meses, aunque con riesgo alto.

### Pregunta 4: Sistema de fraudes
> **Pregunta:** ¿Cómo funciona el sistema de detección de fraudes?
>
> **Respuesta:** NovaPay opera un motor de detección en tiempo real que evalúa más de 200 variables por transacción, incluyendo monto, frecuencia, ubicación geográfica, device fingerprinting y patrones de comportamiento. Las transacciones se clasifican en tres niveles: Bajo (score 0-30, aprobación automática), Medio (31-70, verificación con OTP o biometría) y Alto (71-100, bloqueo automático y revisión manual). Los tipos de fraude monitoreados incluyen phishing, account takeover, identidad sintética, CNP, money muling e ingeniería social.

### Pregunta 5: Límites de cuenta
> **Pregunta:** ¿Cuáles son los límites de transferencia para una cuenta verificada?
>
> **Respuesta:** Una cuenta verificada tiene los siguientes límites: saldo máximo en billetera de $5.000.000 CLP, transferencias diarias de hasta $3.000.000 CLP y transferencias mensuales de hasta $20.000.000 CLP. Además, las transferencias a bancos nacionales en horario bancario son gratuitas para cuentas verificadas.

---

## 🚀 Instalación y Ejecución Local

### Prerrequisitos

- Python 3.11+
- Google API Key ([obtener aquí](https://aistudio.google.com/apikey))

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/inostroza-Daniela/NovaPay-ai-agent.git
cd NovaPay-ai-agent

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
export GOOGLE_API_KEY="tu_google_api_key"

# 4. Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en `http://localhost:7860`

### Alternativa: Google Colab

### Alternativa: Google Colab

1. El proyecto puede ejecutarse en Google Colab subiendo los archivos `app.py` y la carpeta `documents/`, instalando    las dependencias.
2. Configurar la API Key en Secrets (🔑 icono en el panel izquierdo)
3. Ejecutar todas las celdas

---

## ☁️ Deploy en Oracle Cloud (OCI)

### Evidencia del deploy

> 📸 *Captura disponible tras completar el despliegue en OCI.*


### Pasos del deploy

1. **Crear cuenta gratuita** en [Oracle Cloud](https://cloud.oracle.com/free)

2. **Crear instancia Compute** (Always Free Tier):
   - Shape: `VM.Standard.E2.1.Micro`
   - OS: Oracle Linux 8
   - SSH key: agregar tu clave pública

3. **Configurar Security List** (Networking > VCN > Subnet > Security Lists):
   - Agregar Ingress Rule: Source `0.0.0.0/0`, Protocol TCP, Port `7860`

4. **Conectar y desplegar:**
```bash
ssh opc@IP_PUBLICA
# Ejecutar el script automatizado:
bash deploy/setup_oci.sh
```

5. **Acceder a la aplicación:** `http://IP_PUBLICA:7860`

---

## 📁 Estructura del Proyecto

```
NovaPay-ai-agent/
├── README.md                  # Documentación del proyecto
├── requirements.txt           # Dependencias de Python
├── app.py                     # Aplicación principal (Gradio + Agente)
├── documents/                 # Documentos internos de NovaPay
│   ├── politica_privacidad.md    # Política de privacidad (Markdown)
│   ├── terminos_condiciones.md   # Términos y condiciones (Markdown)
│   ├── faq_transacciones.md      # FAQ (Markdown)
│   ├── politica_seguridad.md     # Política de seguridad (Markdown)
│   ├── tarifas_comisiones.csv    # Tarifas y comisiones (CSV)
│   └── productos_servicios.json  # Productos y servicios (JSON)
├── notebooks/
│   └── AluraAgente_NovaPay.ipynb # Notebook para Google Colab
└── deploy/
    └── setup_oci.sh              # Script de deploy para OCI
```

---

## 👩‍💻 Autor

**Daniela Inostroza Mancilla**  
Ingeniería en Ciberseguridad | Data Analyst  
📍 Temuco, Chile

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Daniela_Inostroza-blue?logo=linkedin)](https://www.linkedin.com/in/daniela-i-592462389)
[![GitHub](https://img.shields.io/badge/GitHub-inostroza--Daniela-black?logo=github)](https://github.com/inostroza-Daniela)

---

## 📜 Licencia

MIT License © 2026 Daniela Inostroza Mancilla
