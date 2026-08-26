---
layout: page
lang: en
title: Chilean Ecovillages Database
description: Design and implementation of a PostgreSQL relational database to manage information on Chilean ecological communities.
img: assets/img/projects/p5_sql.png
importance: 6
category: Technical
related_publications: false
---

Design and implementation of a **relational database** (PostgreSQL / SQLite) to manage information on Chilean ecological communities. The domain comes from my **published academic research** (2017 book + 4 articles on the topic).

**Schema**: 8 tables with 1:N and N:M relationships (ecovillage, member, role, activity, activity_category, participation, resource, production).

**15 queries** organized by difficulty:
- **Basic**: SELECT, JOIN, GROUP BY, ORDER BY
- **Intermediate**: subqueries, HAVING, CTEs
- **Advanced**: WINDOW functions (RANK, NTILE, ROW_NUMBER, PERCENT_RANK)

**Sample data**: 5 anonymized Chilean ecovillages, 25 pseudonymized members (codes like CRI-001), 17 activities, 14 economic outputs.

[Full SQL code on GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/05_ecoaldeas_sql)
