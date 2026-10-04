# Proyecto 1 — Descomposición del crecimiento y regresiones log-log (Chile, 1990–2050)

Re-análisis en Python de un trabajo evaluado del módulo cuantitativo del MSc (*Tools and Techniques*, University of Leeds, 2019), hecho originalmente en MATLAB. Combina **descomposición de Kaya**, **regresiones log-log entre 90 países (2002)** y **proyecciones de escenarios** al 2050.

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
- **Regresión log-log entre países**: coeficientes interpretados como elasticidades (ver `stirpat_coefficients.csv`)
- **Proyecciones de escenarios** a 2050 con tasas de crecimiento constantes sobre logaritmos

Ver tarjeta del proyecto en el portafolio: [/projects/1_chile_co2/](https://vicente-lombardozzi.github.io/projects/1_chile_co2/)
