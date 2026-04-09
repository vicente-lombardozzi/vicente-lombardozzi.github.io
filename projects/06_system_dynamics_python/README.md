# Proyecto 6 — System Dynamics: de Vensim a Python

Re-implementación en Python (`scipy.integrate`) de modelos de dinámica de sistemas que originalmente construí en **Vensim** durante mi MSc en Leeds (2019).

## Modelos incluidos

1. **Lotka-Volterra** (depredador-presa) — series temporales y plano de fase
2. **Savings-Income** — modelo de stock-flow para acumulación de capital
3. **Recurso renovable logístico** — comparación de tasas de extracción sostenible vs. excesiva

## Estructura

```
06_system_dynamics_python/
├── README.md
├── requirements.txt
├── src/
│   └── lotka_volterra.py
├── models/                      (archivos .mdl originales de Vensim 2019)
│   ├── Lotka2.mdl
│   ├── tutorial exercise 1 (savings-income).mdl
│   └── ...
├── figures/
│   ├── 00_thumbnail.png
│   ├── 01_lotka_volterra.png
│   ├── 02_savings_income.png
│   └── 03_renewable_resource.png
└── notebooks/                   (versión Jupyter, opcional)
```

## Reproducir

```bash
pip install -r requirements.txt
python src/lotka_volterra.py
```

## Por qué Python en lugar de Vensim

- Vensim es **software cerrado y de pago** (~$1.295/año)
- Python + scipy es **gratis, abierto y reproducible**
- Los archivos `.py` se versionan en Git; los `.mdl` de Vensim son binarios
- **Misma matemática, misma precisión**, mejor portabilidad

Ver tarjeta del proyecto en el portafolio: [/projects/6_system_dynamics/](https://vicente-lombardozzi.github.io/projects/6_system_dynamics/)
