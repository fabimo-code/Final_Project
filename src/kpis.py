import pandas as pd


def calcular_kpis(df: pd.DataFrame) -> dict:
    """Calcula indicadores ejecutivos para el dashboard."""
    total_accidentes = len(df)

    if total_accidentes == 0:
        return {
            "total_accidentes": 0,
            "accidentes_heridos": 0,
            "accidentes_muertos": 0,
            "porcentaje_riesgo_alto": 0.0,
            "localidad_critica": "Sin datos",
            "hora_pico": "Sin datos",
            "mes_critico": "Sin datos",
        }

    gravedad = df["GRAVEDAD"].value_counts()
    accidentes_heridos = int(gravedad.get("CON HERIDOS", 0))
    accidentes_muertos = int(gravedad.get("CON MUERTOS", 0))
    porcentaje_riesgo_alto = ((accidentes_heridos + accidentes_muertos) / total_accidentes) * 100

    localidad_critica = (
        df["LOCALIDAD"].value_counts().idxmax()
        if "LOCALIDAD" in df.columns and not df["LOCALIDAD"].dropna().empty
        else "Sin datos"
    )

    hora_pico = (
        int(df["HORA"].value_counts().idxmax())
        if "HORA" in df.columns and not df["HORA"].dropna().empty
        else "Sin datos"
    )

    mes_critico = (
        df["MES_NOMBRE"].value_counts().idxmax()
        if "MES_NOMBRE" in df.columns and not df["MES_NOMBRE"].dropna().empty
        else "Sin datos"
    )

    return {
        "total_accidentes": int(total_accidentes),
        "accidentes_heridos": accidentes_heridos,
        "accidentes_muertos": accidentes_muertos,
        "porcentaje_riesgo_alto": round(porcentaje_riesgo_alto, 2),
        "localidad_critica": localidad_critica,
        "hora_pico": hora_pico,
        "mes_critico": mes_critico,
    }
