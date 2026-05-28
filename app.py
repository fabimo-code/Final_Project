import streamlit as st

st.set_page_config(
    page_title="Siniestralidad Vial Bogotá",
    page_icon="🚦",
    layout="wide"
)

st.title("Plataforma Visual Interactiva para el Monitoreo y Análisis de Siniestralidad Vial en Bogotá")

st.markdown("""
Bienvenido al dashboard interactivo para el análisis estratégico de siniestros viales en Bogotá.

Utiliza el menú lateral para navegar entre las diferentes vistas analíticas:
- Vista Ejecutiva
- Análisis Temporal
- Análisis Geográfico
- Gravedad y Riesgo
- Modelos Analíticos
- Conclusiones
""")

st.info(
    "Esta herramienta está orientada a apoyar procesos de monitoreo, prevención y toma de decisiones en movilidad y seguridad vial."
)