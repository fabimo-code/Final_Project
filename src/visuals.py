import pandas as pd
import plotly.express as px

COLOR_GRAVEDAD = {
    "SOLO DANOS": "#6B7280",
    "CON HERIDOS": "#F59E0B",
    "CON MUERTOS": "#DC2626",
}

COLOR_PRINCIPAL = "#1E3A8A"


def grafico_evolucion_anual(df: pd.DataFrame):
    data = df.groupby("ANIO", as_index=False).size().rename(columns={"size": "Accidentes"})
    fig = px.line(
        data,
        x="ANIO",
        y="Accidentes",
        markers=True,
        title="Evolución anual de accidentes",
    )
    fig.update_traces(line_color=COLOR_PRINCIPAL)
    fig.update_layout(xaxis_title="Año", yaxis_title="Número de accidentes")
    return fig


def grafico_top_localidades(df: pd.DataFrame, n: int = 10):
    data = (
        df["LOCALIDAD"]
        .value_counts()
        .head(n)
        .sort_values()
        .reset_index()
    )
    data.columns = ["LOCALIDAD", "Accidentes"]
    fig = px.bar(
        data,
        x="Accidentes",
        y="LOCALIDAD",
        orientation="h",
        title=f"Top {n} localidades con más accidentes",
    )
    fig.update_traces(marker_color=COLOR_PRINCIPAL)
    fig.update_layout(xaxis_title="Número de accidentes", yaxis_title="Localidad")
    return fig


def grafico_distribucion_gravedad(df: pd.DataFrame):
    data = df["GRAVEDAD"].value_counts().reset_index()
    data.columns = ["GRAVEDAD", "Accidentes"]
    fig = px.bar(
        data,
        x="GRAVEDAD",
        y="Accidentes",
        color="GRAVEDAD",
        color_discrete_map=COLOR_GRAVEDAD,
        title="Distribución de accidentes por gravedad",
    )
    fig.update_layout(xaxis_title="Gravedad", yaxis_title="Número de accidentes", showlegend=False)
    return fig


def grafico_accidentes_por_hora(df: pd.DataFrame):
    data = df.groupby("HORA", as_index=False).size().rename(columns={"size": "Accidentes"})
    fig = px.bar(
        data,
        x="HORA",
        y="Accidentes",
        title="Accidentes por hora del día",
    )
    fig.update_traces(marker_color=COLOR_PRINCIPAL)
    fig.update_layout(xaxis_title="Hora", yaxis_title="Número de accidentes")
    return fig


def grafico_accidentes_por_mes(df: pd.DataFrame):
    orden_meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    data = df.groupby(["MES", "MES_NOMBRE"], as_index=False).size().rename(columns={"size": "Accidentes"})
    data = data.sort_values("MES")
    fig = px.bar(
        data,
        x="MES_NOMBRE",
        y="Accidentes",
        category_orders={"MES_NOMBRE": orden_meses},
        title="Accidentes por mes",
    )
    fig.update_traces(marker_color=COLOR_PRINCIPAL)
    fig.update_layout(xaxis_title="Mes", yaxis_title="Número de accidentes")
    return fig
