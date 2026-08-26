---
layout: page
lang: en
title: Solar Panels CBA — Chilean High School
description: Python re-implementation of a real Cost-Benefit Analysis for a 70 kWp PV installation at Liceo Alfredo Nazar Feres (Valparaíso).
img: assets/img/projects/p7_cba.png
importance: 2
category: Work
related_publications: false
---

**Real** Cost-Benefit Analysis (CBA) on the installation of solar PV panels at **Liceo Técnico Alfredo Nazar Feres** in Valparaíso, under Chile's Ministry of Energy "Public Solar Rooftops" programme.

**Real project data**:
- 1,200 students, 805 m² of usable roof area, **70 kWp** plant (280 PV modules of 250 Wp)
- 2 actual bids from Chilean firms: **Ecoambiente Ingeniería** and **Ecolife**
- Official correspondence with the Ministry of Energy (with documented response)
- Project lifetime: 20 years
- Discount rate: 3.5% (HM Treasury Green Book)

**Results (base scenario, Bid 2 - Ecolife)**:

| Scenario | 20-year NPV (USD) |
|---|---|
| No project (BAU) | -146,544 |
| **Bid 2 - Ecolife** | **+62,288** |
| Bid 2 - 2026 update | **+96,486** |
| Worst-case combined | -3,880 |

In 2026 I re-implemented the entire analysis in **Python** and updated parameters: the CO2 price rose from USD 17.6/ton (2018) to USD 85/ton (2026), almost 5x.

[Python code, Excel workbook and 2019 official documents on GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/07_cba_solar_liceo)
