---
layout: page
lang: es
title: Evaluación de un proyecto de inversión (VAN y sensibilidad)
description: Análisis costo-beneficio a 20 años de un proyecto de infraestructura en un liceo de Valparaíso, con dos ofertas reales. Excel (2019) y Python (2026).
img: assets/img/projects/p7_cba.png
importance: 2
category: Work
related_publications: false
---

**Análisis costo-beneficio** de un proyecto real de infraestructura energética (planta fotovoltaica de 70 kWp) en un liceo técnico de Valparaíso, postulado a un programa del Ministerio de Energía.

**Método**:

- Flujos de caja a **20 años** para dos ofertas reales de empresas chilenas, frente al escenario sin proyecto
- **Valor actual neto (VAN)** con tasa de descuento de 3,5% (HM Treasury Green Book) y tasa alternativa de 10%
- **Análisis de sensibilidad**: tarifa eléctrica (±20%), tasa de descuento y escenario combinado desfavorable

**Herramientas**: el análisis original lo hice en **Excel** durante el MSc (2019); en 2026 lo reimplementé en **Python** (pandas) para hacerlo reproducible y actualizar parámetros. Los resultados dependen de supuestos de tarifa e inversión que están documentados en el código.

[Código, planilla Excel y documentos originales en GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/07_cba_solar_liceo)
