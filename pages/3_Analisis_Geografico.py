import streamlit as st
import plotly.express as px

from src.data_prep import cargar_datos, aplicar_filtros
from src.visuals import COLOR_GRAVEDAD


st.set_page_config(
    page_title="Análisis Geográfico",
    page_icon="🗺️",
    layout="wide"
)

# =========================
# CARGA DE DATOS
# =========================
df = cargar_datos()

st.title("🗺️ Análisis Geográfico de Siniestralidad Vial")

st.markdown("""
Esta vista permite identificar la concentración territorial de los siniestros viales en Bogotá. 
El análisis se enfoca en localidades críticas, distribución espacial de los accidentes y severidad por territorio.
""")

st.markdown("""
Esta vista será clave para responder:
¿Cuáles son las localidades con mayor concentración de accidentes?
¿Qué zonas requieren priorización de intervención preventiva?
""")

# =========================
# SIDEBAR - FILTROS
# =========================
with st.sidebar:
    st.header("🔎 Filtros de análisis")

    anio_min = int(df["ANIO"].min())
    anio_max = int(df["ANIO"].max())

    rango_anios = st.slider(
        "Rango de años",
        min_value=anio_min,
        max_value=anio_max,
        value=(anio_min, anio_max),
        key="geo_rango_anios"
    )

    localidades = st.multiselect(
        "Localidad",
        options=sorted(df["LOCALIDAD"].dropna().unique()),
        default=sorted(df["LOCALIDAD"].dropna().unique()),
        key="geo_localidades"
    )

    gravedades = st.multiselect(
        "Gravedad",
        options=sorted(df["GRAVEDAD"].dropna().unique()),
        default=sorted(df["GRAVEDAD"].dropna().unique()),
        key="geo_gravedades"
    )

    clases = st.multiselect(
        "Clase de accidente",
        options=sorted(df["CLASE_ACC"].dropna().unique()),
        default=sorted(df["CLASE_ACC"].dropna().unique()),
        key="geo_clases"
    )

df_filtrado = aplicar_filtros(
    df,
    rango_anios=rango_anios,
    localidades=localidades,
    gravedades=gravedades,
    clases=clases
)

if df_filtrado.empty:
    st.warning("No hay datos disponibles con los filtros seleccionados. Ajusta los filtros para continuar.")
    st.stop()

# =========================
# DATOS PARA MAPA
# =========================
df_mapa = df_filtrado.dropna(subset=["LATITUD", "LONGITUD"]).copy()

# Filtramos coordenadas aproximadas válidas para Bogotá.
df_mapa = df_mapa[
    (df_mapa["LATITUD"].between(4.3, 4.9)) &
    (df_mapa["LONGITUD"].between(-74.4, -73.8))
]

# Para rendimiento visual, limitamos puntos si hay demasiados registros.
max_puntos = 8000
if len(df_mapa) > max_puntos:
    df_mapa_plot = df_mapa.sample(max_puntos, random_state=42)
else:
    df_mapa_plot = df_mapa.copy()

# =========================
# KPIS GEOGRÁFICOS
# =========================
st.subheader("Indicadores geográficos")

acc_localidad = (
    df_filtrado
    .groupby("LOCALIDAD")
    .size()
    .reset_index(name="Accidentes")
    .sort_values("Accidentes", ascending=False)
)

localidad_critica = acc_localidad.iloc[0]["LOCALIDAD"]
acc_localidad_critica = int(acc_localidad.iloc[0]["Accidentes"])

top5_acc = int(acc_localidad.head(5)["Accidentes"].sum())
total_acc = len(df_filtrado)
porcentaje_top5 = (top5_acc / total_acc) * 100 if total_acc > 0 else 0

localidades_analizadas = df_filtrado["LOCALIDAD"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Localidad crítica", localidad_critica)
col2.metric("Accidentes en localidad crítica", f"{acc_localidad_critica:,}".replace(",", "."))
col3.metric("% concentrado en Top 5", f"{porcentaje_top5:.2f}%")

col4, col5 = st.columns(2)

col4.metric("Localidades analizadas", localidades_analizadas)
col5.metric("Registros con coordenadas válidas", f"{len(df_mapa):,}".replace(",", "."))

st.divider()

# =========================
# LECTURA EJECUTIVA
# =========================
st.subheader("Lectura geográfica")

st.markdown(f"""
Con los filtros seleccionados, la localidad con mayor concentración de accidentes es 
**{localidad_critica}**, con **{acc_localidad_critica:,} registros**. 
Además, las cinco localidades con mayor accidentalidad concentran aproximadamente 
**{porcentaje_top5:.2f}%** del total de siniestros analizados.
""".replace(",", "."))

st.divider()

# =========================
# VISUALIZACIONES
# =========================
st.subheader("Visualizaciones territoriales")

tab1, tab2, tab3 = st.tabs([
    "Ranking de localidades",
    "Mapa de accidentes",
    "Gravedad por localidad"
])

with tab1:
    top_localidades = acc_localidad.head(15).sort_values("Accidentes", ascending=True)

    fig_ranking = px.bar(
        top_localidades,
        x="Accidentes",
        y="LOCALIDAD",
        orientation="h",
        title="Top 15 localidades con mayor número de accidentes"
    )

    fig_ranking.update_layout(
        xaxis_title="Número de accidentes",
        yaxis_title="Localidad"
    )

    st.plotly_chart(fig_ranking, use_container_width=True)

    st.caption(
        "Este ranking permite identificar las localidades que deberían priorizarse para análisis preventivo."
    )

with tab2:
    if df_mapa_plot.empty:
        st.warning("No hay coordenadas válidas para construir el mapa con los filtros seleccionados.")
    else:
        fig_mapa = px.scatter_map(
            df_mapa_plot,
            lat="LATITUD",
            lon="LONGITUD",
            color="GRAVEDAD",
            color_discrete_map=COLOR_GRAVEDAD,
            hover_name="LOCALIDAD",
            hover_data={
                "CLASE_ACC": True,
                "GRAVEDAD": True,
                "ANIO": True,
                "LATITUD": False,
                "LONGITUD": False
            },
            zoom=10,
            height=650,
            title="Mapa de siniestros viales georreferenciados"
        )

        fig_mapa.update_layout(
            map_style="open-street-map",
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            legend_title_text="Gravedad"
        )

        st.plotly_chart(fig_mapa, use_container_width=True)

        if len(df_mapa) > max_puntos:
            st.info(
                f"Para mejorar el rendimiento, el mapa muestra una muestra aleatoria de "
                f"{max_puntos:,} puntos de {len(df_mapa):,} registros con coordenadas válidas.".replace(",", ".")
            )

with tab3:
    gravedad_localidad = (
        df_filtrado
        .groupby(["LOCALIDAD", "GRAVEDAD"])
        .size()
        .reset_index(name="Accidentes")
    )

    top10_localidades = acc_localidad.head(10)["LOCALIDAD"].tolist()
    gravedad_localidad_top = gravedad_localidad[
        gravedad_localidad["LOCALIDAD"].isin(top10_localidades)
    ]

    fig_gravedad_localidad = px.bar(
        gravedad_localidad_top,
        x="LOCALIDAD",
        y="Accidentes",
        color="GRAVEDAD",
        color_discrete_map=COLOR_GRAVEDAD,
        title="Distribución de gravedad en las 10 localidades con más accidentes"
    )

    fig_gravedad_localidad.update_layout(
        xaxis_title="Localidad",
        yaxis_title="Número de accidentes",
        legend_title_text="Gravedad",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_gravedad_localidad, use_container_width=True)

    st.caption(
        "Esta visualización permite comparar si las localidades con más accidentes también concentran eventos de mayor severidad."
    )

st.divider()

# =========================
# TABLA DE PRIORIZACIÓN
# =========================
st.subheader("Tabla de priorización territorial")

riesgo_localidad = (
    df_filtrado
    .groupby("LOCALIDAD")
    .agg(
        total_accidentes=("LOCALIDAD", "size"),
        accidentes_riesgo_alto=("RIESGO_ALTO", "sum")
    )
    .reset_index()
)

riesgo_localidad["porcentaje_riesgo_alto"] = (
    riesgo_localidad["accidentes_riesgo_alto"] /
    riesgo_localidad["total_accidentes"] * 100
)

riesgo_localidad = riesgo_localidad.sort_values(
    ["total_accidentes", "porcentaje_riesgo_alto"],
    ascending=[False, False]
)

riesgo_localidad_mostrar = riesgo_localidad.rename(columns={
    "LOCALIDAD": "Localidad",
    "total_accidentes": "Total accidentes",
    "accidentes_riesgo_alto": "Accidentes riesgo alto",
    "porcentaje_riesgo_alto": "% riesgo alto"
})

riesgo_localidad_mostrar["% riesgo alto"] = riesgo_localidad_mostrar["% riesgo alto"].round(2)

st.dataframe(
    riesgo_localidad_mostrar,
    use_container_width=True,
    hide_index=True
)