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
   ├── buscar_documentos
   │   Búsqueda semántica en FAISS
   │   (políticas, FAQ, seguridad, productos)
   │
   └── consultar_datos_csv
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

## 💬 Ejemplos de Preguntas y Respuestas

### Pregunta 1: Datos biométricos
> **Pregunta:** ¿Cuál es la política de privacidad de NovaPay respecto a datos biométricos?
>
> **Respuesta:** NovaPay recopila datos biométricos, como huella dactilar o reconocimiento facial, únicamente para la verificación de identidad y autenticación en la aplicación móvil. Estos datos se almacenan cifrados y no se comparten con terceros. Además, los datos biométricos son eliminados inmediatamente tras el cierre de la cuenta del usuario.
>
> Fuente: Política de Privacidad y Protección de Datos — NovaPay SpA (Versión 3.2).

![Ejemplo biométricos](Captura%20de%20pantalla%202026-06-28%20a%20la(s)%2012.22.31.png)

### Pregunta 2: Sistema de detección de fraudes
> **Pregunta:** ¿Cómo funciona el sistema de detección de fraudes?
>
> **Respuesta:** El sistema de detección de fraudes de NovaPay funciona con un motor en tiempo real que evalúa más de 200 variables por transacción, incluyendo monto y frecuencia, ubicación geográfica, patrones de comportamiento (behavioral analytics), device fingerprinting y velocidad de operaciones sucesivas.
>
> El sistema clasifica el riesgo: Bajo (score 0-30) con aprobación automática, Medio (31-70) con verificación adicional (OTP o biometría), y Alto (71-100) con bloqueo automático y revisión manual.

![Ejemplo fraudes](Captura%20de%20pantalla%202026-06-28%20a%20la(s)%2012.22.48.png)

### Pregunta 3: Productos de inversión
> **Pregunta:** ¿Qué productos de inversión ofrece NovaPay y cuál es la rentabilidad?
>
> **Respuesta:** NovaPay Invest ofrece: Fondo NovaPay Conservador (Renta Fija, 5.2%), Fondo NovaPay Balanceado (Mixto, 8.7%), Fondo NovaPay Crecimiento (Renta Variable, 14.3%), Depósito a Plazo NovaPay (tasa anual 4.8%) y Cuenta Ahorro NovaPay (tasa anual 3.1%). Próximamente se añadirán ETFs internacionales en Q3 2026.

![Ejemplo inversiones](Captura%20de%20pantalla%202026-06-28%20a%20la(s)%2012.23.18.png)

---

## Instalación y Ejecución Local

### Prerrequisitos

- Python 3.11+
- Google API Key

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
2. Configurar la API Key en Secrets (icono en el panel izquierdo)
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
