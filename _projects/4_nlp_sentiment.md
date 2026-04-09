---
layout: page
title: Sentiment Analysis en Espanol
description: Comparacion de tres enfoques de NLP para clasificar sentimiento en resenas en espanol, desde un lexicon simple hasta TF-IDF y SVM.
img: assets/img/projects/p4_nlp.png
importance: 5
category: work
related_publications: false
---

Comparacion de tres enfoques de **NLP** para clasificar el sentimiento de resenas en espanol, conectando con mi experiencia previa como **AI Data Trainer en Outlier** y mi rol actual como co-fundador de **StratNova** (bots de venta automatizada).

**Modelos comparados**:

| Modelo | Accuracy |
|---|---|
| Lexicon (diccionario) | 72.2 % |
| Bag-of-Words + Logistic Regression | 100 % |
| TF-IDF + Linear SVM | 100 % |

> Nota: el 100% es particular de un dataset balanceado. En datos reales con sarcasmo y jerga regional, los enfoques clasicos rondan 78-88 %.

**Stack**: Python + scikit-learn + pandas + matplotlib.

[Codigo en GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/04_nlp_sentiment)
