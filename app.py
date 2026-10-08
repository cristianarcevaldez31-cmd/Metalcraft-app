import streamlit as st
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Metalcraft - Creador de Publicaciones",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 Metalcraft - Generador de Publicaciones")
st.write("Sube la foto del equipo, ingresa sus características y descarga el material listo para publicar.")

# --- CONFIGURACIÓN GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ Recuerda agregar tu GEMINI_API_KEY en las opciones de Secrets en Streamlit Cloud.")

# --- CARGAR MARCA DE AGUA LOCAL (logo.png) ---
@st.cache_data
def obtener_marca_agua():
    try:
        # Carga directa del logo subido al repositorio
        return Image.open("logo.png").convert("RGBA")
    except Exception as e:
        return None

# --- FUNCIÓN PARA ESTAMPAR MARCA DE AGUA ---
def estampar_marca_agua(base_img, logo_img, escala_pct=22, opacidad_pct=85):
    base_rgba = base_img.convert("RGBA")
    
    # Redimensionar logo proporcionalmente
    ancho_base, alto_base = base_rgba.size
    ancho_logo = int(ancho_base * (escala_pct / 100))
    ratio = ancho_logo / float(logo_img.size[0])
    alto_logo = int(float(logo_img.size[1]) * ratio)
    logo_resized = logo_img.resize((ancho_logo, alto_logo), Image.Resampling.LANCZOS)
    
    # Ajustar opacidad del logo
    if logo_resized.mode == 'RGBA':
        r, g, b, alpha = logo_resized.split()
        alpha = alpha.point(lambda p: int(p * (opacidad_pct / 100)))
        logo_resized = Image.merge('RGBA', (r, g, b, alpha))

    # Ubicación: Esquina inferior derecha con margen del 3%
    margen_x = int(ancho_base * 0.03)
    margen_y = int(alto_base * 0.03)
    pos_x = ancho_base - ancho_logo - margen_x
    pos_y = alto_base - alto_logo - margen_y

    # Estampar capa transparente
    capa_final = Image.new('RGBA', base_rgba.size, (0, 0, 0, 0))
    capa_final.paste(base_rgba, (0, 0))
    capa_final.paste(logo_resized, (pos_x, pos_y), mask=logo_resized)
    
    return capa_final.convert("RGB")

# --- INTERFAZ DE USUARIO ---
st.subheader("1. Datos del Equipo y Fotografía")

foto_subida = st.file_uploader("Selecciona la foto del equipo (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])

col1, col2 = st.columns(2)
with col1:
    tipo_producto = st.selectbox(
        "Tipo de equipo:",
        [
            "Estufa Industrial",
            "Plancha / Comal",
            "Asador de Pollos",
            "Barra Fría / Mesa de Trabajo",
            "Carrito / Taco Cart",
            "Prensa para Tortillas",
            "Tejaban / Estructura",
            "Otro"
        ]
    )
    material_calibre = st.text_input("Material / Calibre:", placeholder="Ej. Acero Inoxidable, PTR 1.5\", Cal. 18")

with col2:
    medidas = st.text_input("Medidas (Largo x Ancho x Alto):", placeholder="Ej. 120cm x 60cm x 90cm")
    quemadores_detalles = st.text_input("Quemadores / Accesorios:", placeholder="Ej. 4 quemadores H, válvulas alta presión")

detalles_extra = st.text_area("Detalles adicionales o promociones:", placeholder="Ej. Envío disponible, garantía, incluye manguera...")

# --- PROCESAMIENTO ---
if foto_subida and st.button("🚀 Generar Publicación"):
    with st.spinner("Procesando marca de agua y redactando la descripción comercial..."):
        # 1. Abrir imagen
        img_original = Image.open(foto_subida)
        
        # 2. Estampar Logo
        logo = obtener_marca_agua()
        if logo:
            img_procesada = estampar_marca_agua(img_original, logo)
        else:
            img_procesada = img_original
            st.warning("⚠️ No se encontró el archivo 'logo.png' en el repositorio. La imagen se generó sin marca de agua.")

        # 3. Solicitud a Gemini API
        prompt_redaccion =
      
