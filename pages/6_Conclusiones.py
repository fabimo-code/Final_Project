import streamlit as st

from src.data_prep import cargar_datos, crear_sidebar_filtros
from src.kpis import calcular_kpis

st.set_page_config(page_title="Conclusiones", page_icon="✅", layout="wide")

st.title("✅ Conclusiones")
st.markdown("Síntesis ejecutiva de hallazgos y recomendaciones basadas en los filtros seleccionados.")

df = cargar_datos()
df_filtrado = crear_sidebar_filtros(df)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

kpis = calcular_kpis(df_filtrado)

st.subheader("Hallazgos principales")
st.markdown(
    f"""
1. La localidad con mayor concentración de accidentes en el escenario filtrado es **{kpis['localidad_critica']}**.
2. La hora con mayor frecuencia de siniestros es **{kpis['hora_pico']}:00**.
3. El porcentaje de eventos de riesgo alto corresponde al **{kpis['porcentaje_riesgo_alto']}%**.
4. El mes con mayor accidentalidad es **{kpis['mes_critico']}**.
"""
)

st.subheader("Recomendaciones preliminares")
st.markdown(
    """
- Priorizar análisis e intervención en las localidades con mayor concentración de siniestros.
- Reforzar estrategias preventivas en las horas pico identificadas.
- Analizar de forma diferenciada los eventos con heridos y muertos.
- Usar la plataforma como herramienta de monitoreo y comunicación ejecutiva para apoyar decisiones de seguridad vial.
"""
)
