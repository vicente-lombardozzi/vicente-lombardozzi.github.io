# Proyecto 2 — Dashboard de Indicadores Socioeconómicos de Chile

Dashboard interactivo con datos del **Banco Mundial** (2000–2023) y la **encuesta CASEN 2022**, construido en **Plotly** como alternativa open-source equivalente a Power BI.

## Estructura

```
02_powerbi_chile/
├── README.md
├── requirements.txt
├── src/
│   └── dashboard_indicadores.py
├── data/
│   ├── chile_indicators_2000_2023.csv  (24 años, 8 variables)
│   └── chile_regions_2022.csv          (16 regiones, CASEN)
├── docs/
│   ├── dashboard_chile.html            (DASHBOARD INTERACTIVO ⭐)
│   ├── 00_thumbnail.png
│   └── 01_dashboard_preview.png
└── sql/                                 (queries equivalentes Power BI)
```

## Reproducir

```bash
pip install -r requirements.txt
python src/dashboard_indicadores.py
```

Abrir el dashboard interactivo: `docs/dashboard_chile.html`

## ¿Por qué Plotly y no Power BI?

| Criterio | Power BI | Plotly |
|---|---|---|
| Costo | Power BI Pro: ~10 USD/mes | Gratis |
| Embebible en GitHub Pages | No | Sí |
| Versionable en Git | Difícil (.pbix binario) | Fácil (.py + .html) |
| Auditable | Solo con licencia | Cualquiera |

**Para reclutadores que pidan Power BI**: el archivo `data/chile_indicators_2000_2023.csv` puede abrirse directamente en Power BI Desktop, y las medidas DAX equivalentes están documentadas en la tarjeta del proyecto del portafolio.

Ver tarjeta del proyecto: [/projects/2_powerbi_chile/](https://vicente-lombardozzi.github.io/projects/2_powerbi_chile/)
