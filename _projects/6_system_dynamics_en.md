---
layout: page
lang: en
title: System Dynamics from Vensim to Python
description: Python re-implementation (scipy.integrate) of system-dynamics models I originally built in Vensim during my MSc at Leeds.
img: assets/img/projects/p6_systemdyn.png
importance: 7
category: Technical
related_publications: false
---

**Python (scipy.integrate.odeint)** re-implementation of system-dynamics models I originally built in **Vensim** during Assignment 2 of the *Tools and Techniques in Ecological Economics* course (MSc Leeds 2019).

**Models included**:
- **Lotka-Volterra** (predator-prey) with phase plane
- **Savings-Income** (capital accumulation, dynamic equilibrium)
- **Logistic renewable resource** with extraction (sustainability vs collapse)

**Why Python instead of Vensim**: Vensim is closed-source and paid software (~USD 1,295/year). Python with scipy is free, open and reproducible. Same math, better portability.

[Python code and original Vensim models on GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/06_system_dynamics_python)
