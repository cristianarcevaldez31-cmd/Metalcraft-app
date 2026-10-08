import streamlit as st
from google import genai
from PIL import Image
import os
import io

st.set_page_config(page_title="Metalcraft App", page_icon="🛠️", layout="centered")

# Configurar cliente de Gemini IA desde Secrets
client = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error("Error al inicializar cliente de Gemini.")

st.title("🛠️ Metalcraft - Marca de Agua y Asistente IA")

# ==========================================
# SECCIÓN 1: ASISTENTE DE REDACCIÓN CON IA
# ==========================================
st.header("🤖 Asistente IA para Redacción")
st.write("Escribe brevemente qué equipo es y Gemini redactará la publicación por ti.")

equipo_input = st.text_input("¿Qué equipo quieres publicar?:", "Estufa 2 freidoras y plancha")

if st.button("✨ Generar con Gemini IA"):
    if client is None:
        st.error("No se encontró la GEMINI_API_KEY configurada en Secrets.")
    else:
        with st.spinner("La IA está redactando tus títulos y descripción..."):
            prompt = f"""Eres el experto en ventas y marketing de la empresa Metalcraft, especializada en fabricación de equipo industrial gastronómico y herrería.
Crea una publicación altamente atractiva para Facebook/WhatsApp para vender el siguiente equipo: '{equipo_input}'.

Estructura la respuesta así:
1. 💥 3 Propuestas de Títulos llamativos.
2. 📝 Descripción comercial vendedora con emojis, resaltando la calidad del acero, durabilidad industrial y llamado a cotizar por WhatsApp.
3. 🏷️ Hashtags recomendados.
"""
            # Bucle de respaldo para evitar fallos de servidor
            modelos = ['gemini-3.8-flash', 'gemini-2.5-flash']
            exito = False
            
            for model_id in modelos:
                try:
                    response = client.models.generate_content(
                        model=model_id,
                        contents=prompt
                    )
                    st.success("¡Propuestas generadas con éxito!")
                    st.text_area("Copia el texto que más te guste:", value=response.text, height=300)
                    exito = True
                    break
                except Exception:
                    continue
            
            if not exito:
                st.error("El servidor de la IA está saturado en este momento. Intenta presionar el botón de nuevo.")

st.divider()

# ==========================================
# SECCIÓN 2: MARCA DE AGUA MÚLTIPLE
# ==========================================
st.header("📷 Marca de Agua Múltiple")

posicion_opcion = st.selectbox(
    "Posición de la marca de agua:",
    ["Abajo Derecha", "Abajo Centro", "Abajo Izquierda", "Arriba Derecha", "Centro", "Arriba Izquierda"]
)

uploaded_files = st.file_uploader(
    "Selecciona fotos de tu galería:", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo_base = Image.open(logo_path).convert("RGBA")
        
        st.subheader(f"🖼️ Fotos procesadas ({len(uploaded_files)}):")
        
        for idx, file in enumerate(uploaded_files):
            img = Image.open(file).convert("RGBA")
            
            # Ajustar logo al 20% del ancho
            base_width = int(img.width * 0.20)
            w_percent = (base_width / float(logo_base.width))
            h_size = int((float(logo_base.height) * float(w_percent)))
            logo = logo_base.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            # Coordenadas según elección
            if posicion_opcion == "Abajo Derecha":
                pos = (img.width - logo.width - 20, img.height - logo.height - 20)
            elif posicion_opcion == "Abajo Centro":
                pos = ((img.width - logo.width) // 2, img.height - logo.height - 20)
            elif posicion_opcion == "Abajo Izquierda":
                pos = (20, img.height - logo.height - 20)
            elif posicion_opcion == "Arriba Derecha":
                pos = (img.width - logo.width - 20, 20)
            elif posicion_opcion == "Arriba Izquierda":
                pos = (20, 20)
            else: # Centro
                pos = ((img.width - logo.width) // 2, (img.height - logo.height) // 2)

            watermarked = img.copy()
            watermarked.paste(logo, pos, logo)
            final_img = watermarked.convert("RGB")
            
            st.image(final_img, caption=f"Foto {idx+1}: {file.name}", use_column_width=True)
            
            # Descarga directa
            buf = io.BytesIO()
            final_img.save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()
            
            st.download_button(
                label=f"⬇️ Descargar Foto {idx+1}",
                data=byte_im,
                file_name=f"metalcraft_{file.name}",
                mime="image/jpeg",
                key=f"dl_{idx}"
            )
            st.divider()
    else:
        st.error("No se encontró el archivo logo.png en el repositorio.")
        
