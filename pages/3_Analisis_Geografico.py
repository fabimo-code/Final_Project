import streamlit as st
import plotly.express as px

from src.data_prep import cargar_datos, crear_sidebar_filtros, datos_para_mapa
from src.visuals import grafico_top_localidades

st.set_page_config(page_title="Análisis Geográfico", page_icon="🗺️", layout="wide")

st.title("🗺️ Análisis Geográfico")
st.markdown("Identificación de localidades y zonas con mayor concentración de siniestros.")

df = cargar_datos()
df_filtrado = crear_sidebar_filtros(df)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

st.plotly_chart(grafico_top_localidades(df_filtrado, n=15), use_container_width=True)

st.subheader("Mapa de siniestros")
df_mapa = datos_para_mapa(df_filtrado)

if df_mapa.empty:
    st.warning("No hay registros con coordenadas válidas para el mapa.")
else:
    # Muestra una muestra controlada para mantener buen rendimiento en Streamlit.
    muestra = df_mapa.sample(min(len(df_mapa), 10000), random_state=42)
    fig = px.scatter_mapbox(
        muestra,
        lat="LATITUD",
        lon="LONGITUD",
        color="GRAVEDAD",
        hover_data=["LOCALIDAD", "CLASE_ACC", "FECHA_HORA_ACC"],
        zoom=10,
        height=650,
        title="Distribución espacial de siniestros viales",
        mapbox_style="open-street-map",
        color_discrete_map={
            "SOLO DANOS": "#6B7280",
            "CON HERIDOS": "#F59E0B",
            "CON MUERTOS": "#DC2626",
        },
    )
    st.plotly_chart(fig, use_container_width=True)
