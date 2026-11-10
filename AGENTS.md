# AGENTS.md — Reglas y Pautas del Proyecto para Agentes de Código

Este archivo define las directrices obligatorias, estándares de desarrollo y flujos de trabajo que cualquier Agente de Código (Claude Code, Antigravity, Cursor, GitHub Copilot) debe seguir estrictamente al interactuar con este repositorio.

---

## 1. Filosofía de Desarrollo
1. **Planificar antes de codificar:** Sigue el ciclo **Plan &rarr; Aprobar &rarr; Construir &rarr; Probar**. No apliques cambios en código sin una explicación concisa previa del objetivo.
2. **Minimalismo y Solidez:** Una idea pequeña y terminada vale más que una grande a medias. Prioriza la estabilidad del flujo principal antes que agregar funcionalidades secundarias.
3. **Cero Deuda de Seguridad:** Jamás incrustes credenciales, contraseñas ni claves API en el código.

---

## 2. Convenciones Técnicas y de Código

* **Lenguaje:** Python 3.10 o superior.
* **Framework:** Streamlit (`import streamlit as st`).
* **Llamadas a IA:**
  * Usar la librería oficial de Google (`google-generativeai` o `google-genai`) o llamadas HTTP con `requests`/`httpx`.
  * La clave se obtiene estrictamente de: `os.getenv("GEMINI_API_KEY")`.
  * Si la clave no está presente, mostrar mensaje amigable con `st.warning("GEMINI_API_KEY no detectada...")`.
* **Desacoplamiento de Prompts:**
  * **Prohibido:** Hardcodear strings extensos de prompts dentro de `app.py`.
  * **Obligatorio:** Los prompts del sistema residen en la carpeta `prompts/` (ej. `prompts/system_v1.txt`, `prompts/system_v2.txt`). Se leen con una función utilitaria con codificación UTF-8.

---

## 3. Estructura de Directorios del Proyecto

```text
propuesta-express-ai/
├── .gitignore               # Excluye .env, __pycache__, .venv
├── README.md                # Presentación, negocio y arquitectura
├── PROMPT_MAESTRO.md        # Especificación maestra del proyecto
├── AGENTS.md                # Reglas para agentes de código
├── Dockerfile               # Contenedor para despliegue en la nube
├── requirements.txt         # Dependencias Python mínimas
├── app.py                   # Aplicación principal Streamlit
├── prompts/                 # Versionamiento de prompts de sistema
│   ├── system_v1.txt
│   └── system_v2.txt
├── tests/
│   └── golden_set.json      # Golden set con 5+ casos de prueba
└── docs/
    └── FICHA_DE_NEGOCIO.md  # Ficha de negocio en Markdown / PDF
```

---

## 4. Comandos de Operación Local

```bash
# Activar entorno virtual
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# Ejecutar aplicación localmente
streamlit run app.py

# Construir imagen Docker
docker build -t propuesta-express-ai .

# Ejecutar contenedor Docker
docker run -p 8501:8501 -e GEMINI_API_KEY="AIzaSy..." propuesta-express-ai
```

---

## 5. Criterios de Calidad y Validación
* Cada modificación debe ser verificada ejecutando la aplicación localmente.
* La interfaz debe contener manejo de excepciones para cuotas de API agotadas o fallos de red.
* El Golden Set (`tests/golden_set.json`) debe actualizarse y mantenerse coherente con las versiones de los prompts.
