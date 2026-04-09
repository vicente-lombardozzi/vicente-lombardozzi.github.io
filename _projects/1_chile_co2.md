---
layout: page
title: "Emisiones de CO₂ en Chile (1990–2050)"
description: Re-análisis en Python de mi tesina del MSc Leeds (2019). Descomposición KAYA, modelo STIRPAT, proyecciones BAU y sostenible al 2050.
img: assets/img/projects/p1_chile_co2.png
importance: 1
category: data-sostenibilidad
giscus_comments: false
---

## Contexto del proyecto

Durante mi máster en **Economía Ecológica en la University of Leeds (2019)** desarrollé un análisis cuantitativo de las emisiones de CO₂ de Chile como parte del curso *Tools and Techniques in Ecological Economics*. El trabajo combinaba descomposición **KAYA**, regresión **STIRPAT** y proyecciones a 2050. Recibí observaciones específicas del profesor sobre limitaciones metodológicas y aplicación de los modelos.

**En 2026 retomé el proyecto** y lo reimplementé desde cero en Python, corrigiendo las observaciones originales, actualizando datos y generando un análisis 100% reproducible.

## Pregunta de investigación

¿Chile ha desacoplado su crecimiento económico de las emisiones de CO₂? ¿Cuál es la trayectoria realista para alcanzar las metas de la NDC chilena?

## Metodología

### 1. Descomposición KAYA
La identidad KAYA expresa las emisiones de CO₂ como producto de cuatro factores:

$$
CO_2 = \text{Población} \times \frac{\text{PIB}}{\text{Población}} \times \frac{\text{Energía}}{\text{PIB}} \times \frac{CO_2}{\text{Energía}}
$$

Permite identificar **qué está empujando** las emisiones (crecimiento poblacional, riqueza o intensidad energética) y **qué está conteniéndolas** (eficiencia, descarbonización).

### 2. Modelo STIRPAT
Regresión log-log multivariable sobre 90 países (año 2002):

$$
\ln(CO_2) = \beta_0 + \beta_1 \ln(PIB) + \beta_2 \ln(\text{Energía}) + \varepsilon
$$

Implementación con `statsmodels.OLS`.

### 3. Proyecciones a 2050
Dos escenarios:
- **Business-as-Usual (BAU)**: extensión lineal de las tasas históricas
- **Transición sostenible**: aceleración de eficiencia energética y descarbonización

## Resultados clave

| Indicador | 1990 | 2013 | Cambio |
|---|---|---|---|
| Población | 13,1 M | 17,6 M | +34 % |
| CO₂ territorial | 33,3 MtCO₂ | 83,2 MtCO₂ | **+150 %** |
| PIB per cápita PPP | USD 9.245 | USD 21.749 | +135 % |
| Intensidad energética | — | — | −12,4 % |
| Huella de carbono energética | — | — | −9,7 % |

**Modelo STIRPAT (R² = 0.91)**: la elasticidad del CO₂ respecto al PIB PPP es **0,74** y respecto a la energía total es **0,35**, ambos coeficientes altamente significativos (p < 0,001).

**Proyecciones 2030**:
- BAU: 163,6 MtCO₂
- Sostenible: 68,9 MtCO₂
- Meta NDC Chile: 50,1 MtCO₂

## Tecnologías usadas

- **Python 3.13** + Jupyter
- **pandas, numpy** — manipulación de datos
- **scipy.io** — lectura de los datasets originales en formato Matlab `.mat`
- **statsmodels** — regresión OLS para STIRPAT
- **matplotlib** — visualizaciones
- Datasets reales: Global Carbon Budget, World Bank, IEA, ONU

## Reproducir el análisis

```bash
cd projects/01_chile_co2_python
pip install -r requirements.txt
python src/analysis_chile_co2.py
```

El script genera 5 figuras en `figures/`, escribe los datos limpios en `data/` y produce las tablas de resultados de la regresión STIRPAT y los coeficientes de Gini.

## Lo que aprendí pasando de Matlab a Python

El trabajo original (2019) usaba Matlab, software cerrado y de licencia paga. La versión 2026 es **100% open source y reproducible**: cualquier persona puede clonar el repositorio, instalar las dependencias y obtener los mismos resultados. Esa portabilidad es uno de los argumentos centrales por los que el ecosistema científico ha migrado masivamente a Python en los últimos años.

---

📁 **Código completo**: [`projects/01_chile_co2_python/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/01_chile_co2_python)
