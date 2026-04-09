# Proyecto 1 — Emisiones de CO₂ de Chile (1990–2050)

Re-análisis en Python de mi tesina del MSc en Economía Ecológica (University of Leeds, 2019). Combina **descomposición KAYA**, **regresión STIRPAT** y **proyecciones de escenarios** al 2050.

## Estructura

```
01_chile_co2_python/
├── README.md              (este archivo)
├── requirements.txt       (dependencias Python)
├── data/
│   ├── Chile.zip          (dataset original — 24 años, 1990-2013)
│   ├── CC02.zip           (90 países, año 2002)
│   ├── chile_1990_2013.csv
│   ├── chile_kaya_decomposition.csv
│   ├── stirpat_coefficients.csv
│   └── gini_coefficients.csv
├── figures/
│   ├── 00_thumbnail.png
│   ├── 01_kaya_decomposition.png
│   ├── 02_projections_2050.png
│   ├── 03_stirpat_scatter.png
│   └── 04_gini_global.png
├── notebooks/             (versión Jupyter — generada del .py)
└── src/
    └── analysis_chile_co2.py
```

## Reproducir

```bash
pip install -r requirements.txt
python src/analysis_chile_co2.py
```

## Resultados clave

- **Identidad KAYA verificada** (error matemático despreciable)
- **CO₂ creció 150 %** entre 1990 y 2013 (de 33,3 a 83,2 MtCO₂)
- **Modelo STIRPAT R² = 0.91**, elasticidad PIB = 0,74
- **Proyección BAU 2030**: 163,6 MtCO₂ (vs meta NDC = 50,1 MtCO₂)

Ver tarjeta del proyecto en el portafolio: [/projects/1_chile_co2/](https://vicente-lombardozzi.github.io/projects/1_chile_co2/)
