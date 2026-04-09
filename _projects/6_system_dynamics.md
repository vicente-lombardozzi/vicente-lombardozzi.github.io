---
layout: page
title: System Dynamics de Vensim a Python
description: Re-implementacion en Python (scipy.integrate) de modelos de dinamica de sistemas que originalmente construi en Vensim durante mi MSc en Leeds.
img: assets/img/projects/p6_systemdyn.png
importance: 7
category: investigacion
---

Re-implementacion en **Python (scipy.integrate.odeint)** de modelos de dinamica de sistemas que originalmente construi en **Vensim** durante el Assignment 2 del curso *Tools and Techniques in Ecological Economics* (MSc Leeds 2019).

**Modelos incluidos**:
- **Lotka-Volterra** (depredador-presa) con plano de fase
- **Savings-Income** (acumulacion de capital, equilibrio dinamico)
- **Recurso renovable logistico** con extraccion (sostenibilidad vs colapso)

**Por que Python en lugar de Vensim**:

| Criterio | Vensim | Python (scipy) |
|---|---|---|
| Costo de licencia | ~1.295 USD/ano | Gratis |
| Portabilidad | Solo Windows con licencia | Cualquier OS |
| Versionable en Git | Archivos binarios | Texto plano |

**Misma matematica**, mejor portabilidad, totalmente reproducible.

[Codigo Python + modelos Vensim originales en GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/06_system_dynamics_python)
