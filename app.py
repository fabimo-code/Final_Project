import streamlit as st

st.set_page_config(
    page_title="Siniestralidad Vial Bogotá",
    page_icon="🚦",
    layout="wide",
)

st.title("🚦 Plataforma Visual Interactiva para el Monitoreo y Análisis de Siniestralidad Vial en Bogotá")

st.markdown(
    """
Esta aplicación permite analizar la siniestralidad vial en Bogotá a partir de datos históricos de accidentes de tránsito.

El dashboard busca facilitar la identificación de patrones temporales, geográficos y de gravedad para apoyar procesos de monitoreo, prevención y toma de decisiones en movilidad y seguridad vial.
"""
)

st.subheader("Audiencia objetivo")
st.markdown(
    """
- Secretaría Distrital de Movilidad.
- Analistas de movilidad urbana.
- Entidades de seguridad vial.
- Tomadores de decisiones del sector público.
"""
)

st.subheader("Navegación")
st.info(
    "Usa el menú lateral para recorrer las páginas del dashboard: Vista Ejecutiva, Análisis Temporal, Análisis Geográfico, Gravedad y Riesgo, Modelos Analíticos y Conclusiones."
)

st.markdown(
    """
### Estructura del análisis

1. **Vista Ejecutiva:** KPIs principales y panorama general.
2. **Análisis Temporal:** evolución anual, mensual y horaria.
3. **Análisis Geográfico:** localidades críticas y distribución espacial.
4. **Gravedad y Riesgo:** severidad de los accidentes.
5. **Conclusiones:** hallazgos y recomendaciones.
"""
)
