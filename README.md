# Plataforma Visual Interactiva para el Monitoreo y Análisis de Siniestralidad Vial en Bogotá

Dashboard desarrollado en Streamlit para analizar siniestros viales históricos en Bogotá.

## Estructura

```text
proyecto_siniestros_streamlit/
├── app.py
├── requirements.txt
├── data/
│   └── historico_siniestros_bogota_d.c_-.csv
├── src/
│   ├── data_prep.py
│   ├── kpis.py
│   └── visuals.py
└── pages/
    ├── 1_Vista_Ejecutiva.py
    ├── 2_Analisis_Temporal.py
    ├── 3_Analisis_Geografico.py
    ├── 4_Gravedad_y_Riesgo.py
    ├── 5_Modelos_Analiticos.py
    └── 6_Conclusiones.py
```

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Propósito

Transformar datos históricos de siniestros viales en información visual, interactiva y accionable para apoyar decisiones de movilidad y seguridad vial en Bogotá.
