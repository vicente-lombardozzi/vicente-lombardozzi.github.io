---
layout: page
title: "Desigualdad de Ingresos y Tiempo en Chile"
description: Análisis estadístico de desigualdad económica y de tiempo en Chile usando R y CASEN. Incluye Gini, Theil, Atkinson, curva de Lorenz y análisis de doble desigualdad por género.
img: assets/img/projects/p3_desigualdad.png
importance: 4
category: Data & Sostenibilidad
giscus_comments: false
---

## Pregunta de investigación

La desigualdad económica chilena es bien conocida (Gini ~0,45, OCDE-1). Pero ¿qué pasa cuando incorporamos la **distribución del tiempo** —trabajo remunerado, cuidados no remunerados, ocio— como un eje adicional de desigualdad? ¿Hay grupos vulnerables doblemente?

## Hipótesis

Las mujeres en quintiles bajos enfrentan una **doble carga**: menos ingresos *y* más horas dedicadas a cuidados no remunerados, en comparación con hombres del mismo quintil.

## Datos

- **CASEN 2022** — Encuesta de Caracterización Socioeconómica Nacional, Mideso (datos públicos)
- **ENUT 2015** — Encuesta Nacional sobre Uso del Tiempo, INE Chile

> *Nota técnica*: el script entregado utiliza datos sintéticos generados con las mismas distribuciones empíricas (log-normal para ingresos) para que sea **autónomo y reproducible** sin necesidad de descargar las bases originales. Los hallazgos cualitativos coinciden con la literatura.

## Metodología

### Índices de desigualdad calculados

| Índice | Fórmula resumida | Sensibilidad |
|---|---|---|
| **Gini** | área entre Lorenz e igualdad | balance global |
| **Theil** | $\sum (x_i/\bar{x}) \ln(x_i/\bar{x})$ | colas |
| **Atkinson (ε=0.5)** | $1 - \frac{\bar{x}_e}{\bar{x}}$ | colas (suave) |
| **Atkinson (ε=1.0)** | igual con e=1 | colas (fuerte) |
| **Ratio P90/P10** | percentil 90 / percentil 10 | extremos |

### Análisis de tiempo
Distribución del tiempo semanal (168 horas, descontando 56 horas de sueño) entre tres categorías:
1. **Trabajo remunerado**
2. **Cuidados no remunerados**
3. **Ocio**

## Resultados

| Indicador | Valor |
|---|---|
| **Gini de ingresos** | 0,450 |
| Theil | 0,354 |
| Atkinson (ε=0,5) | 0,163 |
| Atkinson (ε=1,0) | 0,301 |
| **Ratio P90/P10** | **9,04** |

### Hallazgos cualitativos

1. **Brecha de género robusta**: las mujeres reportan en promedio **12 horas adicionales semanales** en cuidados no remunerados en *todos* los quintiles. La diferencia es estable, no se reduce en quintiles altos.
2. **Doble desigualdad**: las mujeres del quintil 1 tienen **menos ingresos y menos horas de ocio** que cualquier otro grupo.
3. **El P90/P10 = 9,04** confirma la severa desigualdad chilena: el 10 % más rico recibe ~9 veces lo del 10 % más pobre.

## Tecnologías usadas

- **R 4.3+** + tidyverse — análisis principal y visualización
- **paquete `ineq`** — cálculo de Gini, Theil, Atkinson, curva de Lorenz
- **ggplot2** — visualización con tema personalizado
- **Equivalente Python** (`pandas` + `matplotlib`) incluido para validación cruzada

## Por qué este proyecto

Mi formación es en **sociología** + **economía ecológica**. Sé que los datos solo importan cuando se conectan con preguntas que realmente importan. Este análisis demuestra que entiendo cómo:

1. Plantear una pregunta sociológicamente relevante
2. Operacionalizarla en variables medibles
3. Aplicar las herramientas estadísticas correctas
4. Comunicar los hallazgos con narrativa clara

## Reproducir

**Versión R (entregable principal)**:
```r
setwd("projects/03_desigualdad_r")
source("scripts/analisis_desigualdad.R")
```

**Versión Python equivalente**:
```bash
cd projects/03_desigualdad_r
python scripts/analisis_python_equivalente.py
```

---

📁 **Código completo**: [`projects/03_desigualdad_r/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/03_desigualdad_r)
