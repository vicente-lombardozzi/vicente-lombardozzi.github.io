---
layout: page
title: "Análisis Costo-Beneficio: Paneles Solares en una Escuela Pública"
description: Re-implementación en Python de un CBA real sobre instalación de 70 kWp fotovoltaicos en el Liceo Alfredo Nazar Feres (Valparaíso). Incluye análisis de sensibilidad y actualización de parámetros 2019 → 2026.
img: assets/img/projects/p7_cba.png
importance: 2
category: data-sostenibilidad
giscus_comments: false
---

## Contexto del proyecto

Durante mi máster en Leeds (2019) realicé un análisis costo-beneficio (CBA) **real** sobre la instalación de paneles fotovoltaicos en el **Liceo Técnico Alfredo Nazar Feres** de Valparaíso, en el marco del programa **Techos Solares Públicos** del Ministerio de Energía de Chile. El estudio incluyó:

- Comunicación oficial con el Ministerio de Energía de Chile (con respuesta documentada)
- Dos propuestas reales de empresas chilenas: **Ecoambiente Ingeniería** y **Ecolife**
- Datos técnicos del liceo: 1.200 estudiantes, 805 m² de techo útil, planta de **70 kWp** con 280 módulos PV de 250 Wp cada uno
- Cálculo de NPV a 20 años con tasa de descuento del HM Treasury Green Book (3,5 %) y comparación con la tasa social chilena (10 %)
- Análisis de sensibilidad sobre precio de electricidad, tasa de descuento y precio del CO₂

## Por qué este proyecto es diferente

A diferencia de un ejercicio académico genérico, este es un caso **real, verificable y trazable**: el Liceo Alfredo Nazar Feres existe, las dos empresas existen, y los precios son los que efectivamente cotizaron en 2019.

## Re-análisis 2026

En 2026 reimplementé toda la planilla Excel original en **Python con pandas**. La principal ventaja: el código es ahora reproducible, auditable y se puede generalizar fácilmente a otras escuelas del programa.

Además **actualicé los parámetros clave** para reflejar la realidad de 2026:
- **Precio del CO₂**: pasó de USD 17,6/ton (EEX 2018) a USD 85/ton (EU ETS 2026), casi 5 veces más
- **Costos de paneles solares**: cayeron ~40 % entre 2019 y 2025

## Resultados (Propuesta 2 — Ecolife, escenario base)

| Escenario | NPV a 20 años (USD) |
|---|---|
| **Sin proyecto (BAU)** | -146.544 |
| Propuesta 1 — Ecoambiente, dr=3,5 % | +35.615 |
| **Propuesta 2 — Ecolife, dr=3,5 %** | **+62.288** ⭐ |
| Propuesta 2 — dr=10 % (Chile) | +6.346 |
| Propuesta 2 — +20 % precio elec | +89.393 |
| Propuesta 2 — −20 % precio elec | +35.183 |
| Peor escenario (P1 + 20 % elec + dr=10 %) | -3.880 |
| **Propuesta 2 — actualizada 2026 (CO₂ a USD 85)** | **+96.486** |

**Conclusión robusta**: la decisión de instalar los paneles era económicamente óptima en 2019 bajo todos los escenarios excepto el peor combinado, y con los precios actuales del CO₂ es **claramente más rentable** todavía.

## Análisis de sensibilidad

Construí un *tornado chart* con los principales drivers del NPV:

1. **Precio del CO₂** — variable de mayor impacto positivo (paso a USD 85)
2. **Tasa de descuento** — Chile usa 10 % vs el UK 3,5 %
3. **Variación precio electricidad** — ±20 %
4. **Diferencia entre propuestas** — Ecoambiente más cara que Ecolife

## Tecnologías usadas

- **Python 3.13** + pandas + numpy
- **matplotlib** — gráficos de flujos de caja, sensibilidad y comparativos 2019/2026
- **Excel** original (planilla `Cost-benefit A2 VL.xlsx` archivada como referencia)

## Documentación oficial archivada

El repositorio incluye:
- Las dos cotizaciones reales en PDF (Ecoambiente y Ecolife)
- La ficha técnica del Liceo Alfredo Nazar Feres
- La carta-respuesta del Ministerio de Energía
- El proyecto educativo del liceo
- Diagrama Gantt del proyecto fotovoltaico

## Aplicabilidad profesional

Este proyecto demuestra capacidades concretas para roles de:
- **Sustainability / ESG Data Analyst**
- **Climate finance / Carbon accounting**
- **Análisis de proyectos públicos** (CEPAL, BID, Ministerios)
- **Consultoras de eficiencia energética** (Fundación Chile, Energy+, etc.)

---

📁 **Código completo**: [`projects/07_cba_solar_liceo/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/07_cba_solar_liceo)
