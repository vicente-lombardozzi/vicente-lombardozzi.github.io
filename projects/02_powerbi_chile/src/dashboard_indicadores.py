"""
================================================================================
DASHBOARD DE INDICADORES SOCIOECONÓMICOS DE CHILE
================================================================================

Construye un dashboard interactivo con Plotly que replica el tipo de
visualización que se haría en Power BI, usando datos públicos del Banco
Mundial sobre Chile.

Por qué Plotly y no Power BI:
    - Plotly es 100% open source y no requiere licencia
    - El output es HTML interactivo que se puede embeber en GitHub Pages
    - Cualquier reclutador puede verlo sin instalar nada
    - Reproducible: el código genera siempre el mismo dashboard

Para una versión Power BI:
    - El archivo .pbix usaría el mismo CSV (data/chile_indicators.csv)
    - Las medidas DAX equivalentes están en docs/dax_measures.md

Autor: Vicente Lombardozzi
Fecha: 2026
================================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib import rcParams

SAGE = "#6b9075"
SAGE_DARK = "#4f7058"
SAGE_LIGHT = "#a8c4ad"
CREAM = "#faf9f6"
SLATE = "#2c3e35"
ACCENT_RED = "#c97064"
ACCENT_AMBER = "#d4a25e"

HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"
DOCS_DIR = HERE / "docs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 1. Dataset histórico de indicadores Chile (datos reales del Banco Mundial 2000-2023)
# =============================================================================
# Datos extraídos manualmente del World Bank Open Data API
# Variables: PIB, población, esperanza de vida, desempleo, pobreza, CO2

chile_data = pd.DataFrame({
    "year": list(range(2000, 2024)),
    "gdp_billion_usd": [77.9, 70.6, 70.0, 75.6, 99.2, 123.0, 154.7, 173.6, 179.6, 172.4,
                        218.5, 252.0, 267.1, 278.4, 260.6, 243.9, 250.4, 277.4, 295.6, 278.6,
                        252.9, 317.1, 301.0, 335.5],
    "gdp_per_capita_usd": [4960, 4438, 4322, 4621, 6006, 7372, 9162, 10171, 10399, 9874,
                           12358, 14108, 14826, 15324, 14213, 13196, 13413, 14721, 15525,
                           14479, 13027, 16236, 15356, 17015],
    "population_millions": [15.4, 15.6, 15.7, 15.9, 16.1, 16.3, 16.4, 16.6, 16.8, 17.0,
                            17.2, 17.4, 17.5, 17.7, 17.8, 18.0, 18.1, 18.2, 18.4, 18.5,
                            18.6, 18.7, 18.8, 19.0],
    "life_expectancy": [77.0, 77.4, 77.6, 77.7, 77.9, 78.0, 78.2, 78.4, 78.6, 78.7,
                        78.8, 79.0, 79.1, 79.3, 79.4, 79.5, 79.7, 79.8, 80.0, 80.2,
                        78.9, 78.0, 80.0, 80.6],
    "unemployment_pct": [9.2, 9.1, 9.0, 9.5, 10.0, 9.3, 7.8, 7.1, 7.8, 9.7,
                         8.2, 7.1, 6.4, 5.9, 6.4, 6.2, 6.5, 6.7, 7.1, 7.2,
                         10.8, 9.1, 7.9, 8.5],
    "poverty_pct": [24.0, 22.0, 21.5, 19.0, 18.5, 17.0, 13.7, 13.7, 13.7, 11.4,
                    11.4, 11.4, 11.4, 7.8, 7.8, 7.8, 6.4, 6.4, 6.4, 8.6,
                    10.7, 10.5, 6.5, 6.5],
    "co2_per_capita_t": [3.6, 3.4, 3.5, 3.7, 3.9, 4.0, 4.0, 4.4, 4.4, 3.8,
                         4.4, 4.5, 4.6, 4.4, 4.7, 4.6, 4.7, 4.7, 4.7, 4.6,
                         4.0, 4.6, 4.7, 4.5],
})

chile_data.to_csv(DATA_DIR / "chile_indicators_2000_2023.csv", index=False)
print(f"✓ data/chile_indicators_2000_2023.csv ({len(chile_data)} años)")


# =============================================================================
# 2. Datos regionales de Chile (CASEN 2022 — pobreza y desigualdad por región)
# =============================================================================
regiones = pd.DataFrame({
    "region": [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
        "Valparaíso", "Metropolitana", "O'Higgins", "Maule", "Ñuble",
        "Biobío", "La Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"
    ],
    "poverty_pct": [8.4, 8.3, 5.8, 9.2, 8.0, 7.1, 4.5, 7.3, 7.6, 9.5,
                    8.7, 17.4, 11.7, 9.6, 4.4, 2.6],
    "gini": [0.45, 0.47, 0.46, 0.45, 0.46, 0.48, 0.49, 0.45, 0.46, 0.47,
             0.47, 0.49, 0.46, 0.46, 0.42, 0.41],
    "unemployment_pct": [9.1, 8.5, 8.0, 7.8, 8.3, 9.2, 8.5, 6.5, 6.2, 7.1,
                         8.4, 7.5, 5.9, 5.5, 4.8, 3.9],
    "population_thousands": [253, 391, 700, 314, 838, 1900, 8200, 1000, 1100, 510,
                             1700, 1010, 410, 880, 110, 175],
})
regiones.to_csv(DATA_DIR / "chile_regions_2022.csv", index=False)
print(f"✓ data/chile_regions_2022.csv ({len(regiones)} regiones)")


# =============================================================================
# 3. Dashboard interactivo en Plotly
# =============================================================================
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "Evolución del PIB (USD billones)",
        "PIB per cápita (USD)",
        "Esperanza de vida (años)",
        "Desempleo (%)",
        "Pobreza por región (CASEN 2022)",
        "Coeficiente de Gini por región",
    ),
    specs=[
        [{"type": "scatter"}, {"type": "scatter"}],
        [{"type": "scatter"}, {"type": "scatter"}],
        [{"type": "bar"}, {"type": "bar"}],
    ],
    vertical_spacing=0.10,
    horizontal_spacing=0.12,
)

# Fila 1
fig.add_trace(
    go.Scatter(x=chile_data["year"], y=chile_data["gdp_billion_usd"],
               mode="lines+markers", name="PIB", line=dict(color=SAGE_DARK, width=3),
               marker=dict(size=6)),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=chile_data["year"], y=chile_data["gdp_per_capita_usd"],
               mode="lines+markers", name="PIB per cápita",
               line=dict(color=SAGE, width=3), marker=dict(size=6)),
    row=1, col=2
)

# Fila 2
fig.add_trace(
    go.Scatter(x=chile_data["year"], y=chile_data["life_expectancy"],
               mode="lines+markers", name="Esperanza de vida",
               line=dict(color=ACCENT_AMBER, width=3), marker=dict(size=6)),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=chile_data["year"], y=chile_data["unemployment_pct"],
               mode="lines+markers", name="Desempleo",
               line=dict(color=ACCENT_RED, width=3), marker=dict(size=6),
               fill="tozeroy", fillcolor="rgba(201, 112, 100, 0.15)"),
    row=2, col=2
)

# Fila 3
regiones_sorted = regiones.sort_values("poverty_pct", ascending=True)
fig.add_trace(
    go.Bar(y=regiones_sorted["region"], x=regiones_sorted["poverty_pct"],
           orientation="h", marker_color=SAGE, name="Pobreza"),
    row=3, col=1
)

regiones_sorted_gini = regiones.sort_values("gini", ascending=True)
fig.add_trace(
    go.Bar(y=regiones_sorted_gini["region"], x=regiones_sorted_gini["gini"],
           orientation="h", marker_color=SAGE_DARK, name="Gini"),
    row=3, col=2
)

fig.update_layout(
    title=dict(
        text="<b>Dashboard de indicadores socioeconómicos de Chile (2000–2023)</b>",
        font=dict(size=18, color=SLATE),
        x=0.5,
        xanchor="center"
    ),
    showlegend=False,
    height=1100,
    width=1300,
    paper_bgcolor=CREAM,
    plot_bgcolor=CREAM,
    font=dict(family="Manrope, Arial", color=SLATE, size=11),
    margin=dict(t=110, b=60, l=60, r=40),
)

# Estilo de los ejes
for i in range(1, 7):
    fig.update_xaxes(showgrid=True, gridcolor="rgba(107,144,117,0.15)",
                     zeroline=False, row=(i-1)//2 + 1, col=(i-1)%2 + 1)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(107,144,117,0.15)",
                     zeroline=False, row=(i-1)//2 + 1, col=(i-1)%2 + 1)

html_out = DOCS_DIR / "dashboard_chile.html"
fig.write_html(html_out, include_plotlyjs="cdn")
print(f"✓ docs/dashboard_chile.html (interactivo)")

# Versión PNG estática para el thumbnail (necesita kaleido — fallback con matplotlib)
try:
    fig.write_image(DOCS_DIR / "dashboard_chile.png", width=1300, height=1100, scale=2)
    print(f"✓ docs/dashboard_chile.png")
except Exception as e:
    print(f"  (Sin kaleido para PNG, generando con matplotlib)")


# =============================================================================
# 4. Versión matplotlib para thumbnails y previews
# =============================================================================
rcParams["font.family"] = "DejaVu Sans"
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["figure.facecolor"] = CREAM
rcParams["axes.facecolor"] = CREAM
rcParams["savefig.facecolor"] = CREAM

fig2, axes = plt.subplots(2, 2, figsize=(13, 8))

axes[0, 0].plot(chile_data["year"], chile_data["gdp_per_capita_usd"],
                color=SAGE_DARK, lw=2.5, marker="o", ms=4)
axes[0, 0].set_title("PIB per cápita (USD)", fontweight="bold")
axes[0, 0].grid(alpha=0.3, ls="--")

axes[0, 1].plot(chile_data["year"], chile_data["unemployment_pct"],
                color=ACCENT_RED, lw=2.5, marker="o", ms=4)
axes[0, 1].fill_between(chile_data["year"], chile_data["unemployment_pct"],
                         alpha=0.2, color=ACCENT_RED)
axes[0, 1].set_title("Tasa de desempleo (%)", fontweight="bold")
axes[0, 1].grid(alpha=0.3, ls="--")

axes[1, 0].plot(chile_data["year"], chile_data["life_expectancy"],
                color=ACCENT_AMBER, lw=2.5, marker="o", ms=4)
axes[1, 0].set_title("Esperanza de vida (años)", fontweight="bold")
axes[1, 0].grid(alpha=0.3, ls="--")

reg_top = regiones.sort_values("poverty_pct", ascending=True)
axes[1, 1].barh(reg_top["region"], reg_top["poverty_pct"], color=SAGE)
axes[1, 1].set_title("Pobreza por región (CASEN 2022, %)", fontweight="bold")
axes[1, 1].grid(alpha=0.3, ls="--", axis="x")

fig2.suptitle("Indicadores socioeconómicos de Chile", fontweight="bold",
              fontsize=14, y=1.00)
fig2.tight_layout()
fig2.savefig(DOCS_DIR / "01_dashboard_preview.png", bbox_inches="tight", dpi=150)
plt.close(fig2)
print(f"✓ docs/01_dashboard_preview.png")

# Thumbnail
fig3, ax = plt.subplots(figsize=(8, 5))
ax.plot(chile_data["year"], chile_data["gdp_per_capita_usd"],
        color=SAGE_DARK, lw=3, marker="o", ms=5, label="PIB per cápita")
ax2 = ax.twinx()
ax2.plot(chile_data["year"], chile_data["unemployment_pct"],
         color=ACCENT_RED, lw=2.5, ls="--", label="Desempleo (%)")
ax.set_xlabel("Año")
ax.set_ylabel("USD", color=SAGE_DARK)
ax2.set_ylabel("Desempleo (%)", color=ACCENT_RED)
ax.set_title("Dashboard Indicadores Chile (Power BI / Plotly)",
             fontweight="bold", fontsize=13)
ax.grid(alpha=0.3, ls="--")
ax2.spines["top"].set_visible(False)
fig3.tight_layout()
fig3.savefig(DOCS_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig3)
print(f"✓ docs/00_thumbnail.png")

print("\n=== DASHBOARD COMPLETO ===")
