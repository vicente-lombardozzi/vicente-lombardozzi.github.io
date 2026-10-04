---
layout: page
lang: en
title: Investment Appraisal (NPV and Sensitivity)
description: 20-year cost-benefit analysis of an infrastructure project at a Valparaíso high school, with two real bids. Excel (2019) and Python (2026).
img: assets/img/projects/p7_cba.png
importance: 2
category: Work
related_publications: false
---

**Cost-benefit analysis** of a real energy-infrastructure project (a 70 kWp photovoltaic plant) at a technical high school in Valparaíso, submitted to a Ministry of Energy programme.

**Method**:

- **20-year cash flows** for two real bids from Chilean firms, against the no-project scenario
- **Net present value (NPV)** at a 3.5% discount rate (HM Treasury Green Book) and an alternative 10% rate
- **Sensitivity analysis**: electricity tariff (±20%), discount rate and a combined downside scenario

**Tools**: I built the original analysis in **Excel** during my MSc (2019); in 2026 I re-implemented it in **Python** (pandas) to make it reproducible and update parameters. Results depend on tariff and investment-cost assumptions documented in the code.

[Code, Excel workbook and original documents on GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/07_cba_solar_liceo)
