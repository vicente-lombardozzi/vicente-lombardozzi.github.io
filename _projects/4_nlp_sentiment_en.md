---
layout: page
lang: en
title: Spanish Sentiment Analysis
description: Comparison of three NLP approaches to classify sentiment in Spanish-language reviews, from a simple lexicon to TF-IDF and SVM.
img: assets/img/projects/p4_nlp.png
importance: 5
category: work
related_publications: false
---

Comparison of three **NLP** approaches to classify the sentiment of Spanish-language reviews, connecting with my previous experience as an **AI Data Trainer at Outlier** and my current role as co-founder of **StratNova** (automated sales bots).

**Models compared**:

| Model | Accuracy |
|---|---|
| Lexicon (dictionary) | 72.2 % |
| Bag-of-Words + Logistic Regression | 100 % |
| TF-IDF + Linear SVM | 100 % |

> Note: the 100% is specific to a balanced dataset. On real data with sarcasm and regional slang, classical approaches typically score 78-88%.

**Stack**: Python + scikit-learn + pandas + matplotlib.

[Code on GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/04_nlp_sentiment)
