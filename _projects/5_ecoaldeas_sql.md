---
layout: page
title: Base de Datos de Ecoaldeas Chilenas
description: Diseno e implementacion de una base de datos relacional PostgreSQL para gestionar informacion sobre comunidades ecologicas chilenas.
img: assets/img/projects/p5_sql.png
importance: 6
category: fun
related_publications: false
---

Diseno e implementacion de una **base de datos relacional** (PostgreSQL / SQLite) para gestionar informacion sobre comunidades ecologicas chilenas. El dominio proviene de mi **investigacion academica publicada** (libro 2017 + 4 articulos sobre el tema).

**Schema**: 8 tablas con relaciones 1:N y N:M (ecovillage, member, role, activity, activity_category, participation, resource, production).

**15 queries** organizadas por nivel:
- **Basicas**: SELECT, JOIN, GROUP BY, ORDER BY
- **Intermedias**: subconsultas, HAVING, CTEs
- **Avanzadas**: WINDOW functions (RANK, NTILE, ROW_NUMBER, PERCENT_RANK)

**Datos de ejemplo**: 5 ecoaldeas chilenas anonimizadas, 25 miembros con pseudonimizacion (codigos como CRI-001), 17 actividades, 14 productos economicos.

[Codigo SQL completo en GitHub](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/05_ecoaldeas_sql)
