# Proyecto 3 — Desigualdad de Ingresos y Tiempo en Chile

Análisis estadístico de desigualdad económica en Chile usando **R + tidyverse + ineq**, con un equivalente Python para validación cruzada.

## Pregunta

¿La desigualdad de tiempo (trabajo, cuidados, ocio) sigue el mismo patrón que la desigualdad de ingresos? ¿Hay grupos doblemente vulnerables?

## Estructura

```
03_desigualdad_r/
├── README.md
├── scripts/
│   ├── analisis_desigualdad.R          (entregable principal — R)
│   └── analisis_python_equivalente.py  (validación en Python)
├── data/                                 (datos sintéticos basados en CASEN)
└── output/
    ├── 00_thumbnail.png
    ├── 01_lorenz_curve.png
    ├── 02_tiempo_por_quintil.png
    ├── 03_brecha_genero.png
    └── indices_desigualdad.csv
```

## Reproducir

**R (recomendado)**:
```r
setwd("projects/03_desigualdad_r")
source("scripts/analisis_desigualdad.R")
```

**Python**:
```bash
pip install pandas numpy matplotlib
python scripts/analisis_python_equivalente.py
```

## Resultados

| Índice | Valor |
|---|---|
| **Gini de ingresos** | 0,450 |
| Theil | 0,354 |
| Atkinson (ε=0,5) | 0,163 |
| Atkinson (ε=1,0) | 0,301 |
| **Ratio P90/P10** | **9,04** |

**Hallazgo principal**: las mujeres reportan **+12 horas semanales en cuidados no remunerados** que los hombres del mismo quintil, en *todos* los quintiles.

Ver tarjeta del proyecto: [/projects/3_desigualdad_r/](https://vicente-lombardozzi.github.io/projects/3_desigualdad_r/)
