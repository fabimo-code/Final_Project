from pathlib import Path

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError:  # Permite probar funciones fuera de Streamlit.
    class _DummySidebar:
        def header(self, *args, **kwargs):
            return None

    class _DummyStreamlit:
        sidebar = _DummySidebar()

        @staticmethod
        def cache_data(*args, **kwargs):
            def decorator(func):
                return func
            return decorator

    st = _DummyStreamlit()

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "historico_siniestros_bogota_d.c_-.csv"

MESES = {
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

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}


def _normalizar_texto(serie: pd.Series) -> pd.Series:
    return (
        serie.astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )


@st.cache_data(show_spinner="Cargando y preparando datos...")
def cargar_datos(ruta_csv: str | Path = DATA_PATH) -> pd.DataFrame:
    """Carga y prepara el dataset de siniestros viales de Bogotá."""
    ruta_csv = Path(ruta_csv)
    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo CSV en: {ruta_csv}. "
            "Verifica que el dataset esté dentro de la carpeta data/."
        )

    df = pd.read_csv(ruta_csv)

    # Eliminación de duplicados exactos para evitar doble conteo.
    df = df.drop_duplicates().copy()

    # Conversión temporal.
    df["FECHA_HORA_ACC"] = pd.to_datetime(
        df["FECHA_HORA_ACC"], errors="coerce", utc=True
    )
    df["FECHA_HORA_ACC"] = df["FECHA_HORA_ACC"].dt.tz_convert(None)

    # Conversión numérica para coordenadas.
    for col in ["LATITUD", "LONGITUD", "X", "Y"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Estandarización de variables categóricas.
    for col in ["LOCALIDAD", "GRAVEDAD", "CLASE_ACC"]:
        if col in df.columns:
            df[col] = _normalizar_texto(df[col])

    # Variables derivadas temporales.
    df["ANIO"] = df["FECHA_HORA_ACC"].dt.year
    df["MES"] = df["FECHA_HORA_ACC"].dt.month
    df["MES_NOMBRE"] = df["MES"].map(MESES)
    df["HORA"] = df["FECHA_HORA_ACC"].dt.hour
    df["DIA_SEMANA_NUM"] = df["FECHA_HORA_ACC"].dt.dayofweek
    df["DIA_SEMANA"] = df["DIA_SEMANA_NUM"].map(DIAS_SEMANA)

    # Variable binaria de severidad.
    df["RIESGO_ALTO"] = df["GRAVEDAD"].isin(["CON HERIDOS", "CON MUERTOS"]).astype(int)

    # Registros sin fecha no sirven para el análisis temporal ni filtros globales.
    df = df.dropna(subset=["FECHA_HORA_ACC", "ANIO", "MES", "HORA"]).copy()

    # Tipos enteros cuando ya no hay nulos en estas variables.
    df["ANIO"] = df["ANIO"].astype(int)
    df["MES"] = df["MES"].astype(int)
    df["HORA"] = df["HORA"].astype(int)

    return df


def aplicar_filtros(
    df: pd.DataFrame,
    rango_anios: tuple[int, int] | None = None,
    localidades: list[str] | None = None,
    gravedades: list[str] | None = None,
    clases_accidente: list[str] | None = None,
) -> pd.DataFrame:
    """Filtra el dataframe según los controles seleccionados por el usuario."""
    df_filtrado = df.copy()

    if rango_anios is not None:
        anio_min, anio_max = rango_anios
        df_filtrado = df_filtrado[
            (df_filtrado["ANIO"] >= anio_min) & (df_filtrado["ANIO"] <= anio_max)
        ]

    if localidades:
        df_filtrado = df_filtrado[df_filtrado["LOCALIDAD"].isin(localidades)]

    if gravedades:
        df_filtrado = df_filtrado[df_filtrado["GRAVEDAD"].isin(gravedades)]

    if clases_accidente:
        df_filtrado = df_filtrado[df_filtrado["CLASE_ACC"].isin(clases_accidente)]

    return df_filtrado


def crear_sidebar_filtros(df: pd.DataFrame) -> pd.DataFrame:
    """Crea filtros globales en la barra lateral y devuelve el dataframe filtrado."""
    st.sidebar.header("Filtros de análisis")

    anio_min = int(df["ANIO"].min())
    anio_max = int(df["ANIO"].max())

    rango_anios = st.sidebar.slider(
        "Rango de años",
        min_value=anio_min,
        max_value=anio_max,
        value=(anio_min, anio_max),
        step=1,
    )

    localidades = st.sidebar.multiselect(
        "Localidad",
        options=sorted(df["LOCALIDAD"].dropna().unique()),
        default=sorted(df["LOCALIDAD"].dropna().unique()),
    )

    gravedades = st.sidebar.multiselect(
        "Gravedad",
        options=sorted(df["GRAVEDAD"].dropna().unique()),
        default=sorted(df["GRAVEDAD"].dropna().unique()),
    )

    clases_accidente = st.sidebar.multiselect(
        "Clase de accidente",
        options=sorted(df["CLASE_ACC"].dropna().unique()),
        default=sorted(df["CLASE_ACC"].dropna().unique()),
    )

    return aplicar_filtros(
        df,
        rango_anios=rango_anios,
        localidades=localidades,
        gravedades=gravedades,
        clases_accidente=clases_accidente,
    )


def datos_para_mapa(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve registros con coordenadas válidas para visualizaciones geográficas."""
    return df.dropna(subset=["LATITUD", "LONGITUD"]).copy()
