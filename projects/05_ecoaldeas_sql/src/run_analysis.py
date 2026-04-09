"""
================================================================================
ECOALDEAS CHILENAS — Análisis SQL ejecutado contra SQLite
================================================================================

Carga el schema y datos de ejemplo en una base SQLite en memoria, ejecuta las
queries principales y genera visualizaciones de los resultados.

Las queries originales fueron escritas para PostgreSQL; aquí adaptamos las
funciones específicas de PG (SERIAL → INTEGER, EXTRACT → strftime, etc.) para
poder demostrar la base de datos sin necesidad de instalar PostgreSQL.

Autor: Vicente Lombardozzi
================================================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

SAGE = "#6b9075"
SAGE_DARK = "#4f7058"
SAGE_LIGHT = "#a8c4ad"
CREAM = "#faf9f6"
SLATE = "#2c3e35"
ACCENT_RED = "#c97064"
ACCENT_AMBER = "#d4a25e"

rcParams["font.family"] = "DejaVu Sans"
rcParams["font.size"] = 11
rcParams["axes.edgecolor"] = SLATE
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["figure.facecolor"] = CREAM
rcParams["axes.facecolor"] = CREAM
rcParams["savefig.facecolor"] = CREAM
rcParams["savefig.dpi"] = 150

HERE = Path(__file__).resolve().parent.parent
FIG_DIR = HERE / "docs"
FIG_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Schema simplificado para SQLite (sin SERIAL ni CHECK constraints PG)
# =============================================================================
SCHEMA = """
DROP TABLE IF EXISTS production;
DROP TABLE IF EXISTS participation;
DROP TABLE IF EXISTS resource;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS activity_category;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS ecovillage;

CREATE TABLE ecovillage (
    ecovillage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    province TEXT,
    commune TEXT,
    founded_year INTEGER NOT NULL,
    hectares REAL,
    legal_status TEXT,
    governance_model TEXT,
    description TEXT
);

CREATE TABLE role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE member (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecovillage_id INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id),
    code TEXT NOT NULL,
    join_year INTEGER NOT NULL,
    residency_type TEXT,
    age_group TEXT,
    role_id INTEGER REFERENCES role(role_id),
    is_founder INTEGER DEFAULT 0,
    UNIQUE (ecovillage_id, code)
);

CREATE TABLE activity_category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecovillage_id INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id),
    category_id INTEGER NOT NULL REFERENCES activity_category(category_id),
    name TEXT NOT NULL,
    description TEXT,
    frequency TEXT,
    is_obligatory INTEGER DEFAULT 0
);

CREATE TABLE participation (
    participation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL REFERENCES member(member_id),
    activity_id INTEGER NOT NULL REFERENCES activity(activity_id),
    hours_per_week REAL,
    UNIQUE (member_id, activity_id)
);

CREATE TABLE resource (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecovillage_id INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id),
    type TEXT NOT NULL,
    quantity REAL,
    unit TEXT,
    is_self_produced INTEGER DEFAULT 0,
    measured_year INTEGER
);

CREATE TABLE production (
    production_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecovillage_id INTEGER NOT NULL REFERENCES ecovillage(ecovillage_id),
    product_name TEXT NOT NULL,
    product_type TEXT,
    annual_value_clp INTEGER,
    is_for_sale INTEGER DEFAULT 1,
    is_for_self_consumption INTEGER DEFAULT 1
);
"""


def load_data(conn):
    """Carga el archivo SQL de inserts adaptado a SQLite (TRUE/FALSE -> 1/0)."""
    sql_file = HERE / "schema" / "02_insert_sample_data.sql"
    text = sql_file.read_text(encoding="utf-8")
    text = text.replace("TRUE", "1").replace("FALSE", "0")
    # Limpiar líneas de comentarios sueltos pero preservar estructura de los inserts
    cleaned_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue
        cleaned_lines.append(line)
    cleaned_sql = "\n".join(cleaned_lines)
    conn.executescript(cleaned_sql)
    conn.commit()


# =============================================================================
# Ejecución
# =============================================================================
print("=" * 78)
print("ECOALDEAS CHILENAS — Ejecución de queries SQL")
print("=" * 78)

conn = sqlite3.connect(":memory:")
conn.executescript(SCHEMA)
load_data(conn)
print("\n✓ Schema cargado y datos insertados")

# Verificación
n_eco = conn.execute("SELECT COUNT(*) FROM ecovillage").fetchone()[0]
n_mem = conn.execute("SELECT COUNT(*) FROM member").fetchone()[0]
n_act = conn.execute("SELECT COUNT(*) FROM activity").fetchone()[0]
n_prod = conn.execute("SELECT COUNT(*) FROM production").fetchone()[0]
print(f"  {n_eco} ecoaldeas")
print(f"  {n_mem} miembros")
print(f"  {n_act} actividades")
print(f"  {n_prod} productos económicos")


# =============================================================================
# Q1. Miembros por ecoaldea
# =============================================================================
print("\n" + "-" * 78)
print("Q1: Miembros por ecoaldea")
print("-" * 78)

q1 = """
SELECT
    e.name AS ecoaldea,
    e.region,
    COUNT(m.member_id) AS total_miembros,
    SUM(CASE WHEN m.is_founder = 1 THEN 1 ELSE 0 END) AS fundadores,
    SUM(CASE WHEN m.residency_type = 'permanente' THEN 1 ELSE 0 END) AS permanentes
FROM ecovillage e
LEFT JOIN member m ON m.ecovillage_id = e.ecovillage_id
GROUP BY e.ecovillage_id, e.name, e.region
ORDER BY total_miembros DESC
"""
df1 = pd.read_sql_query(q1, conn)
print(df1.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5))
y_pos = range(len(df1))
ax.barh(y_pos, df1["total_miembros"], color=SAGE, label="Total miembros")
ax.barh(y_pos, df1["fundadores"], color=SAGE_DARK, label="Fundadores")
ax.set_yticks(y_pos)
ax.set_yticklabels(df1["ecoaldea"])
ax.set_xlabel("Número de miembros")
ax.set_title("Miembros por ecoaldea (con cantidad de fundadores)", fontweight="bold")
ax.legend(loc="lower right", frameon=True)
ax.grid(alpha=0.3, ls="--", axis="x")
fig.tight_layout()
fig.savefig(FIG_DIR / "01_miembros_por_ecoaldea.png", bbox_inches="tight")
plt.close(fig)
print(f"\n✓ docs/01_miembros_por_ecoaldea.png")


# =============================================================================
# Q2. Ingresos económicos por tipo de producto y ecoaldea
# =============================================================================
print("\n" + "-" * 78)
print("Q2: Ingresos por tipo de producto")
print("-" * 78)

q2 = """
SELECT
    e.name AS ecoaldea,
    pr.product_type,
    SUM(pr.annual_value_clp) AS ingresos_clp
FROM ecovillage e
JOIN production pr ON pr.ecovillage_id = e.ecovillage_id
GROUP BY e.name, pr.product_type
ORDER BY e.name, ingresos_clp DESC
"""
df2 = pd.read_sql_query(q2, conn)
df2["ingresos_millones"] = df2["ingresos_clp"] / 1e6
print(df2.to_string(index=False))

# Stacked bar
pivot = df2.pivot_table(
    index="ecoaldea", columns="product_type", values="ingresos_millones", fill_value=0
)
fig, ax = plt.subplots(figsize=(11, 6))
colors = [SAGE_DARK, SAGE, SAGE_LIGHT, ACCENT_AMBER, ACCENT_RED, "#888"]
pivot.plot(kind="barh", stacked=True, ax=ax, color=colors[: pivot.shape[1]], edgecolor="white")
ax.set_xlabel("Ingresos anuales (millones CLP)")
ax.set_ylabel("")
ax.set_title("Composición de ingresos por tipo de producto", fontweight="bold")
ax.legend(loc="lower right", frameon=True, fontsize=9)
ax.grid(alpha=0.3, ls="--", axis="x")
fig.tight_layout()
fig.savefig(FIG_DIR / "02_ingresos_por_tipo.png", bbox_inches="tight")
plt.close(fig)
print(f"\n✓ docs/02_ingresos_por_tipo.png")


# =============================================================================
# Q3. Productividad económica por hectárea
# =============================================================================
print("\n" + "-" * 78)
print("Q3: Productividad económica por hectárea")
print("-" * 78)

q3 = """
SELECT
    e.name AS ecoaldea,
    e.hectares,
    SUM(pr.annual_value_clp) AS ingresos_clp_anuales,
    ROUND((SUM(pr.annual_value_clp) / e.hectares) / 1000000.0, 2) AS millones_clp_por_hectarea
FROM ecovillage e
JOIN production pr ON pr.ecovillage_id = e.ecovillage_id
GROUP BY e.ecovillage_id, e.name, e.hectares
ORDER BY millones_clp_por_hectarea DESC
"""
df3 = pd.read_sql_query(q3, conn)
print(df3.to_string(index=False))


# =============================================================================
# Q4. Promedio de horas semanales por categoría de actividad
# =============================================================================
print("\n" + "-" * 78)
print("Q4: Horas semanales promedio por categoría de actividad")
print("-" * 78)

q4 = """
SELECT
    ac.name AS categoria,
    ROUND(AVG(p.hours_per_week), 2) AS promedio_horas,
    COUNT(p.participation_id) AS num_participaciones
FROM participation p
JOIN activity a ON a.activity_id = p.activity_id
JOIN activity_category ac ON ac.category_id = a.category_id
GROUP BY ac.name
ORDER BY promedio_horas DESC
"""
df4 = pd.read_sql_query(q4, conn)
print(df4.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5.5))
y_pos = range(len(df4))
ax.barh(y_pos, df4["promedio_horas"], color=SAGE, edgecolor=SLATE, linewidth=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(df4["categoria"])
ax.set_xlabel("Horas semanales promedio por miembro")
ax.set_title("Tiempo dedicado por categoría de actividad", fontweight="bold")
ax.grid(alpha=0.3, ls="--", axis="x")
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(FIG_DIR / "03_horas_por_categoria.png", bbox_inches="tight")
plt.close(fig)
print(f"\n✓ docs/03_horas_por_categoria.png")


# =============================================================================
# Thumbnail
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5))
y_pos = range(len(df1))
ax.barh(y_pos, df1["total_miembros"], color=SAGE_DARK, edgecolor=SLATE)
ax.set_yticks(y_pos)
ax.set_yticklabels(df1["ecoaldea"], fontsize=10)
ax.set_xlabel("Miembros")
ax.set_title("Base de datos relacional — Ecoaldeas chilenas", fontweight="bold", fontsize=12)
ax.grid(alpha=0.3, ls="--", axis="x")
ax.invert_yaxis()
fig.tight_layout()
fig.savefig(FIG_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig)
print(f"\n✓ docs/00_thumbnail.png")

conn.close()
print("\n" + "=" * 78)
print("ANÁLISIS SQL COMPLETO ✓")
print("=" * 78)
