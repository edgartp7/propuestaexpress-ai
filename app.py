import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe localmente
load_dotenv()

# Configuración de página de Streamlit
st.set_page_config(
    page_title="PropuestaExpress AI — Generador de Propuestas Comerciales",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para una interfaz moderna y ejecutiva
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    .card-info {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-v1 {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .badge-v2 {
        background-color: #dcfce7;
        color: #166534;
    }
</style>
""", unsafe_allow_html=True)


def cargar_prompt_sistema(version: str) -> str:
    """Carga el prompt de sistema desde el archivo correspondiente."""
    archivo = "system_v2.txt" if version == "v2 (Optimizada)" else "system_v1.txt"
    ruta_prompt = os.path.join(os.path.dirname(__file__), "prompts", archivo)
    try:
        with open(ruta_prompt, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error al leer el archivo de prompt {archivo}: {str(e)}")
        return "Eres un asistente que redacta propuestas comerciales profesionales."


def cargar_golden_set():
    """Carga los casos de prueba del Golden Set."""
    ruta_golden = os.path.join(os.path.dirname(__file__), "tests", "golden_set.json")
    try:
        with open(ruta_golden, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def es_modelo_texto_valido(nombre: str) -> bool:
    """
    Filtra y descarta modelos especializados en Audio/TTS, Embeddings o Imágenes,
    asegurando únicamente modelos optimizados para generación de texto comercial.
    """
    n = nombre.lower()
    descartados = ["-tts", "audio", "realtime", "embedding", "imagen", "aqa", "robotics"]
    return not any(d in n for d in descartados)


def descubrir_modelos_y_metodo(api_key: str):
    """
    Determina si la clave funciona mediante Header (x-goog-api-key) o Query Param (?key=),
    y obtiene la lista real de modelos de TEXTO disponibles para esa clave en Google AI Studio.
    """
    key_clean = api_key.strip()
    
    # 1. Probar método Header (Recomendado por Google, sin ?key= en la URL)
    for ver in ["v1beta", "v1"]:
        try:
            url = f"https://generativelanguage.googleapis.com/{ver}/models"
            headers = {"x-goog-api-key": key_clean}
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                modelos = [
                    m.get("name", "").replace("models/", "") 
                    for m in r.json().get("models", []) 
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                    and es_modelo_texto_valido(m.get("name", ""))
                ]
                if modelos:
                    return ver, "header", modelos
        except Exception:
            pass

    # 2. Probar método Query Param (solo en la URL, sin header x-goog-api-key)
    for ver in ["v1beta", "v1"]:
        try:
            url = f"https://generativelanguage.googleapis.com/{ver}/models?key={key_clean}"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                modelos = [
                    m.get("name", "").replace("models/", "") 
                    for m in r.json().get("models", []) 
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                    and es_modelo_texto_valido(m.get("name", ""))
                ]
                if modelos:
                    return ver, "query", modelos
        except Exception:
            pass

    return "v1beta", "header", []


def llamar_gemini(api_key: str, prompt_sistema: str, prompt_usuario: str) -> tuple[str, str]:
    """
    Llama a la API de Google Gemini utilizando el método de autenticación y modelo
    confirmados por la cuenta de Google AI Studio, descartando modelos de audio/TTS.
    """
    key_clean = api_key.strip()
    
    # Descubrir modelos de texto y método de autenticación válido
    api_ver, metodo_auth, modelos_disponibles = descubrir_modelos_y_metodo(key_clean)
    
    # Priorizar modelos de texto Flash y Pro
    candidatos = []
    if modelos_disponibles:
        preferencias = [
            "gemini-2.0-flash",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-001",
            "gemini-2.5-pro",
            "gemini-1.5-pro"
        ]
        for pref in preferencias:
            for m in modelos_disponibles:
                if pref == m and m not in candidatos:
                    candidatos.append(m)
        for pref in ["2.0-flash", "2.5-flash", "1.5-flash", "flash", "pro"]:
            for m in modelos_disponibles:
                if pref in m.lower() and m not in candidatos:
                    candidatos.append(m)
        for m in modelos_disponibles:
            if m not in candidatos:
                candidatos.append(m)
    else:
        # Fallbacks estándar de texto si ListModels no retornó
        candidatos = [
            "gemini-2.0-flash",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro"
        ]
        
    ultimo_error = ""
    
    for modelo in candidatos:
        # Construir URL y Headers según el método de autenticación detectado (NUNCA mezclar ambos)
        if metodo_auth == "header":
            url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{modelo}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": key_clean
            }
        else:
            url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{modelo}:generateContent?key={key_clean}"
            headers = {
                "Content-Type": "application/json"
            }
            
        payload = {
            "system_instruction": {
                "parts": [{"text": prompt_sistema}]
            },
            "contents": [
                {
                    "parts": [{"text": prompt_usuario}]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 2048,
                "topP": 0.95
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            # Si el modelo no soporta system_instruction (error 400), probamos combinando prompts
            if response.status_code == 400 and "system_instruction" in response.text.lower():
                payload_fallback = {
                    "contents": [
                        {
                            "parts": [{"text": f"INSTRUCCIONES DEL SISTEMA:\n{prompt_sistema}\n\n---\n\nSOLICITUD:\n{prompt_usuario}"}]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.4,
                        "maxOutputTokens": 2048,
                        "topP": 0.95
                    }
                }
                response = requests.post(url, headers=headers, json=payload_fallback, timeout=45)
                
            if response.status_code == 200:
                data = response.json()
                texto_generado = data["candidates"][0]["content"]["parts"][0]["text"]
                return texto_generado, modelo
            elif response.status_code == 404:
                ultimo_error = f"Modelo {modelo} no encontrado (404)"
                continue
            else:
                try:
                    err_json = response.json()
                    mensaje = err_json.get("error", {}).get("message", response.text)
                except Exception:
                    mensaje = response.text
                ultimo_error = f"Google API en {modelo} (Código {response.status_code}): {mensaje}"
                # Solo interrumpir en 403 (clave prohibida). En 400 (modalidad) o 429 (cuota de un modelo), continuar al siguiente
                if response.status_code == 403:
                    break
                continue
        except requests.exceptions.RequestException as e:
            ultimo_error = f"Error de conexión en {modelo}: {str(e)}"
            continue
            
    raise Exception(ultimo_error or "No se pudo conectar con ningún modelo de texto de Gemini disponible.")


# --- BARRA LATERAL (CONFIGURACIÓN Y SECRETOS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    st.title("PropuestaExpress AI")
    st.markdown("**Versión 1.0 — Proyecto Final UAI**")
    
    st.markdown("---")
    st.subheader("⚙️ Configuración del Modelo")
    
    # Detección segura de API Key por variable de entorno o ingreso manual
    env_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    api_key_input = st.text_input(
        "Ingresa tu Gemini API Key:",
        value=env_key,
        type="password",
        placeholder="AQ.Ab8... o AIzaSy...",
        help="Consíguela gratis sin tarjeta en https://aistudio.google.com/"
    )
    
    api_key = api_key_input.strip() if api_key_input else env_key
    
    if api_key:
        if env_key and api_key == env_key:
            st.success("✅ `GEMINI_API_KEY` detectada desde entorno.")
        else:
            st.success("✅ API Key lista para usar.")
    else:
        st.info("ℹ️ Pega tu API Key de Google AI Studio arriba para procesar.")
        
    if api_key:
        with st.expander("🔍 Modelos Detectados en tu Cuenta"):
            v_det, met_det, mods_det = descubrir_modelos_y_metodo(api_key)
            if mods_det:
                st.success(f"Conexión exitosa vía {met_det.upper()}. {len(mods_det)} modelos disponibles:")
                st.write(mods_det[:5])
            else:
                st.info("Intentando conexión directa con endpoints activos...")
    
    st.markdown("---")
    st.subheader("🧪 Ingeniería de Prompts")
    version_prompt = st.radio(
        "Versión del System Prompt:",
        options=["v2 (Optimizada)", "v1 (Baseline)"],
        index=0,
        help="Permite comparar en vivo la diferencia de calidad y formato entre la versión inicial y la optimizada con técnicas de Few-Shot y Guardrails."
    )
    
    if version_prompt == "v2 (Optimizada)":
        st.caption("🟢 **v2:** Incluye Chain-of-Thought, tabla presupuestaria estricta, delimitadores y cláusulas de exclusión contractual.")
    else:
        st.caption("🔴 **v1:** Instrucción genérica básica sin restricciones duras de formato.")

    st.markdown("---")
    st.subheader("📁 Casos de Prueba (Golden Set)")
    golden_cases = cargar_golden_set()
    nombres_casos = ["(Seleccionar manualmente)"] + [c["titulo"] for c in golden_cases]
    caso_seleccionado = st.selectbox("Cargar caso de prueba precargado:", options=nombres_casos)


# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="main-title">💼 PropuestaExpress AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Convierte notas desordenadas de reuniones en propuestas comerciales ejecutivas y cotizaciones formales completas en segundos.</div>', unsafe_allow_html=True)

# Autocompletado si se selecciona un caso del Golden Set
default_cliente = ""
default_servicio = "Desarrollo Web & eCommerce"
default_tono = "Persuasivo / Comercial"
default_moneda = "CLP"
default_notas = ""

if caso_seleccionado != "(Seleccionar manualmente)":
    caso_data = next((c for c in golden_cases if c["titulo"] == caso_seleccionado), None)
    if caso_data:
        default_cliente = caso_data["input"]["cliente"]
        default_servicio = caso_data["input"]["servicio"]
        default_tono = caso_data["input"]["tono"]
        default_moneda = caso_data["input"]["moneda"]
        default_notas = caso_data["input"]["notas_reunion"]
        st.info(f"💡 Caso cargado del Golden Set: **{caso_data['id']}**")

# Formulario de Entrada
col1, col2 = st.columns([1, 1])

with col1:
    cliente = st.text_input("🏢 Nombre del Cliente o Empresa Prospecto:", value=default_cliente, placeholder="Ej: Importadora Los Andes SpA")
    servicios_lista = [
        "Desarrollo Web & eCommerce",
        "Consultoría Estratégica & Automatización",
        "Marketing Digital & Generación de Leads B2B",
        "Infraestructura Cloud & DevOps",
        "Diseño de Marca & Packaging",
        "Servicios Profesionales Generales"
    ]
    idx_serv = servicios_lista.index(default_servicio) if default_servicio in servicios_lista else 0
    servicio = st.selectbox("🛠️ Tipo de Servicio Principal:", options=servicios_lista, index=idx_serv)

with col2:
    tonos_lista = ["Persuasivo / Comercial", "Ejecutivo / Formal", "Cercano / Colaborativo"]
    idx_tono = tonos_lista.index(default_tono) if default_tono in tonos_lista else 0
    tono = st.selectbox("🎯 Tono de la Comunicación:", options=tonos_lista, index=idx_tono)

    monedas_lista = ["CLP", "USD", "EUR", "MXN"]
    idx_mon = monedas_lista.index(default_moneda) if default_moneda in monedas_lista else 0
    moneda = st.selectbox("💰 Moneda del Presupuesto:", options=monedas_lista, index=idx_mon)

notas_reunion = st.text_area(
    "📝 Notas crudas de la reunión / Requerimientos conversados:",
    value=default_notas,
    height=160,
    placeholder="Pega aquí los apuntes de la reunión, dolores del cliente, presupuesto conversado, fechas límite y acuerdos preliminares..."
)

# Botón de Acción Principal
boton_generar = st.button("🚀 Generar Propuesta Comercial con IA")

if boton_generar:
    if not api_key:
        st.error("❌ Se requiere una API Key de Google Gemini para procesar la propuesta. Ingrésala en la barra lateral o configúrala en el entorno como `GEMINI_API_KEY`.")
    elif not cliente.strip() or not notas_reunion.strip():
        st.warning("⚠️ Por favor ingresa al menos el nombre del cliente y las notas de la reunión.")
    else:
        prompt_sistema = cargar_prompt_sistema(version_prompt)
        
        prompt_usuario = f"""
### DATOS DEL CLIENTE:
{cliente}

### TIPO DE SERVICIO:
{servicio}

### TONO COMERCIAL:
{tono}

### MONEDA REFERENCIAL:
{moneda}

### NOTAS CRUDAS DE LA REUNIÓN:
{notas_reunion}
"""
        with st.spinner("🤖 Analizando notas, estructurando alcance y generando cotización con Gemini..."):
            try:
                propuesta_generada, modelo_usado = llamar_gemini(api_key, prompt_sistema, prompt_usuario)
                st.session_state["ultima_propuesta"] = propuesta_generada
                st.session_state["ultimo_cliente"] = cliente
                st.session_state["modelo_usado"] = modelo_usado
                st.success(f"✨ ¡Propuesta generada exitosamente con Gemini ({modelo_usado})!")
            except Exception as e:
                st.error(f"Ocurrió un error al generar la propuesta: {str(e)}")

# Visualización de Resultados
if "ultima_propuesta" in st.session_state and st.session_state["ultima_propuesta"]:
    st.markdown("---")
    st.subheader(f"📄 Propuesta Comercial para {st.session_state.get('ultimo_cliente', 'el Cliente')}")
    
    tab1, tab2 = st.tabs(["👁️ Vista Documental Formateada", "📋 Código Markdown & Exportación"])
    
    with tab1:
        st.markdown(st.session_state["ultima_propuesta"])
    
    with tab2:
        st.text_area("Contenido en Markdown crudo:", value=st.session_state["ultima_propuesta"], height=300)
        col_down1, col_down2 = st.columns([1, 3])
        with col_down1:
            st.download_button(
                label="📥 Descargar Propuesta (.md)",
                data=st.session_state["ultima_propuesta"],
                file_name=f"Propuesta_Comercial_{cliente.replace(' ', '_')}.md",
                mime="text/markdown"
            )

# Pie de página
st.markdown("---")
st.caption("PropuestaExpress AI · Desarrollado para el Proyecto Final del Certificado en Prompt Engineering · UAI 2026")
