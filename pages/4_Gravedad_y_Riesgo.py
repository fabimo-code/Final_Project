import streamlit as st
import plotly.express as px

from src.data_prep import cargar_datos, crear_sidebar_filtros
from src.visuals import COLOR_GRAVEDAD, grafico_distribucion_gravedad

st.set_page_config(page_title="Gravedad y Riesgo", page_icon="⚠️", layout="wide")

st.title("⚠️ Gravedad y Riesgo")
st.markdown("Análisis de severidad de los siniestros viales y eventos clasificados como riesgo alto.")

df = cargar_datos()
df_filtrado = crear_sidebar_filtros(df)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grafico_distribucion_gravedad(df_filtrado), use_container_width=True)

with col2:
    data = (
        df_filtrado.groupby(["LOCALIDAD", "GRAVEDAD"], as_index=False)
        .size()
        .rename(columns={"size": "Accidentes"})
    )
    top_localidades = df_filtrado["LOCALIDAD"].value_counts().head(10).index
    data = data[data["LOCALIDAD"].isin(top_localidades)]
    fig = px.bar(
        data,
        x="LOCALIDAD",
        y="Accidentes",
        color="GRAVEDAD",
        color_discrete_map=COLOR_GRAVEDAD,
        title="Gravedad por localidad (Top 10)",
    )
    fig.update_layout(xaxis_title="Localidad", yaxis_title="Accidentes", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Riesgo alto por hora")
data_hora = (
    df_filtrado.groupby("HORA", as_index=False)["RIESGO_ALTO"]
    .mean()
    .rename(columns={"RIESGO_ALTO": "Proporción riesgo alto"})
)
data_hora["Porcentaje riesgo alto"] = data_hora["Proporción riesgo alto"] * 100
fig = px.line(
    data_hora,
    x="HORA",
    y="Porcentaje riesgo alto",
    markers=True,
    title="Porcentaje de riesgo alto por hora",
)
st.plotly_chart(fig, use_container_width=True)
