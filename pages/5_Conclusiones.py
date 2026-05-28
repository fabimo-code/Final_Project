import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_prep import cargar_datos, aplicar_filtros
from src.visuals import COLOR_GRAVEDAD


st.set_page_config(
    page_title="Conclusiones",
    page_icon="✅",
    layout="wide"
)

# =========================
# CARGA DE DATOS
# =========================
df = cargar_datos()

st.title("✅ Conclusiones y Hallazgos Estratégicos")

st.markdown("""
Esta vista sintetiza los principales hallazgos del dashboard y traduce los resultados en recomendaciones 
orientadas a la toma de decisiones en movilidad y seguridad vial.
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
        key="conclusiones_rango_anios"
    )

    localidades = st.multiselect(
        "Localidad",
        options=sorted(df["LOCALIDAD"].dropna().unique()),
        default=sorted(df["LOCALIDAD"].dropna().unique()),
        key="conclusiones_localidades"
    )

    gravedades = st.multiselect(
        "Gravedad",
        options=sorted(df["GRAVEDAD"].dropna().unique()),
        default=sorted(df["GRAVEDAD"].dropna().unique()),
        key="conclusiones_gravedades"
    )

    clases = st.multiselect(
        "Clase de accidente",
        options=sorted(df["CLASE_ACC"].dropna().unique()),
        default=sorted(df["CLASE_ACC"].dropna().unique()),
        key="conclusiones_clases"
    )

    meses = st.multiselect(
        "Mes",
        options=sorted(df["MES"].dropna().unique()),
        default=sorted(df["MES"].dropna().unique()),
        key="conclusiones_meses"
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
# DICCIONARIOS
# =========================
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

# =========================
# CÁLCULOS GENERALES
# =========================
total_accidentes = len(df_filtrado)

acc_heridos = int((df_filtrado["GRAVEDAD"] == "CON HERIDOS").sum())
acc_muertos = int((df_filtrado["GRAVEDAD"] == "CON MUERTOS").sum())
acc_riesgo_alto = int(df_filtrado["RIESGO_ALTO"].sum())
porc_riesgo_alto = (acc_riesgo_alto / total_accidentes) * 100 if total_accidentes > 0 else 0

localidad_critica = df_filtrado["LOCALIDAD"].value_counts().idxmax()
acc_localidad_critica = int(df_filtrado["LOCALIDAD"].value_counts().max())

hora_pico = int(df_filtrado["HORA"].value_counts().idxmax())
mes_pico_num = int(df_filtrado["MES"].value_counts().idxmax())
mes_pico = meses_nombre.get(mes_pico_num, mes_pico_num)

clase_critica = df_filtrado["CLASE_ACC"].value_counts().idxmax()
acc_clase_critica = int(df_filtrado["CLASE_ACC"].value_counts().max())

# =========================
# KPIS DE CIERRE
# =========================
st.subheader("Resumen ejecutivo del periodo analizado")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total accidentes", f"{total_accidentes:,}".replace(",", "."))
col2.metric("Riesgo alto", f"{porc_riesgo_alto:.2f}%")
col3.metric("Localidad crítica", localidad_critica)
col4.metric("Hora pico", f"{hora_pico}:00")

col5, col6, col7 = st.columns(3)

col5.metric("Mes crítico", mes_pico)
col6.metric("Clase más frecuente", clase_critica)
col7.metric("Accidentes con muertos", f"{acc_muertos:,}".replace(",", "."))

st.divider()

# =========================
# CONCLUSIÓN GENERAL
# =========================
st.subheader("Conclusión general")

st.success(f"""
El análisis de los datos filtrados evidencia que la siniestralidad vial en Bogotá presenta patrones claros de concentración 
territorial, temporal y de severidad. En el periodo seleccionado se registran **{total_accidentes:,} siniestros**, 
de los cuales **{acc_riesgo_alto:,}** corresponden a eventos de riesgo alto, es decir, accidentes con heridos o muertos. 
La localidad con mayor concentración es **{localidad_critica}**, la hora de mayor ocurrencia es **{hora_pico}:00** 
y la clase de accidente más frecuente es **{clase_critica}**.
""".replace(",", "."))

# =========================
# HALLAZGOS PRINCIPALES
# =========================
st.subheader("Hallazgos principales")

hallazgo_1 = (
    f"La localidad **{localidad_critica}** concentra el mayor número de accidentes "
    f"con **{acc_localidad_critica:,} registros**, lo que la convierte en un punto prioritario "
    f"para monitoreo e intervención preventiva."
).replace(",", ".")

hallazgo_2 = (
    f"La mayor frecuencia horaria se presenta a las **{hora_pico}:00**, lo que sugiere la existencia "
    f"de franjas críticas asociadas a dinámicas de movilidad urbana."
)

hallazgo_3 = (
    f"El porcentaje de accidentes de riesgo alto es **{porc_riesgo_alto:.2f}%**, considerando como riesgo alto "
    f"los eventos con heridos o muertos."
)

hallazgo_4 = (
    f"La clase de accidente más frecuente es **{clase_critica}**, con **{acc_clase_critica:,} registros**, "
    f"lo que permite orientar estrategias específicas según el tipo de siniestro predominante."
).replace(",", ".")

col_a, col_b = st.columns(2)

with col_a:
    st.info(f"**Hallazgo territorial**  \n{hallazgo_1}")
    st.warning(f"**Hallazgo de severidad**  \n{hallazgo_3}")

with col_b:
    st.info(f"**Hallazgo temporal**  \n{hallazgo_2}")
    st.warning(f"**Hallazgo por tipo de accidente**  \n{hallazgo_4}")

st.divider()

# =========================
# VISUALIZACIONES DE SÍNTESIS
# =========================
st.subheader("Síntesis visual de hallazgos")

tab1, tab2, tab3 = st.tabs([
    "Prioridad territorial",
    "Severidad",
    "Temporalidad"
])

with tab1:
    top_localidades = (
        df_filtrado
        .groupby("LOCALIDAD")
        .size()
        .reset_index(name="Accidentes")
        .sort_values("Accidentes", ascending=False)
        .head(10)
        .sort_values("Accidentes", ascending=True)
    )

    fig_top_localidades = px.bar(
        top_localidades,
        x="Accidentes",
        y="LOCALIDAD",
        orientation="h",
        title="Top 10 localidades prioritarias por número de accidentes"
    )

    fig_top_localidades.update_layout(
        xaxis_title="Número de accidentes",
        yaxis_title="Localidad"
    )

    st.plotly_chart(fig_top_localidades, use_container_width=True)

with tab2:
    gravedad = (
        df_filtrado
        .groupby("GRAVEDAD")
        .size()
        .reset_index(name="Accidentes")
        .sort_values("Accidentes", ascending=False)
    )

    fig_gravedad = px.pie(
        gravedad,
        names="GRAVEDAD",
        values="Accidentes",
        color="GRAVEDAD",
        color_discrete_map=COLOR_GRAVEDAD,
        title="Participación por gravedad",
        hole=0.45
    )

    fig_gravedad.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(fig_gravedad, use_container_width=True)

with tab3:
    acc_hora = (
        df_filtrado
        .groupby("HORA")
        .size()
        .reset_index(name="Accidentes")
        .sort_values("HORA")
    )

    fig_hora = px.line(
        acc_hora,
        x="HORA",
        y="Accidentes",
        markers=True,
        title="Distribución de accidentes por hora"
    )

    fig_hora.update_layout(
        xaxis_title="Hora del día",
        yaxis_title="Número de accidentes",
        xaxis=dict(dtick=1),
        hovermode="x unified"
    )

    st.plotly_chart(fig_hora, use_container_width=True)

st.divider()

# =========================
# RECOMENDACIONES
# =========================
st.subheader("Recomendaciones para la toma de decisiones")

recomendaciones = pd.DataFrame({
    "Línea de acción": [
        "Priorización territorial",
        "Gestión por franjas horarias",
        "Seguimiento a riesgo alto",
        "Análisis por clase de accidente",
        "Monitoreo continuo"
    ],
    "Recomendación": [
        f"Concentrar análisis preventivo en {localidad_critica} y en las localidades del top de accidentalidad.",
        f"Reforzar seguimiento operativo en la franja cercana a las {hora_pico}:00, donde se observa mayor frecuencia.",
        "Diferenciar los accidentes con heridos o muertos para orientar medidas de seguridad vial más focalizadas.",
        f"Analizar con mayor detalle los eventos tipo {clase_critica}, por ser la clase más frecuente en los datos filtrados.",
        "Usar el dashboard como herramienta de monitoreo periódico para comparar cambios por año, mes, localidad y gravedad."
    ]
})

st.dataframe(
    recomendaciones,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# PREGUNTAS RESPONDIDAS
# =========================
st.subheader("Preguntas de análisis respondidas")

preguntas = pd.DataFrame({
    "Pregunta de análisis": [
        "¿Cuáles son las localidades con mayor concentración de accidentes?",
        "¿Qué horarios presentan mayor frecuencia de siniestralidad?",
        "¿Cómo ha evolucionado la accidentalidad a través del tiempo?",
        "¿Qué tipos de accidentes presentan mayor gravedad?",
        "¿Qué zonas requieren priorización de intervención preventiva?"
    ],
    "Respuesta desde el dashboard": [
        "Se responde mediante rankings territoriales, mapas y tabla de priorización por localidad.",
        "Se responde mediante gráficos por hora, mapa de calor temporal y KPIs de hora pico.",
        "Se responde mediante series anuales y análisis mensual.",
        "Se responde mediante distribución por gravedad y análisis de riesgo alto.",
        "Se responde combinando concentración territorial, riesgo alto y severidad por localidad."
    ],
    "Vista relacionada": [
        "Análisis Geográfico",
        "Análisis Temporal",
        "Análisis Temporal",
        "Gravedad y Riesgo",
        "Análisis Geográfico / Gravedad y Riesgo"
    ]
})

st.dataframe(
    preguntas,
    use_container_width=True,
    hide_index=True
)

# =========================
# CIERRE EJECUTIVO
# =========================
st.divider()

st.subheader("Cierre ejecutivo")

st.markdown("""
El dashboard permite transformar datos históricos de siniestros viales en información clara, visual e interactiva. 
Su principal aporte es facilitar la identificación de patrones críticos de accidentalidad, apoyar la priorización de zonas 
y horarios de intervención, y fortalecer la toma de decisiones basada en evidencia para la gestión de movilidad y seguridad vial en Bogotá.
""")

# =========================
# NOTA TÉCNICA
# =========================
with st.expander("Ver nota técnica de conclusiones"):
    st.markdown("""
    Las conclusiones se calculan dinámicamente a partir de los filtros seleccionados por el usuario.

    La clasificación de riesgo alto considera los accidentes cuya gravedad corresponde a:

    - `CON HERIDOS`
    - `CON MUERTOS`

    Las recomendaciones no representan decisiones institucionales definitivas, sino orientaciones analíticas derivadas 
    de los patrones observados en los datos históricos.
    """)