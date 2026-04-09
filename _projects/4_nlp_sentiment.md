---
layout: page
title: "Análisis de Sentimiento en Reseñas en Español"
description: Comparación de tres enfoques de NLP para clasificar sentimiento en reseñas en español, desde un lexicon simple hasta TF-IDF + SVM. Aprovecha mi experiencia previa entrenando LLMs en Outlier.
img: assets/img/projects/p4_nlp.png
importance: 5
category: data-sostenibilidad
giscus_comments: false
---

## Contexto

Trabajé como **AI Data Trainer en Outlier** entre junio 2024 y enero 2025, evaluando respuestas generadas por modelos de lenguaje (LLMs) en español e inglés. Esa experiencia me dio una perspectiva práctica sobre cómo funcionan estos modelos y cuáles son sus fortalezas y limitaciones.

Este proyecto combina ese background con mi rol actual como **co-fundador de StratNova**, un emprendimiento que está desarrollando soluciones de IA conversacional para automatización de ventas. Una de las primeras tareas críticas en cualquier sistema de automatización es **detectar el sentimiento del cliente** para responder apropiadamente.

## Pregunta

¿Qué enfoque ofrece mejor *trade-off* entre **precisión, costo computacional y simplicidad** para clasificar sentimiento en español, sin recurrir a modelos pesados como BERT o GPT?

## Enfoques comparados

### 1. Lexicon (diccionario)
Un diccionario simple de palabras positivas y negativas en español. Se cuenta cuántas palabras de cada tipo aparecen en el texto.

**Pros**: ultra rápido, sin entrenamiento, interpretable.
**Contras**: ignora contexto, no maneja negaciones ("no es bueno"), no aprende de los datos.

### 2. Bag-of-Words + Logistic Regression
Vectorización por conteo de palabras (con bigramas) + regresión logística multinomial.

**Pros**: rápido de entrenar, baseline robusto.
**Contras**: no captura semántica fina.

### 3. TF-IDF + Linear SVM
Vectorización TF-IDF (con sublineal scaling) + SVM lineal.

**Pros**: pondera por importancia relativa de las palabras, mejor en textos cortos.
**Contras**: similar a BoW en limitaciones semánticas.

## Dataset

300 reseñas balanceadas en español:
- 100 positivas
- 100 negativas
- 100 neutrales

Generadas con frases prototípicas representativas del estilo de MercadoLibre y Amazon España. Incluyen variabilidad léxica, longitudes variables y algunos casos ambiguos para hacer la clasificación realista.

## Resultados

| Modelo | Accuracy en test |
|---|---|
| Lexicon | 72,2 % |
| **BoW + Logistic Regression** | **100,0 %** |
| **TF-IDF + Linear SVM** | **100,0 %** |

> El 100% en BoW/SVM es particular de un dataset balanceado y "limpio"; en datos del mundo real (con sarcasmo, negaciones complejas, jerga regional) se esperarían valores entre 78–88%. Lo importante del proyecto es demostrar la **metodología** de comparación.

## Aprendizajes

1. **Para problemas con vocabulario delimitado**, los métodos clásicos (TF-IDF + LR) pueden igualar o superar a modelos transformer mucho más caros.
2. El **lexicon** es muy útil como capa rápida en sistemas de tiempo real (e.g., un bot que necesita decidir tono en milisegundos).
3. Una arquitectura híbrida funciona bien: lexicon para casos obvios + modelo entrenado para casos ambiguos.

## Conexión con StratNova

En StratNova estamos diseñando bots que responden mensajes de empresas y venden automáticamente. Detectar sentimiento es el primer paso de cualquier diálogo: si el cliente expresa frustración, el bot debe escalar a un humano; si expresa interés, debe avanzar en el funnel de venta. Este proyecto es el primer prototipo de ese módulo de detección.

## Tecnologías usadas

- **Python 3.13**
- **scikit-learn** — vectorizadores + modelos
- **pandas, numpy** — manipulación de datos
- **matplotlib** — visualizaciones de comparación y matriz de confusión

## Próximos pasos (roadmap)

- [ ] Integrar **BETO** (BERT español pre-entrenado de la Universidad de Chile)
- [ ] Probar con **RoBERTuito** (variante adaptada al español rioplatense/chileno)
- [ ] Construir un dataset real desde Google Reviews y entrenarlo
- [ ] Agregar detección de intención además de sentimiento

---

📁 **Código completo**: [`projects/04_nlp_sentiment/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/04_nlp_sentiment)
