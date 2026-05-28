import streamlit as st

from src.data_prep import cargar_datos, crear_sidebar_filtros
from src.visuals import grafico_accidentes_por_hora, grafico_accidentes_por_mes, grafico_evolucion_anual

st.set_page_config(page_title="Análisis Temporal", page_icon="⏱️", layout="wide")

st.title("⏱️ Análisis Temporal")
st.markdown("Exploración de patrones de accidentalidad por año, mes y hora.")

df = cargar_datos()
df_filtrado = crear_sidebar_filtros(df)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

st.plotly_chart(grafico_evolucion_anual(df_filtrado), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grafico_accidentes_por_mes(df_filtrado), use_container_width=True)
with col2:
    st.plotly_chart(grafico_accidentes_por_hora(df_filtrado), use_container_width=True)

st.info("En una siguiente iteración agregaremos un heatmap de hora vs. día de la semana para detectar franjas críticas.")
