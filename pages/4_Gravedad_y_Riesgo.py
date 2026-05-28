import streamlit as st
import plotly.express as px

from src.data_prep import cargar_datos, aplicar_filtros
from src.visuals import COLOR_GRAVEDAD


st.set_page_config(
    page_title="Gravedad y Riesgo",
    page_icon="🚨",
    layout="wide"
)

# =========================
# CARGA DE DATOS
# =========================
df = cargar_datos()

st.title("🚨 Análisis de Gravedad y Riesgo")

st.markdown("""
Esta vista analiza la severidad de los siniestros viales en Bogotá, diferenciando entre accidentes de solo daños,
accidentes con heridos y accidentes con muertos. También permite identificar patrones asociados a eventos de riesgo alto.
""")

st.markdown("""
Esta vista profundiza en:
¿Qué tipos de accidentes presentan mayor gravedad?
¿Qué variables están relacionadas con accidentes de mayor severidad?
¿Dónde y cuándo se concentra el riesgo alto?
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
        key="riesgo_rango_anios"
    )

    localidades = st.multiselect(
        "Localidad",
        options=sorted(df["LOCALIDAD"].dropna().unique()),
        default=sorted(df["LOCALIDAD"].dropna().unique()),
        key="riesgo_localidades"
    )

    gravedades = st.multiselect(
        "Gravedad",
        options=sorted(df["GRAVEDAD"].dropna().unique()),
        default=sorted(df["GRAVEDAD"].dropna().unique()),
        key="riesgo_gravedades"
    )

    clases = st.multiselect(
        "Clase de accidente",
        options=sorted(df["CLASE_ACC"].dropna().unique()),
        default=sorted(df["CLASE_ACC"].dropna().unique()),
        key="riesgo_clases"
    )

    meses = st.multiselect(
        "Mes",
        options=sorted(df["MES"].dropna().unique()),
        default=sorted(df["MES"].dropna().unique()),
        key="riesgo_meses"
    )

df_filtrado = aplicar_filtros(
    df,
    rango_anios=rango_anios,
    localidades=localidades,
    gravedades=gravedades,
    clases=clases,
    meses=meses
)

if df_filtrado.empty:
    st.warning("No hay datos disponibles con los filtros seleccionados. Ajusta los filtros para continuar.")
    st.stop()

# =========================
# KPIS DE RIESGO
# =========================
st.subheader("Indicadores de severidad")

total_accidentes = len(df_filtrado)
acc_solo_danos = int((df_filtrado["GRAVEDAD"] == "SOLO DANOS").sum())
acc_heridos = int((df_filtrado["GRAVEDAD"] == "CON HERIDOS").sum())
acc_muertos = int((df_filtrado["GRAVEDAD"] == "CON MUERTOS").sum())
acc_riesgo_alto = int(df_filtrado["RIESGO_ALTO"].sum())

porc_riesgo_alto = (acc_riesgo_alto / total_accidentes) * 100 if total_accidentes > 0 else 0
porc_muertos = (acc_muertos / total_accidentes) * 100 if total_accidentes > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total accidentes", f"{total_accidentes:,}".replace(",", "."))
col2.metric("Riesgo alto", f"{acc_riesgo_alto:,}".replace(",", "."))
col3.metric("% riesgo alto", f"{porc_riesgo_alto:.2f}%")
col4.metric("Accidentes con muertos", f"{acc_muertos:,}".replace(",", "."))

col5, col6, col7 = st.columns(3)

col5.metric("Solo daños", f"{acc_solo_danos:,}".replace(",", "."))
col6.metric("Con heridos", f"{acc_heridos:,}".replace(",", "."))
col7.metric("% con muertos", f"{porc_muertos:.2f}%")

st.divider()

# =========================
# LECTURA EJECUTIVA
# =========================
st.subheader("Lectura ejecutiva del riesgo")

st.markdown(f"""
Con los filtros seleccionados, se identifican **{acc_riesgo_alto:,} accidentes de riesgo alto**, 
equivalentes al **{porc_riesgo_alto:.2f}%** del total analizado. 
Esta categoría agrupa los siniestros con **heridos** o **muertos**, por lo que representa el componente más relevante 
para acciones de prevención y priorización institucional.
""".replace(",", "."))

st.divider()

# =========================
# VISUALIZACIONES
# =========================
st.subheader("Visualizaciones de gravedad y riesgo")

tab1, tab2, tab3, tab4 = st.tabs([
    "Distribución de gravedad",
    "Riesgo por localidad",
    "Clase de accidente",
    "Riesgo temporal"
])

with tab1:
    gravedad = (
        df_filtrado
        .groupby("GRAVEDAD")
        .size()
        .reset_index(name="Accidentes")
        .sort_values("Accidentes", ascending=False)
    )

    col_a, col_b = st.columns(2)

    with col_a:
        fig_bar_gravedad = px.bar(
            gravedad,
            x="GRAVEDAD",
            y="Accidentes",
            color="GRAVEDAD",
            color_discrete_map=COLOR_GRAVEDAD,
            title="Accidentes por gravedad"
        )

        fig_bar_gravedad.update_layout(
            xaxis_title="Gravedad",
            yaxis_title="Número de accidentes",
            showlegend=False
        )

        st.plotly_chart(fig_bar_gravedad, use_container_width=True)

    with col_b:
        fig_pie_gravedad = px.pie(
            gravedad,
            names="GRAVEDAD",
            values="Accidentes",
            color="GRAVEDAD",
            color_discrete_map=COLOR_GRAVEDAD,
            title="Participación porcentual por gravedad",
            hole=0.45
        )

        fig_pie_gravedad.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig_pie_gravedad, use_container_width=True)

    st.caption(
        "La distribución por gravedad permite diferenciar los eventos de solo daños frente a los siniestros con consecuencias sobre la vida o integridad de las personas."
    )

with tab2:
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

    top_riesgo_localidad = riesgo_localidad.sort_values(
        "accidentes_riesgo_alto",
        ascending=False
    ).head(15)

    fig_riesgo_localidad = px.bar(
        top_riesgo_localidad.sort_values("accidentes_riesgo_alto", ascending=True),
        x="accidentes_riesgo_alto",
        y="LOCALIDAD",
        orientation="h",
        title="Top 15 localidades por accidentes de riesgo alto"
    )

    fig_riesgo_localidad.update_layout(
        xaxis_title="Accidentes de riesgo alto",
        yaxis_title="Localidad"
    )

    st.plotly_chart(fig_riesgo_localidad, use_container_width=True)

    fig_porc_riesgo = px.bar(
        top_riesgo_localidad.sort_values("porcentaje_riesgo_alto", ascending=True),
        x="porcentaje_riesgo_alto",
        y="LOCALIDAD",
        orientation="h",
        title="% de riesgo alto en localidades con mayor volumen de riesgo"
    )

    fig_porc_riesgo.update_layout(
        xaxis_title="% riesgo alto",
        yaxis_title="Localidad"
    )

    st.plotly_chart(fig_porc_riesgo, use_container_width=True)

with tab3:
    clase_gravedad = (
        df_filtrado
        .groupby(["CLASE_ACC", "GRAVEDAD"])
        .size()
        .reset_index(name="Accidentes")
    )

    fig_clase_gravedad = px.bar(
        clase_gravedad,
        x="CLASE_ACC",
        y="Accidentes",
        color="GRAVEDAD",
        color_discrete_map=COLOR_GRAVEDAD,
        title="Clase de accidente según gravedad"
    )

    fig_clase_gravedad.update_layout(
        xaxis_title="Clase de accidente",
        yaxis_title="Número de accidentes",
        legend_title_text="Gravedad",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig_clase_gravedad, use_container_width=True)

    clase_riesgo = (
        df_filtrado
        .groupby("CLASE_ACC")
        .agg(
            total_accidentes=("CLASE_ACC", "size"),
            accidentes_riesgo_alto=("RIESGO_ALTO", "sum")
        )
        .reset_index()
    )

    clase_riesgo["porcentaje_riesgo_alto"] = (
        clase_riesgo["accidentes_riesgo_alto"] /
        clase_riesgo["total_accidentes"] * 100
    )

    clase_riesgo = clase_riesgo.sort_values("porcentaje_riesgo_alto", ascending=False)

    st.dataframe(
        clase_riesgo.rename(columns={
            "CLASE_ACC": "Clase de accidente",
            "total_accidentes": "Total accidentes",
            "accidentes_riesgo_alto": "Accidentes riesgo alto",
            "porcentaje_riesgo_alto": "% riesgo alto"
        }).assign(
            **{"% riesgo alto": clase_riesgo["porcentaje_riesgo_alto"].round(2)}
        ),
        use_container_width=True,
        hide_index=True
    )

with tab4:
    riesgo_hora = (
        df_filtrado
        .groupby("HORA")
        .agg(
            total_accidentes=("HORA", "size"),
            accidentes_riesgo_alto=("RIESGO_ALTO", "sum")
        )
        .reset_index()
        .sort_values("HORA")
    )

    riesgo_hora["porcentaje_riesgo_alto"] = (
        riesgo_hora["accidentes_riesgo_alto"] /
        riesgo_hora["total_accidentes"] * 100
    )

    fig_riesgo_hora = px.line(
        riesgo_hora,
        x="HORA",
        y="accidentes_riesgo_alto",
        markers=True,
        title="Accidentes de riesgo alto por hora"
    )

    fig_riesgo_hora.update_layout(
        xaxis_title="Hora del día",
        yaxis_title="Accidentes de riesgo alto",
        xaxis=dict(dtick=1),
        hovermode="x unified"
    )

    st.plotly_chart(fig_riesgo_hora, use_container_width=True)

    fig_porc_hora = px.bar(
        riesgo_hora,
        x="HORA",
        y="porcentaje_riesgo_alto",
        title="% de riesgo alto por hora"
    )

    fig_porc_hora.update_layout(
        xaxis_title="Hora del día",
        yaxis_title="% riesgo alto",
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(fig_porc_hora, use_container_width=True)

st.divider()

# =========================
# TABLA FINAL
# =========================
st.subheader("Resumen por gravedad")

tabla_gravedad = (
    df_filtrado
    .groupby("GRAVEDAD")
    .size()
    .reset_index(name="Accidentes")
)

tabla_gravedad["Porcentaje"] = (
    tabla_gravedad["Accidentes"] / tabla_gravedad["Accidentes"].sum() * 100
).round(2)

tabla_gravedad = tabla_gravedad.sort_values("Accidentes", ascending=False)

st.dataframe(
    tabla_gravedad.rename(columns={
        "GRAVEDAD": "Gravedad"
    }),
    use_container_width=True,
    hide_index=True
)

