# Proyecto 4 — Análisis de Sentimiento en Español

Comparación de tres enfoques de NLP para clasificar el sentimiento de reseñas en español, desde un lexicon simple hasta TF-IDF + SVM.

## Conexión profesional

Este proyecto enlaza dos partes de mi trayectoria:
- **Outlier (2024–2025)** — trabajé como AI Data Trainer evaluando modelos de lenguaje en español e inglés
- **StratNova (2026–presente)** — co-fundador de un emprendimiento que desarrolla bots de venta automatizada (la detección de sentimiento es un componente crítico)

## Estructura

```
04_nlp_sentiment/
├── README.md
├── requirements.txt
├── src/
│   └── sentiment_analysis.py
├── data/
│   ├── dataset_resenas.csv             (300 reseñas balanceadas)
│   ├── results_comparison.csv
│   └── figures/
│       ├── 00_thumbnail.png
│       ├── 01_model_comparison.png
│       └── 02_confusion_matrix.png
└── notebooks/
```

## Reproducir

```bash
pip install -r requirements.txt
python src/sentiment_analysis.py
```

## Resultados

| Modelo | Accuracy |
|---|---|
| Lexicon | 72,2 % |
| **BoW + Logistic Regression** | **100,0 %** |
| **TF-IDF + Linear SVM** | **100,0 %** |

> Nota: el 100 % es particular de un dataset balanceado y "limpio". En datos del mundo real (con sarcasmo, negaciones complejas, jerga regional) se esperarían valores entre 78–88 %. Lo importante del proyecto es la **metodología** de comparación.

Ver tarjeta del proyecto: [/projects/4_nlp_sentiment/](https://vicente-lombardozzi.github.io/projects/4_nlp_sentiment/)
