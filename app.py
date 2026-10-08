import streamlit as st
from PIL import Image
import os
import io

st.set_page_config(page_title="Metalcraft - Marca de Agua", page_icon="🛠️", layout="centered")

st.title("🛠️ Metalcraft - Marca de Agua y Fichas")

# --- SECCIÓN 1: MARCA DE AGUA EN FOTOS ---
st.header("📷 Procesador de Imágenes Múltiple")

# Opciones de posición para la marca de agua
posicion_opcion = st.selectbox(
    "Ubicación de la marca de agua:",
    [
        "Abajo Derecha", 
        "Abajo Centro", 
        "Abajo Izquierda", 
        "Arriba Derecha", 
        "Centro", 
        "Arriba Izquierda"
    ]
)

# Carga de múltiples imágenes (Soporta selección masiva desde Galería)
uploaded_files = st.file_uploader(
    "Selecciona una o varias imágenes de tu galería:", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Cargar logo de marca de agua
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo_base = Image.open(logo_path).convert("RGBA")
        
        st.subheader(f"🖼️ Imágenes procesadas ({len(uploaded_files)}):")
        
        for idx, file in enumerate(uploaded_files):
            img = Image.open(file).convert("RGBA")
            
            # Ajustar logo al 20% del ancho de la imagen
            base_width = int(img.width * 0.20)
            w_percent = (base_width / float(logo_base.width))
            h_size = int((float(logo_base.height) * float(w_percent)))
            logo = logo_base.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            # Lógica de cálculo de posiciones
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
            else:  # Centro
                pos = ((img.width - logo.width) // 2, (img.height - logo.height) // 2)

            # Aplicar marca de agua
            watermarked = img.copy()
            watermarked.paste(logo, pos, logo)
            final_img = watermarked.convert("RGB")
            
            # Mostrar vista previa
            st.image(final_img, caption=f"Foto {idx+1}: {file.name}", use_column_width=True)
            
            # Preparar buffer en memoria para la descarga
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

# --- SECCIÓN 2: REDACCIÓN Y PLANTILLA DE TEXTOS ---
st.header("📝 Generador de Fichas y Publicaciones")

producto = st.text_input("Nombre del equipo / producto:", "Estufa industrial con 2 freidoras y plancha")
detalles = st.text_area("Detalles técnicos (medidas, calibre, acero, quemadores, etc.):", "Fabricado en acero inoxidable, quemadores H de alta presión, tina en acero 304.")

if st.button("📋 Generar plantilla de venta"):
    plantilla = f"""🔥 **{producto.upper()} - METALCRAFT** 🔥

🛠️ **Especificaciones y Detalles:**
{detalles}

✅ **Fabricación de alta durabilidad y calidad industrial.**
🚛 Envíos a todo el país / Entregas locales.

📲 **Cotizaciones y pedidos vía WhatsApp.**
¡Contáctanos para personalizar tu equipo a la medida!"""

    st.success("¡Texto generado!")
    st.text_area("Copia y pega este texto directamente en WhatsApp o Facebook:", value=plantilla, height=220)
    
