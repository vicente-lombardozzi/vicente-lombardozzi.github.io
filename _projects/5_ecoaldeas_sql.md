---
layout: page
title: "Base de Datos Relacional: Ecoaldeas Chilenas"
description: Diseño e implementación de una base de datos PostgreSQL para gestionar información sobre comunidades ecológicas chilenas, basada en mi propia investigación académica publicada.
img: assets/img/projects/p5_sql.png
importance: 6
category: investigacion
giscus_comments: false
---

## Contexto del proyecto

Este proyecto cruza tres capas de mi perfil:

1. **SQL avanzado**: diseño de esquema relacional, queries con `WINDOW FUNCTIONS`, `CTEs`, agregaciones complejas.
2. **Investigación académica propia**: el dominio (ecoaldeas chilenas) viene de mi libro publicado en Editorial Académica Española (2017) y de mis 4 artículos sobre el tema.
3. **Privacidad y ética**: trabajo con pseudonimización a nivel de schema, en línea con los estándares de investigación social.

## Pregunta

¿Cómo se puede modelar formalmente la complejidad organizativa de una ecoaldea —miembros, actividades, recursos, producción económica— en una base de datos relacional que permita responder preguntas analíticas?

## Diseño del esquema

```
┌──────────────┐         ┌──────────────┐
│  ecovillage  │1───────N│   member     │N────1┐
└──────┬───────┘         └──────┬───────┘      │
       │                        │              │
       1                        N         ┌────▼─────┐
       │                        │         │   role   │
       N                        N         └──────────┘
┌──────▼──────┐         ┌───────▼──────┐
│  resource   │         │participation │N───────┐
└─────────────┘         └──────────────┘        │
                                                 │
┌──────────────┐         ┌──────────────┐       N
│  production  │         │   activity   │N──────┘
│              │         │              │
└──────────────┘         └──────┬───────┘
                                │
                                N
                                │
                         ┌──────▼────────┐
                         │ activity_cat  │
                         └───────────────┘
```

**8 tablas** con relaciones 1:N y N:M:
- `ecovillage` — entidad principal
- `member` — miembros con pseudonimización (códigos en lugar de nombres)
- `role` — roles que pueden cumplir
- `activity` + `activity_category` — actividades dentro de cada ecoaldea
- `participation` — tabla puente (M:N) miembros ↔ actividades, con horas semanales
- `resource` — recursos materiales y energéticos
- `production` — productos económicos comercializados

## Datos de ejemplo

5 ecoaldeas chilenas (anonimizadas), 25 miembros, 17 actividades, 14 productos económicos. Los datos están basados en investigación real pero los nombres son ficticios para proteger la privacidad de las comunidades.

## Queries destacadas (15 totales)

### Nivel básico
- Listar ecoaldeas con su antigüedad
- Cantidad de miembros por ecoaldea (con fundadores y permanentes)
- Distribución de miembros por grupo etario

### Nivel intermedio
- Promedio de horas semanales por categoría de actividad y región (`HAVING`)
- Ingresos por tipo de producto y participación porcentual (subconsultas)
- Auto-suficiencia energética por ecoaldea (`CTE`)

### Nivel avanzado
- Ranking de ecoaldeas por diversidad productiva (`RANK`, `PERCENT_RANK`, `WINDOW`)
- Productividad económica por hectárea (`NTILE` para terciles)
- Análisis de retención de miembros con `ROW_NUMBER`

## Resultados con datos sintéticos

| Métrica | Valor |
|---|---|
| Promedio de horas por miembro en producción agrícola | 19,3 h/sem |
| Productividad económica máxima (ingresos/ha) | 1,16 M CLP/ha (Comunidad Crisálida) |
| Ecoaldea más diversa productivamente | Pewkayal (3 tipos de productos) |
| Brecha entre ecoaldea más antigua y más reciente | 17 años |

## Tecnologías usadas

- **PostgreSQL 14+** (compatible con SQLite 3.35+ para pruebas)
- **Python + sqlite3** — script de validación y visualización
- **pandas + matplotlib** — visualización de resultados
- **Diagramas ER** documentados en `docs/`

## Decisiones de diseño

1. **Pseudonimización**: los miembros se identifican con códigos como `CRI-001` en lugar de nombres reales, replicando el estándar ético de la investigación social.
2. **CASCADE en relaciones**: si se elimina una ecoaldea, se eliminan en cascada sus miembros, actividades y producciones (refleja dependencia ontológica).
3. **CHECK constraints**: validación a nivel de base de datos para garantizar integridad numérica.
4. **Índices**: en columnas usadas frecuentemente en JOINs y WHEREs.

## Reproducir

**PostgreSQL**:
```bash
psql -U postgres -c "CREATE DATABASE ecoaldeas;"
psql -U postgres -d ecoaldeas -f schema/01_create_tables.sql
psql -U postgres -d ecoaldeas -f schema/02_insert_sample_data.sql
psql -U postgres -d ecoaldeas -f queries/01_basic_queries.sql
```

**SQLite (script de validación en Python)**:
```bash
cd projects/05_ecoaldeas_sql
python src/run_analysis.py
```

---

📁 **Código completo**: [`projects/05_ecoaldeas_sql/`](https://github.com/vicente-lombardozzi/vicente-lombardozzi.github.io/tree/main/projects/05_ecoaldeas_sql)
