import streamlit as st
from google import genai
from PIL import Image
import os

st.set_page_config(page_title="Metalcraft App", page_icon="🛠️", layout="centered")

# Configurar API Key desde Secrets con el cliente de google-genai
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
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
        
        # Redimensionar logo al 20% del ancho
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
        watermarked = image.copy()
        st.image(watermarked.convert("RGB"), use_column_width=True)

    # Generación de descripción comercial
    st.subheader("📝 Generar ficha técnica / texto publicitario")
    detalles = st.text_input("Detalles adicionales (medidas, material, calibre, etc.):", "Estufa 2 freidoras y plancha")

    if st.button("Generar texto con Gemini"):
        with st.spinner("Redactando ficha publicitaria..."):
            image_rgb = watermarked.convert("RGB")
            prompt = f"Eres un experto en ventas de equipos gastronómicos e industriales de acero de la marca Metalcraft. Genera una publicación atractiva y profesional para redes sociales/WhatsApp basada en la foto adjunta y estos detalles: {detalles}."
            
            # Intenta primero con gemini-3.8-flash y si está saturado cambia a gemini-2.5-flash
            modelos = ['gemini-3.8-flash', 'gemini-2.5-flash']
            
            respuesta_exitosa = False
            for model_id in modelos:
                try:
                    response = client.models.generate_content(
                        model=model_id,
                        contents=[prompt, image_rgb]
                    )
                    st.success("¡Texto generado con éxito!")
                    st.text_area("Copia tu texto aquí:", value=response.text, height=250)
                    respuesta_exitosa = True
                    break
                except Exception as e:
                    continue
            
            if not respuesta_exitosa:
                st.error("Los servidores de Google están experimentando alta demanda. Presiona el botón de nuevo en un momento.")
                
