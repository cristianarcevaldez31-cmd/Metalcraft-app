import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Metalcraft App", page_icon="🛠️", layout="centered")

# Configurar API Key desde Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta la GEMINI_API_KEY en Secrets de Streamlit.")

st.title("🛠️ Metalcraft - Marca de Agua y Fichas Comercial")

# Subir imagen
uploaded_file = st.file_uploader("Sube la foto del equipo o producto:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGBA")
    
    # Cargar logo para marca de agua
    if os.path.exists("logo.png"):
        logo = Image.open("logo.png").convert("RGBA")
        
        # Redimensionar logo al 20% del ancho de la imagen principal
        base_width = int(image.width * 0.20)
        w_percent = (base_width / float(logo.width))
        h_size = int((float(logo.height) * float(w_percent)))
        logo = logo.resize((base_width, h_size), Image.Resampling.LANCZOS)
        
        # Posicionar abajo a la derecha
        position = (image.width - logo.width - 20, image.height - logo.height - 20)
        watermarked = image.copy()
        watermarked.paste(logo, position, logo)
        
        st.subheader("📷 Imagen con marca de agua")
        st.image(watermarked.convert("RGB"), use_column_width=True)
    else:
        st.warning("No se encontró el archivo logo.png en el repositorio.")
        watermarked = image.convert("RGB")
        st.image(watermarked, use_column_width=True)

    # Generación de descripción comercial
    st.subheader("📝 Generar ficha técnica / texto publicitario")
    detalles = st.text_input("Detalles adicionales (medidas, material, calibre, etc.):", "Acero inoxidable, uso industrial")

    if st.button("Generar texto con Gemini"):
        with st.spinner("Redactando ficha publicitaria..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Eres un experto en ventas de equipos gastronómicos e industriales de acero de la marca Metalcraft. Genera una publicación atractiva y profesional para redes sociales/WhatsApp basada en la foto adjunta y estos detalles: {detalles}."
                response = model.generate_content([prompt, image])
                st.success("¡Texto generado!")
                st.text_area("Copia tu texto aquí:", value=response.text, height=250)
            except Exception as e:
                st.error(f"Error al conectar con Gemini: {e}")
                
