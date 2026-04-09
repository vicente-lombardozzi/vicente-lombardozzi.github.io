# Proyecto 7 — CBA Paneles Solares · Liceo Alfredo Nazar Feres (Valparaíso)

Re-implementación en Python del análisis costo-beneficio que originalmente realicé en Excel durante mi MSc en Leeds (2019), evaluando 70 kWp de paneles fotovoltaicos en una escuela pública chilena bajo el programa "Techos Solares Públicos".

## Datos del proyecto real

- **Liceo**: Alfredo Nazar Feres, Valparaíso (1.200 estudiantes)
- **Instalación**: 280 paneles PV de 250 Wp = 70 kWp totales
- **Producción estimada**: 103.110 kWh/año
- **CO₂ evitado**: 35,7 toneladas/año
- **Vida útil del proyecto**: 20 años
- **Propuestas comparadas**: Ecoambiente Ingeniería vs Ecolife (datos reales)

## Estructura

```
07_cba_solar_liceo/
├── README.md
├── requirements.txt
├── src/
│   └── cba_liceo_solar.py
├── data/
│   ├── npv_summary.csv
│   └── cashflow_p2_base.csv
├── figures/
│   ├── 00_thumbnail.png
│   ├── 01_npv_scenarios.png
│   ├── 02_2019_vs_2026.png
│   └── 03_sensitivity.png
└── docs/
    ├── datos_originales_2019/    (cotizaciones, fichas técnicas, respuesta del Ministerio)
    └── graficos_2019/            (sensibilidad original en Excel)
```

## Reproducir

```bash
pip install -r requirements.txt
python src/cba_liceo_solar.py
```

## Resultados (escenario base)

| Escenario | NPV a 20 años (USD) |
|---|---|
| Sin proyecto (BAU) | -146.544 |
| **Propuesta 2 — Ecolife** | **+62.288** ⭐ |
| Propuesta 2 — actualizado 2026 | **+96.486** |
| Peor escenario combinado | -3.880 |

Ver tarjeta del proyecto en el portafolio: [/projects/7_cba_solar/](https://vicente-lombardozzi.github.io/projects/7_cba_solar/)
