---
layout: page
title: "System Dynamics: de Vensim a Python"
description: Re-implementación en Python (scipy.integrate) de modelos de dinámica de sistemas que originalmente construí en Vensim durante mi MSc en Leeds. Incluye Lotka-Volterra, savings-income y un modelo de recurso renovable.
img: assets/img/projects/p6_systemdyn.png
importance: 7
category: investigacion
giscus_comments: false
---

## Contexto del proyecto

Durante el Assignment 2 del curso *Tools and Techniques in Ecological Economics* (MSc Leeds 2019) construí varios modelos de dinámica de sistemas usando **Vensim**. Vensim es un software profesional pero **cerrado y de pago**, lo cual significa que mis modelos originales solo podían ser ejecutados por alguien con licencia de Vensim instalada.

**En 2026 los porté a Python** usando `scipy.integrate.odeint`, manteniendo exactamente la misma matemática pero ahora ejecutables en cualquier computadora con Python.

## Modelos incluidos

### 1. Lotka-Volterra (depredador-presa)

El sistema clásico de ecuaciones diferenciales acopladas que describe la dinámica entre dos poblaciones:

$$
\frac{dx}{dt} = \alpha x - \beta xy
$$

$$
\frac{dy}{dt} = \delta xy - \gamma y
$$

Donde $x$ = presas, $y$ = depredadores. Visualizamos tanto las **series temporales** (oscilaciones) como el **plano de fase** (órbitas cerradas características).

### 2. Modelo Savings-Income

Un modelo simple de stock-flow para acumulación de capital:

$$
\frac{dK}{dt} = sY - dK
$$

$$
Y = aK
$$

Donde $K$ es el stock de capital, $Y$ el ingreso, $s$ la tasa de ahorro, $d$ la depreciación y $a$ la productividad del capital. El modelo converge a un equilibrio $K^* = saK_0/d$.

### 3. Recurso renovable (modelo logístico con extracción)

Modelo aplicado a sostenibilidad — un recurso natural (bosque, pesquería) que crece logísticamente y es extraído por la actividad humana:

$$
\frac{dR}{dt} = gR\left(1 - \frac{R}{K}\right) - hR
$$

Compara tres escenarios de tasas de extracción ($h = 0.10$, $0.20$, $0.35$) para mostrar cómo extracciones moderadas son sostenibles, pero superar un umbral lleva al colapso del recurso.

## ¿Por qué Python en lugar de Vensim?

| Criterio | Vensim | Python (scipy) |
|---|---|---|
| **Costo de licencia** | $~$1.295 USD/año | Gratis |
| **Portabilidad** | Solo Windows con licencia | Cualquier OS, cualquier máquina |
| **Reproducibilidad** | Requiere abrir el `.mdl` en Vensim | `python script.py` |
| **Versionado en Git** | Archivos binarios `.mdl` | Texto plano `.py` |
| **Aprendizaje** | Curva alta | scipy es estándar científico |
| **Visualización** | Limitada al output de Vensim | matplotlib + plotly libres |

Los **mismos modelos** que en 2019 corrían solo en mi laptop con Vensim, hoy pueden ser clonados, ejecutados y modificados por cualquiera en el mundo desde GitHub.

## Aplicabilidad profesional

Modelar sistemas dinámicos es una habilidad poco común entre Data Analysts junior, pero **muy valorada** en:

- **Consultoras de sostenibilidad** (forecasting de impacto ambiental)
- **Think tanks de política pública** (simulación de escenarios)
- **Empresas de climate-tech** (Watershed, Persefoni, Sinai)
- **Investigación científica aplicada** (CEPAL, Banco Mundial)
- **Modelado epidemiológico, financiero, energético**

## Tecnologías usadas

- **Python 3.13**
- **scipy.integrate.odeint** — solver de ecuaciones diferenciales ordinarias
- **numpy** — operaciones numéricas
- **matplotlib** — series temporales, planos de fase

## Reproducir

```bash
cd projects/06_system_dynamics_python
python src/lotka_volterra.py
```

Genera 4 figuras en `figures/`:
- `01_lotka_volterra.png` — series temporales y plano de fase
- `02_savings_income.png` — acumulación de capital
- `03_renewable_resource.png` — comparación de tasas de extracción
- `00_thumbnail.png` — preview para el portafolio

## Archivos Vensim originales

El repositorio incluye los archivos `.mdl` originales de Vensim (2019) en `models/` como archivo histórico. Pueden abrirse en Vensim PLE (versión gratuita) si se quiere comparar con los outputs de Python.

---

📁 **Código completo**: [`projects/06_system_dynamics_python/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/06_system_dynamics_python)
