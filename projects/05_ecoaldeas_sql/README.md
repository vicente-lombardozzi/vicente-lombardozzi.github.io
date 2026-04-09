# Proyecto 5 — Base de Datos Relacional: Ecoaldeas Chilenas

Diseño e implementación de una base de datos relacional para gestionar información sobre comunidades ecológicas chilenas. Demuestra **SQL avanzado** (window functions, CTEs, agregaciones complejas) usando un dominio que conozco profundamente porque proviene de mi propia investigación académica publicada.

## Estructura

```
05_ecoaldeas_sql/
├── README.md
├── schema/
│   ├── 01_create_tables.sql       (DDL — 8 tablas con relaciones)
│   └── 02_insert_sample_data.sql  (datos sintéticos anonimizados)
├── queries/
│   ├── 01_basic_queries.sql       (5 queries básicas)
│   ├── 02_intermediate_queries.sql (5 queries intermedias)
│   └── 03_advanced_queries.sql    (5 queries avanzadas con WINDOW)
├── src/
│   └── run_analysis.py            (validación y visualización con SQLite)
└── docs/
    ├── 00_thumbnail.png
    └── *.png                      (gráficos generados de los queries)
```

## 8 tablas, 25 miembros, 17 actividades, 14 productos

- `ecovillage` — entidad principal (5 ecoaldeas chilenas anonimizadas)
- `member` — pseudonimizado (códigos como `CRI-001`)
- `role`, `activity`, `activity_category` — taxonomías
- `participation` — tabla puente N:M
- `resource` — recursos materiales y energéticos
- `production` — productos económicos

## Reproducir

**Con SQLite (recomendado para pruebas)**:
```bash
pip install pandas matplotlib
python src/run_analysis.py
```

**Con PostgreSQL (entorno real)**:
```bash
psql -U postgres -c "CREATE DATABASE ecoaldeas;"
psql -U postgres -d ecoaldeas -f schema/01_create_tables.sql
psql -U postgres -d ecoaldeas -f schema/02_insert_sample_data.sql
psql -U postgres -d ecoaldeas -f queries/03_advanced_queries.sql
```

Ver tarjeta del proyecto en el portafolio: [/projects/5_ecoaldeas_sql/](https://vicente-lombardozzi.github.io/projects/5_ecoaldeas_sql/)
