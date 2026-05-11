---
layout: page
lang: en
title: Income Inequality in Chile
description: Statistical analysis in R of economic and time inequality in Chile, using CASEN and ENUT data.
img: assets/img/projects/p3_desigualdad.png
importance: 4
category: work
related_publications: false
---

Quantitative analysis of economic inequality in Chile using **R + tidyverse + ineq**, with a Python equivalent for cross-validation.

**Question**: does time inequality (paid work, care work, leisure) follow the same pattern as income inequality? Are there doubly vulnerable groups?

**Indices computed**: Gini, Theil, Atkinson (ε=0.5 and 1.0), P90/P10 ratio.

**Key results**:
- Income Gini: 0.45 (consistent with Chilean reality, OECD-1 in inequality)
- P90/P10 ratio: 9.04 (the top 10% earns 9 times what the bottom 10% earns)
- **Robust gender gap**: women report +12 weekly hours of unpaid care work compared to men in the same quintile, *across all quintiles*

[R and Python code on GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/03_desigualdad_r)
