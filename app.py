import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Metalcraft Catálogo", page_icon="🛠️", layout="wide")

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=950, scrolling=True)
except Exception as e:
    st.error(f"Error al leer index.html: {e}")
  
