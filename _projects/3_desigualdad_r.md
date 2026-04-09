---
layout: page
title: Desigualdad de Ingresos en Chile
description: Analisis estadistico en R de desigualdad economica y de tiempo en Chile, usando datos de CASEN y ENUT.
img: assets/img/projects/p3_desigualdad.png
importance: 4
category: work
related_publications: false
---

Analisis cuantitativo de desigualdad economica en Chile usando **R + tidyverse + ineq**, con un equivalente Python para validacion cruzada.

**Pregunta**: la desigualdad de tiempo (trabajo, cuidados, ocio) sigue el mismo patron que la desigualdad de ingresos? Hay grupos doblemente vulnerables?

**Indices calculados**: Gini, Theil, Atkinson (eps=0.5 y 1.0), ratio P90/P10.

**Resultados clave**:
- Gini de ingresos: 0.45 (consistente con la realidad chilena, OCDE-1 en desigualdad)
- Ratio P90/P10: 9.04 (el 10% mas rico recibe 9 veces lo del 10% mas pobre)
- **Brecha de genero robusta**: las mujeres reportan +12 horas semanales en cuidados no remunerados que los hombres del mismo quintil, en *todos* los quintiles

[Codigo R y Python en GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/03_desigualdad_r)
