# PropuestaExpress AI — Generador de Propuestas Comerciales con IA

> De notas desordenadas de reunión a propuestas comerciales ejecutivas y cotizaciones formales en segundos.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Enlaces Rápidos del Proyecto
* 🌐 **URL Pública Desplegada:** `[Configurar URL de Render / Cloud Run tras despliegue]`
* 🎥 **Video Demo (Máximo 3 minutos):** `[Configurar enlace a YouTube / Loom]`
* 📄 **Ficha de Negocio Oficial (1 Página en PDF):** [docs/FICHA_DE_NEGOCIO_PROPUESTAEXPRESS.pdf](docs/FICHA_DE_NEGOCIO_PROPUESTAEXPRESS.pdf)
* 📋 **Prompt Maestro:** [PROMPT_MAESTRO.md](PROMPT_MAESTRO.md)
* 🤖 **Reglas para Agentes de Código:** [AGENTS.md](AGENTS.md)

---

## 1. Idea de Negocio y Propuesta de Valor

### 1.1. El Problema
Los profesionales independientes (freelancers), consultores y pequeñas agencias de servicios B2B pierden entre **4 y 6 horas redactando propuestas comerciales formales** tras cada reunión de prospección con un cliente. Las notas tomadas durante las reuniones suelen ser desordenadas, con requerimientos dispersos, plazos difusos y acuerdos preliminares verbales. 

La demora en enviar la cotización (a menudo de 3 a 5 días) enfría el interés del cliente, reduce la tasa de cierre y quita tiempo productivo que debería dedicarse a la ejecución de proyectos remunerados.

### 1.2. El Cliente
* Consultores y agencias de marketing, desarrollo de software, diseño y servicios profesionales B2B.
* Freelancers y profesionales independientes que necesitan profesionalizar su proceso de ventas sin contratar personal administrativo.

### 1.3. La Solución
**PropuestaExpress AI** es una plataforma web desarrollada en Python con Streamlit que transforma notas crudas de reuniones en propuestas comerciales estructuradas de alto impacto. 

El usuario simplemente ingresa el nombre del cliente, el tipo de servicio, el tono comercial (Formal, Persuasivo o Cercano), la moneda y pega sus notas crudas. La IA procesa la información y genera de inmediato:
1. **Diagnóstico y Objetivos de Negocio:** Síntesis del problema real del cliente.
2. **Alcance de la Solución (Scope of Work):** Detalle técnico de lo que se incluye y lo que queda **explícitamente excluido**.
3. **Cronograma y Fases de Entrega:** Hitos con plazos de tiempo lógicos y secuenciales.
4. **Desglose Presupuestario Sugerido:** Tabla de inversión por fase o entregable con moneda personalizada y total exacto.
5. **Próximos Pasos y Condiciones:** Términos de pago y llamados a la acción para la firma.

### 1.4. El Rol Central de la IA Generativa
La IA no opera como un formulario de plantillas estáticas:
* Realiza **razonamiento semántico** para interpretar requerimientos implícitos a partir de apuntes desordenados.
* Estructura los entregables con lenguaje persuasivo y técnico acorde al tono seleccionado.
* Diseña una secuencia lógica de hitos y previene el *scope creep* (extensión desmedida de alcance sin cobrar).
* Calcula una distribución presupuestaria matemáticamente consistente.

### 1.5. Modelo de Ingresos y Viabilidad Financiera
* **Freemium (Starter):** 3 propuestas al mes gratis (canal de adquisición).
* **Plan Pro ($15 USD/mes):** Propuestas ilimitadas, exportación en Markdown/PDF y personalización de marca.
* **Plan Agency ($39 USD/mes):** Hasta 5 usuarios por equipo y plantillas corporativas avanzadas.

#### Costo Mensual Estimado de Operar la App (Escenario: 1.000 usuarios activos / 10.000 propuestas al mes)
* **Consumo de API de IA (Google Gemini 1.5/2.0 Flash):**  
  $10.000 \text{ solicitudes} \times (1.000 \text{ tokens in} + 1.500 \text{ tokens out}) = 25 \text{M tokens/mes}$.  
  Costo Gemini Flash ($0,075 / 1M in, $0,30 / 1M out): **$1,13 USD / mes** *(En Free Tier: $0,00 USD)*.
* **Hosting en la Nube (Contenedor Cloud Run / Render con auto-scaling):** **$7,00 USD / mes**.
* **Base de datos y almacenamiento serverless:** **$0,00 USD / mes**.
* **Costo Operativo Total:** **~$8,13 USD / mes**.
* **Margen Bruto:** Con solo 1 usuario de pago ($15 USD/mes) se cubren el 100% de los costos operativos (**Margen > 85%**).

---

## 2. Arquitectura del Sistema

```
                      ┌────────────────────────────────────────┐
                      │          Usuario / Cliente Web         │
                      └──────────────────┬─────────────────────┘
                                         │ (HTTPS)
                                         ▼
                      ┌────────────────────────────────────────┐
                      │    Streamlit Web App (Frontend/UI)     │
                      │               [app.py]                 │
                      └──────────┬───────────────────▲─────────┘
                                 │                   │
                     Carga Prompt│                   │Renderiza Markdown
                                 ▼                   │
                      ┌──────────────────────┐       │
                      │  prompts/system_*.txt│       │
                      └──────────┬───────────┘       │
                                 │                   │
                                 ▼                   │
                      ┌──────────────────────────────┴─────────┐
                      │           Gemini API Client            │
                      │ (Autodescubrimiento dinámico de texto) │
                      └──────────────────┬─────────────────────┘
                                         │ Inyectada vía ENV
                      ┌──────────────────┴─────────────────────┐
                      │     Variables de Entorno / Secrets     │
                      │         (GEMINI_API_KEY)               │
                      └────────────────────────────────────────┘
```

---

## 3. Instrucciones de Uso y Ejecución Local

### 3.1. Requisitos Previos
* Python 3.10 o superior instalado.
* API Key gratuita de Gemini (obtenida en [Google AI Studio](https://aistudio.google.com/)).

### 3.2. Instalación Local
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/propuestaexpress-ai.git
cd propuestaexpress-ai

# 2. Crear y activar entorno virtual
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variable de entorno (opcional si la ingresas en la app)
# En Windows (PowerShell):
$env:GEMINI_API_KEY="tu-api-key-aqui"
# En Linux/Mac:
export GEMINI_API_KEY="tu-api-key-aqui"

# 5. Ejecutar la aplicación
streamlit run app.py
```

### 3.3. Ejecución con Docker
```bash
# Construir la imagen Docker
docker build -t propuestaexpress-ai .

# Correr el contenedor pasando la clave como variable de entorno
docker run -p 8501:8501 -e GEMINI_API_KEY="tu-api-key-aqui" propuestaexpress-ai
```

---

## 4. Ingeniería de Prompts y Evidencia de Mejora (Golden Set)

La aplicación desacopla estrictamente la lógica de la interfaz de las directrices del modelo de lenguaje. Los prompts residen en la carpeta `/prompts`:
* **`system_v1.txt` (Baseline):** Instrucción genérica básica sin restricciones duras de estructura ni guardrails.
* **`system_v2.txt` (Optimizada):** Prompt de alta precisión con delimitadores de entrada, proceso de análisis interno (Chain-of-Thought guiado), restricciones explícitas de formato Markdown, cláusulas obligatorias de exclusión de alcance y tabla presupuestaria matemáticamente estricta.

### Tabla Comparativa del Golden Set (5 Casos de Prueba)

A continuación se documenta la evaluación empírica de los 5 casos diseñados en `tests/golden_set.json`:

| ID Caso | Cliente y Escenario | Resultado con Prompt v1 (Baseline) | Resultado con Prompt v2 (Optimizado) | Mejora Medida y Evidenciada |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Calzados Austral SpA**<br>*(eCommerce & Webpay)* | Propuesta genérica. Asumió que el proveedor tomaba las fotos de los productos. Sin tabla de precios. | Detalló 5 inclusiones y 3 exclusiones críticas (fotografía, licencias). Tabla presupuestaria en CLP ($2.500.000) en 3 fases. | **Cumplimiento de criterios: 25% &rarr; 100%.** Blindaje contra sobrecostos fotográficos. |
| **02** | **Clínica DentalPlus**<br>*(Automatización No-Show)* | Trató el proyecto como un chatbot genérico sin cuantificar la tasa de inasistencia del 32%. | Resaltó el dolor del ausentismo clínico (32%). Excluyó los costos de Meta API y presupuestó $2,000 USD en 3 hitos. | **Precisión de alcance: 0% &rarr; 100%.** Enfoque directo a ROI clínico. |
| **03** | **ShieldTech Security**<br>*(Marketing B2B Leads)* | Ofreció estrategias para Instagram/TikTok (no aptas para B2B). Confundió leads con ventas finales. | Diseñó campaña Outbound en LinkedIn/Email para CISOs. Aclaró que el cliente cierra la venta. Presupuesto $9,000 USD trimestral. | **Alineación B2B: 30% &rarr; 100%.** Eliminación de garantías falsas de venta. |
| **04** | **MicroPresta Fintech**<br>*(Migración Cloud Docker)* | Redactó un texto vago sin mencionar Docker ni la concurrencia crítica de fin de mes. | Detalló Dockerización, migración sin downtime y excluyó de los honorarios las facturas de nube de AWS/GCP. | **Rigor técnico: 35% &rarr; 100%.** Delimitación transparente de costos de nube. |
| **05** | **VerdePuro Alimentos**<br>*(Packaging & Marca)* | No especificó si el presupuesto cubría la impresión física de las bolsas plásticas. | Entregables claros (Logo, 3 artes Doypack, Landing) y excluyó explícitamente costos de tiraje de imprenta. Plazo exacto de 4 semanas. | **Prevención de disputas: 0% &rarr; 100%.** Cumplimiento total del plazo de 4 semanas. |

### Resumen Cuantitativo de Mejoras
* **Consistencia de Estructura Documental:** 40% en v1 $\rightarrow$ **100% en v2**.
* **Presencia de Tabla Presupuestaria con Coherencia Matemática:** 0/5 en v1 $\rightarrow$ **5/5 en v2**.
* **Inclusión de Cláusulas de Exclusión (Scope Guardrails):** 0/5 en v1 $\rightarrow$ **5/5 en v2**.

---

## 5. Buenas Prácticas y Seguridad de Secretos
* **Cero claves en código:** Todas las credenciales se consumen a través de `os.getenv("GEMINI_API_KEY")` o ingreso en tiempo de ejecución.
* **Control de Costos:** Configurado en Google AI Studio con cuota Free Tier (límite de gasto nativo en **$0,00 USD**).
* **Verificación de Requisitos Mínimos:** Probado en navegador privado en modo incógnito, sin dependencias de sesiones locales.
