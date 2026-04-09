---
layout: page
title: System Dynamics de Vensim a Python
description: Re-implementacion en Python (scipy.integrate) de modelos de dinamica de sistemas que originalmente construi en Vensim durante mi MSc en Leeds.
img: assets/img/projects/p6_systemdyn.png
importance: 7
category: fun
related_publications: false
---

Re-implementacion en **Python (scipy.integrate.odeint)** de modelos de dinamica de sistemas que originalmente construi en **Vensim** durante el Assignment 2 del curso *Tools and Techniques in Ecological Economics* (MSc Leeds 2019).

**Modelos incluidos**:
- **Lotka-Volterra** (depredador-presa) con plano de fase
- **Savings-Income** (acumulacion de capital, equilibrio dinamico)
- **Recurso renovable logistico** con extraccion (sostenibilidad vs colapso)

**Por que Python en lugar de Vensim**: Vensim es software cerrado y de pago (~1.295 USD/ano). Python con scipy es gratis, abierto y reproducible. Misma matematica, mejor portabilidad.

[Codigo Python y modelos Vensim originales en GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/06_system_dynamics_python)
