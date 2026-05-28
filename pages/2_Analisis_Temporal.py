import streamlit as st
import plotly.express as px

from src.data_prep import cargar_datos, aplicar_filtros
from src.visuals import COLOR_GRAVEDAD


st.set_page_config(
    page_title="Análisis Temporal",
    page_icon="⏱️",
    layout="wide"
)

# =========================
# CARGA DE DATOS
# =========================
df = cargar_datos()

st.title("⏱️ Análisis Temporal de la Siniestralidad Vial")

st.markdown("""
Esta vista permite explorar la evolución de los siniestros viales en Bogotá a través del tiempo. 
El análisis se concentra en patrones anuales, mensuales, horarios y combinaciones entre día de la semana y hora del accidente.
""")

st.markdown("""
Además responde directamente a estas preguntas del proyecto:
¿Qué horarios presentan mayor frecuencia de siniestralidad?
¿Cómo ha evolucionado la accidentalidad a través del tiempo?
¿Existen patrones temporales recurrentes asociados al riesgo?
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
        key="temporal_rango_anios"
    )

    localidades = st.multiselect(
        "Localidad",
        options=sorted(df["LOCALIDAD"].dropna().unique()),
        default=sorted(df["LOCALIDAD"].dropna().unique()),
        key="temporal_localidades"
    )

    gravedades = st.multiselect(
        "Gravedad",
        options=sorted(df["GRAVEDAD"].dropna().unique()),
        default=sorted(df["GRAVEDAD"].dropna().unique()),
        key="temporal_gravedades"
    )

    clases = st.multiselect(
        "Clase de accidente",
        options=sorted(df["CLASE_ACC"].dropna().unique()),
        default=sorted(df["CLASE_ACC"].dropna().unique()),
        key="temporal_clases"
    )

    meses = st.multiselect(
        "Mes",
        options=sorted(df["MES"].dropna().unique()),
        default=sorted(df["MES"].dropna().unique()),
        key="temporal_meses"
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
# INDICADORES TEMPORALES
# =========================
st.subheader("Indicadores temporales")

hora_pico = int(df_filtrado["HORA"].value_counts().idxmax())
mes_pico_num = int(df_filtrado["MES"].value_counts().idxmax())
anio_pico = int(df_filtrado["ANIO"].value_counts().idxmax())

meses_nombre = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

col1, col2, col3 = st.columns(3)

col1.metric("Hora con más accidentes", f"{hora_pico}:00")
col2.metric("Mes con más accidentes", meses_nombre.get(mes_pico_num, mes_pico_num))
col3.metric("Año con más accidentes", anio_pico)

st.divider()

# =========================
# GRÁFICOS PRINCIPALES
# =========================
st.subheader("Evolución y distribución temporal")

tab1, tab2, tab3 = st.tabs([
    "Evolución anual",
    "Meses y horas",
    "Mapa de calor temporal"
])

# Streamlit permite organizar contenido relacionado en pestañas con st.tabs.
# Esto ayuda a no saturar visualmente la página.

with tab1:
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

    if len(acc_anio) > 1:
        primer_anio = acc_anio.iloc[0]
        ultimo_anio = acc_anio.iloc[-1]

        variacion = (
            (ultimo_anio["Accidentes"] - primer_anio["Accidentes"])
            / primer_anio["Accidentes"]
        ) * 100

        st.info(
            f"Entre {int(primer_anio['ANIO'])} y {int(ultimo_anio['ANIO'])}, "
            f"la variación acumulada de accidentes fue de {variacion:.2f}%."
        )

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        acc_mes = (
            df_filtrado
            .groupby("MES")
            .size()
            .reset_index(name="Accidentes")
            .sort_values("MES")
        )

        acc_mes["MES_NOMBRE"] = acc_mes["MES"].map(meses_nombre)

        fig_mes = px.bar(
            acc_mes,
            x="MES_NOMBRE",
            y="Accidentes",
            title="Accidentes por mes"
        )

        fig_mes.update_layout(
            xaxis_title="Mes",
            yaxis_title="Número de accidentes"
        )

        st.plotly_chart(fig_mes, use_container_width=True)

    with col_b:
        acc_hora = (
            df_filtrado
            .groupby("HORA")
            .size()
            .reset_index(name="Accidentes")
            .sort_values("HORA")
        )

        fig_hora = px.bar(
            acc_hora,
            x="HORA",
            y="Accidentes",
            title="Accidentes por hora del día"
        )

        fig_hora.update_layout(
            xaxis_title="Hora del día",
            yaxis_title="Número de accidentes",
            xaxis=dict(dtick=1)
        )

        st.plotly_chart(fig_hora, use_container_width=True)

    st.markdown(f"""
    **Lectura temporal:** con los filtros actuales, la mayor concentración horaria se presenta a las **{hora_pico}:00** 
    y el mes con mayor número de accidentes es **{meses_nombre.get(mes_pico_num, mes_pico_num)}**.
    """)

with tab3:
    dias_nombre = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }

    heatmap_data = (
        df_filtrado
        .dropna(subset=["DIA_SEMANA_NUM", "HORA"])
        .groupby(["DIA_SEMANA_NUM", "HORA"])
        .size()
        .reset_index(name="Accidentes")
    )

    if heatmap_data.empty:
        st.warning("No hay datos suficientes para construir el mapa de calor con los filtros seleccionados.")
    else:
        heatmap_pivot = heatmap_data.pivot_table(
            index="DIA_SEMANA_NUM",
            columns="HORA",
            values="Accidentes",
            aggfunc="sum",
            fill_value=0
        )

        heatmap_pivot = heatmap_pivot.reindex(index=range(0, 7), columns=range(0, 24), fill_value=0)
        heatmap_pivot.index = [dias_nombre[dia] for dia in heatmap_pivot.index]

        fig_heatmap = px.imshow(
            heatmap_pivot,
            aspect="auto",
            title="Mapa de calor: accidentes por día de la semana y hora",
            labels=dict(x="Hora del día", y="Día de la semana", color="Accidentes"),
            text_auto=True
        )

        fig_heatmap.update_layout(
            xaxis=dict(dtick=1),
            yaxis_title="Día de la semana",
            xaxis_title="Hora del día"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.caption(
            "El mapa de calor permite identificar franjas críticas combinando día de la semana y hora del accidente."
        )

st.divider()

# =========================
# GRAVEDAD EN EL TIEMPO
# =========================
st.subheader("Evolución temporal por gravedad")

acc_gravedad_anio = (
    df_filtrado
    .groupby(["ANIO", "GRAVEDAD"])
    .size()
    .reset_index(name="Accidentes")
    .sort_values("ANIO")
)

fig_grav_anio = px.line(
    acc_gravedad_anio,
    x="ANIO",
    y="Accidentes",
    color="GRAVEDAD",
    color_discrete_map=COLOR_GRAVEDAD,
    markers=True,
    title="Evolución anual por gravedad"
)

fig_grav_anio.update_layout(
    xaxis_title="Año",
    yaxis_title="Número de accidentes",
    hovermode="x unified"
)

st.plotly_chart(fig_grav_anio, use_container_width=True)

