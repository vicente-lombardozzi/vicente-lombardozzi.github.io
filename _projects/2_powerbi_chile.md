---
layout: page
title: "Dashboard de Indicadores Socioeconómicos de Chile"
description: Dashboard interactivo con datos del Banco Mundial y CASEN. Construido en Plotly como alternativa open-source equivalente a Power BI, embebible en cualquier navegador.
img: assets/img/projects/p2_powerbi.png
importance: 3
category: data
giscus_comments: false
---

## Contexto

Los reclutadores chilenos para roles de Data Analyst suelen pedir explícitamente **Power BI** en sus ofertas. Sin embargo, Power BI Desktop es software propietario y los archivos `.pbix` no son embebibles directamente en GitHub Pages.

Este proyecto entrega **lo mejor de los dos mundos**:
- Un **dashboard interactivo en HTML** generado con **Plotly** (open source, embebible en cualquier navegador)
- El mismo dataset listo para abrir en Power BI Desktop (`chile_indicators_2000_2023.csv`)
- Una **guía DAX equivalente** para reproducir las mismas medidas en Power BI

## Pregunta de negocio

¿Cómo han evolucionado los indicadores macroeconómicos y sociales clave de Chile en los últimos 24 años? ¿Qué regiones presentan mayor vulnerabilidad?

## Datos utilizados

Todos los datos son **públicos y verificables**:

| Variable | Fuente | Cobertura |
|---|---|---|
| PIB y PIB per cápita | World Bank Open Data | 2000–2023 |
| Población | UN World Population Prospects | 2000–2023 |
| Esperanza de vida | World Bank | 2000–2023 |
| Desempleo | INE Chile / World Bank | 2000–2023 |
| Pobreza por ingresos | CASEN, Mideso | 2000–2022 |
| Pobreza regional | CASEN 2022 | 16 regiones |
| Coeficiente de Gini regional | CASEN 2022 | 16 regiones |
| CO₂ per cápita | Our World in Data | 2000–2023 |

## Visualizaciones del dashboard

El dashboard cuenta con **6 paneles interactivos**:

1. Evolución histórica del PIB
2. Evolución del PIB per cápita
3. Esperanza de vida (incluye caída por COVID-19 en 2020-2021)
4. Tasa de desempleo
5. Pobreza por región (CASEN 2022)
6. Coeficiente de Gini por región

## Tecnologías usadas

- **Python 3.13** + pandas + numpy
- **Plotly** — visualización interactiva
- **matplotlib** — preview estático para el portafolio

## Equivalencia DAX para Power BI

Si se quiere reproducir el mismo dashboard en Power BI, las medidas DAX equivalentes son:

```dax
-- PIB acumulado
PIB Acumulado =
CALCULATE(
    SUM('Chile'[gdp_billion_usd]),
    FILTER(ALL('Chile'), 'Chile'[year] <= MAX('Chile'[year]))
)

-- Tasa de variación anual
Variacion Anual PIB =
VAR PIBActual = SUM('Chile'[gdp_billion_usd])
VAR PIBAnterior = CALCULATE(SUM('Chile'[gdp_billion_usd]),
                            DATEADD('Chile'[year], -1, YEAR))
RETURN
    DIVIDE(PIBActual - PIBAnterior, PIBAnterior)

-- Ranking de regiones por pobreza
RankPobreza =
RANKX(
    ALL(Regiones[region]),
    [Pobreza Promedio],
    ,
    DESC
)
```

## Reproducir

```bash
cd projects/02_powerbi_chile
pip install pandas plotly matplotlib
python src/dashboard_indicadores.py
```

Genera:
- `docs/dashboard_chile.html` — dashboard completo interactivo
- `docs/01_dashboard_preview.png` — preview estático
- `data/chile_indicators_2000_2023.csv` — dataset listo para Power BI
- `data/chile_regions_2022.csv` — datos regionales

---

📁 **Código completo**: [`projects/02_powerbi_chile/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/02_powerbi_chile)
