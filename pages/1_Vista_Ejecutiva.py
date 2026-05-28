import streamlit as st
import plotly.express as px

from src.data_prep import cargar_datos, aplicar_filtros
from src.kpis import calcular_kpis
from src.visuals import COLOR_GRAVEDAD


st.set_page_config(
    page_title="Vista Ejecutiva",
    page_icon="📊",
    layout="wide"
)

# =========================
# CARGA DE DATOS
# =========================
df = cargar_datos()

st.title("📊 Vista Ejecutiva de Siniestralidad Vial en Bogotá")

st.markdown("""
Esta vista resume el comportamiento general de los siniestros viales en Bogotá, 
permitiendo identificar rápidamente la magnitud del fenómeno, la severidad de los eventos, 
las localidades críticas y los patrones temporales más relevantes.
""")

st.info(
    "Audiencia objetivo: Secretaría Distrital de Movilidad, analistas de movilidad urbana, entidades de seguridad vial y tomadores de decisiones del sector público."
)

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
        value=(anio_min, anio_max)
    )

    localidades = st.multiselect(
        "Localidad",
        options=sorted(df["LOCALIDAD"].dropna().unique()),
        default=sorted(df["LOCALIDAD"].dropna().unique())
    )

    gravedades = st.multiselect(
        "Gravedad",
        options=sorted(df["GRAVEDAD"].dropna().unique()),
        default=sorted(df["GRAVEDAD"].dropna().unique())
    )

    clases = st.multiselect(
        "Clase de accidente",
        options=sorted(df["CLASE_ACC"].dropna().unique()),
        default=sorted(df["CLASE_ACC"].dropna().unique())
    )

df_filtrado = aplicar_filtros(
    df,
    rango_anios=rango_anios,
    localidades=localidades,
    gravedades=gravedades,
    clases=clases
)

kpis = calcular_kpis(df_filtrado)

# =========================
# VALIDACIÓN
# =========================
if df_filtrado.empty:
    st.warning("No hay datos disponibles con los filtros seleccionados. Ajusta los filtros para continuar.")
    st.stop()

# =========================
# KPIS PRINCIPALES
# =========================
st.subheader("Indicadores clave")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total de accidentes",
    value=f"{kpis['total_accidentes']:,}".replace(",", ".")
)

col2.metric(
    label="% riesgo alto",
    value=f"{kpis['porcentaje_riesgo_alto']:.2f}%"
)

col3.metric(
    label="Accidentes con heridos",
    value=f"{kpis['accidentes_heridos']:,}".replace(",", ".")
)

col4.metric(
    label="Accidentes con muertos",
    value=f"{kpis['accidentes_muertos']:,}".replace(",", ".")
)

col5, col6, col7 = st.columns(3)

col5.metric(
    label="Localidad crítica",
    value=kpis["localidad_critica"]
)

col6.metric(
    label="Hora pico",
    value=f"{kpis['hora_pico']}:00"
)

col7.metric(
    label="Mes crítico",
    value=kpis["mes_critico"]
)

st.divider()

# =========================
# HALLAZGO EJECUTIVO
# =========================
st.subheader("Lectura ejecutiva")

st.markdown(f"""
Con los filtros seleccionados, se registran **{kpis['total_accidentes']:,} accidentes**. 
La localidad con mayor concentración es **{kpis['localidad_critica']}**, 
la hora con mayor frecuencia es **{kpis['hora_pico']}:00** 
y el porcentaje de accidentes clasificados como riesgo alto es **{kpis['porcentaje_riesgo_alto']:.2f}%**.
""".replace(",", "."))

st.divider()

# =========================
# VISUALIZACIONES
# =========================
st.subheader("Visualizaciones principales")

col_a, col_b = st.columns(2)

with col_a:
    acc_anio = (
        df_filtrado
        .groupby("ANIO")
        .size()
        .reset_index(name="Accidentes")
        .sort_values("ANIO")
    )

    fig_anio = px.line(
        acc_anio,
        x="ANIO",
        y="Accidentes",
        markers=True,
        title="Evolución anual de accidentes"
    )

    fig_anio.update_layout(
        xaxis_title="Año",
        yaxis_title="Número de accidentes",
        hovermode="x unified"
    )

    st.plotly_chart(fig_anio, use_container_width=True)

with col_b:
    gravedad = (
        df_filtrado
        .groupby("GRAVEDAD")
        .size()
        .reset_index(name="Accidentes")
        .sort_values("Accidentes", ascending=False)
    )

    fig_gravedad = px.bar(
        gravedad,
        x="GRAVEDAD",
        y="Accidentes",
        color="GRAVEDAD",
        color_discrete_map=COLOR_GRAVEDAD,
        title="Distribución por gravedad"
    )

    fig_gravedad.update_layout(
        xaxis_title="Gravedad",
        yaxis_title="Número de accidentes",
        showlegend=False
    )

    st.plotly_chart(fig_gravedad, use_container_width=True)

top_localidades = (
    df_filtrado
    .groupby("LOCALIDAD")
    .size()
    .reset_index(name="Accidentes")
    .sort_values("Accidentes", ascending=False)
    .head(10)
)

fig_localidades = px.bar(
    top_localidades,
    x="Accidentes",
    y="LOCALIDAD",
    orientation="h",
    title="Top 10 localidades con mayor número de accidentes"
)

fig_localidades.update_layout(
    xaxis_title="Número de accidentes",
    yaxis_title="Localidad",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig_localidades, use_container_width=True)

