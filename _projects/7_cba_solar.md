---
layout: page
title: CBA Paneles Solares Liceo
description: Re-implementacion en Python de un CBA real sobre instalacion de 70 kWp fotovoltaicos en el Liceo Alfredo Nazar Feres (Valparaiso). Incluye analisis de sensibilidad.
img: assets/img/projects/p7_cba.png
importance: 2
category: data
---

Analisis Costo-Beneficio (CBA) **real** sobre la instalacion de paneles fotovoltaicos en el **Liceo Tecnico Alfredo Nazar Feres** de Valparaiso, en el marco del programa "Techos Solares Publicos" del Ministerio de Energia de Chile.

**Datos reales del proyecto**:
- 1.200 estudiantes, 805 m2 de techo util, planta de **70 kWp** (280 modulos PV de 250 Wp)
- 2 propuestas reales de empresas chilenas: **Ecoambiente Ingenieria** y **Ecolife**
- Comunicacion oficial con el Ministerio de Energia (con respuesta documentada)
- Vida util del proyecto: 20 anos
- Tasa de descuento: 3.5% (HM Treasury Green Book)

**Resultados (escenario base, Propuesta 2 - Ecolife)**:

| Escenario | NPV a 20 anos (USD) |
|---|---|
| Sin proyecto (BAU) | -146.544 |
| **Propuesta 2 - Ecolife** | **+62.288** |
| Propuesta 2 - actualizado 2026 | **+96.486** |
| Peor escenario combinado | -3.880 |

En 2026 reimplemente todo el analisis en **Python** y actualize parametros: el precio del CO2 paso de USD 17.6/ton (2018) a USD 85/ton (2026), casi 5 veces mas.

[Codigo Python + planilla Excel + documentos oficiales 2019](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/07_cba_solar_liceo)
