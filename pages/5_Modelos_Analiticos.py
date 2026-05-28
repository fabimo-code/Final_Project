import streamlit as st

st.set_page_config(page_title="Modelos Analíticos", page_icon="🤖", layout="wide")

st.title("🤖 Modelos Analíticos")
st.markdown(
    """
Esta sección se desarrollará como componente complementario del dashboard.

Modelos previstos:

- **Random Forest:** clasificación exploratoria de riesgo alto.
- **Regresión Logística:** estimación de probabilidad de riesgo alto.
- **K-Means:** identificación de agrupamientos temporales por hora y mes.

Los modelos se presentarán como apoyo analítico y no como sistema oficial de predicción institucional.
"""
)

st.info("En la siguiente iteración adaptaremos el código del proyecto anterior para esta página.")
