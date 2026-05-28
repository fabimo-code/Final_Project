import streamlit as st

from src.data_prep import cargar_datos, crear_sidebar_filtros
from src.kpis import calcular_kpis
from src.visuals import (
    grafico_distribucion_gravedad,
    grafico_evolucion_anual,
    grafico_top_localidades,
)

st.set_page_config(page_title="Vista Ejecutiva", page_icon="📊", layout="wide")

st.title("📊 Vista Ejecutiva")
st.markdown(
    """
Esta vista resume el comportamiento general de los siniestros viales en Bogotá mediante indicadores clave, filtros interactivos y visualizaciones principales.
"""
)

try:
    df = cargar_datos()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

df_filtrado = crear_sidebar_filtros(df)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados. Ajusta los filtros en el menú lateral.")
    st.stop()

kpis = calcular_kpis(df_filtrado)

st.subheader("Indicadores clave")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total accidentes", f"{kpis['total_accidentes']:,}".replace(",", "."))
col2.metric("% riesgo alto", f"{kpis['porcentaje_riesgo_alto']}%")
col3.metric("Con heridos", f"{kpis['accidentes_heridos']:,}".replace(",", "."))
col4.metric("Con muertos", f"{kpis['accidentes_muertos']:,}".replace(",", "."))
col5.metric("Hora pico", f"{kpis['hora_pico']}:00" if isinstance(kpis['hora_pico'], int) else kpis['hora_pico'])

st.caption(
    f"Localidad crítica según los filtros actuales: **{kpis['localidad_critica']}**. Mes con mayor accidentalidad: **{kpis['mes_critico']}**."
)

st.divider()

col_a, col_b = st.columns((1.2, 1))

with col_a:
    st.plotly_chart(grafico_evolucion_anual(df_filtrado), use_container_width=True)

with col_b:
    st.plotly_chart(grafico_distribucion_gravedad(df_filtrado), use_container_width=True)

st.plotly_chart(grafico_top_localidades(df_filtrado), use_container_width=True)

st.subheader("Lectura ejecutiva")
st.markdown(
    f"""
Con los filtros seleccionados, la localidad con mayor concentración de accidentes es **{kpis['localidad_critica']}** y la hora de mayor ocurrencia es **{kpis['hora_pico']}:00**.

El porcentaje de accidentes clasificados como riesgo alto, es decir, eventos con heridos o muertos, corresponde al **{kpis['porcentaje_riesgo_alto']}%** del total filtrado.
"""
)
