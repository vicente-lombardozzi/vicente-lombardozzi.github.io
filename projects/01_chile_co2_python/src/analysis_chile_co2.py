"""
================================================================================
EMISIONES DE CO2 EN CHILE: Re-análisis del trabajo MSc Leeds 2019
================================================================================

Este script re-implementa en Python el análisis cuantitativo de emisiones
de CO2 que originalmente realicé en Matlab durante mi MSc in Ecological
Economics en University of Leeds (2019).

Metodologías reproducidas:
    1. Análisis KAYA (descomposición de emisiones)
    2. Modelo STIRPAT (regresión multivariable)
    3. Coeficientes de Gini globales
    4. Proyecciones BAU y escenario sostenible

Autor: Vicente Lombardozzi
Fecha: 2026
Datos originales: Chile.mat (1990-2013, MSc Leeds dataset)
                  CC02.mat (90 países, año 2002)
================================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
import scipy.io
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rcParams

# -----------------------------------------------------------------------------
# Configuración estética (paleta sage del portafolio)
# -----------------------------------------------------------------------------
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
rcParams["axes.labelcolor"] = SLATE
rcParams["xtick.color"] = SLATE
rcParams["ytick.color"] = SLATE
rcParams["axes.titlecolor"] = SLATE
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["figure.facecolor"] = CREAM
rcParams["axes.facecolor"] = CREAM
rcParams["savefig.facecolor"] = CREAM
rcParams["savefig.edgecolor"] = "none"
rcParams["savefig.dpi"] = 150

# -----------------------------------------------------------------------------
# Rutas
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"
FIG_DIR = HERE / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Carga del dataset original Chile.mat
# -----------------------------------------------------------------------------
print("=" * 78)
print("1. Cargando dataset Chile.mat (MSc Leeds 2019)")
print("=" * 78)

mat = scipy.io.loadmat(DATA_DIR / "Chile.mat")

years = mat["yrs"].flatten()
pop = mat["pop_UN"].flatten()
co2_terr = mat["CO2_terr_GCB"].flatten()
co2_cons = mat["CO2_cons_GCB"].flatten()
gdp_ppp = mat["GDP_PPP_WB"].flatten()
gdp_real = mat["GDP_real_WB"].flatten()
energy = mat["primary_energy_IEA"].flatten().astype(float)
life_exp = mat["life_expectancy_WB"].flatten()

chile = pd.DataFrame(
    {
        "year": years.astype(int),
        "population": pop,
        "co2_terr_t": co2_terr,
        "co2_cons_t": co2_cons,
        "gdp_ppp_2011usd": gdp_ppp,
        "gdp_real_2010usd": gdp_real,
        "primary_energy_gj": energy,
        "life_expectancy": life_exp,
    }
)

print(f"   Periodo cubierto : {chile['year'].min()}–{chile['year'].max()}")
print(f"   Observaciones    : {len(chile)} años")
print(f"   Población inicial: {chile['population'].iloc[0] / 1e6:.2f} M")
print(f"   Población final  : {chile['population'].iloc[-1] / 1e6:.2f} M")
print(f"   CO2 territorial inicial: {chile['co2_terr_t'].iloc[0] / 1e6:.1f} MtCO2")
print(f"   CO2 territorial final  : {chile['co2_terr_t'].iloc[-1] / 1e6:.1f} MtCO2")

# Guardar dataset limpio en CSV (para reproducibilidad)
chile.to_csv(DATA_DIR / "chile_1990_2013.csv", index=False)
print(f"\n   ✓ Dataset limpio guardado en data/chile_1990_2013.csv")


# -----------------------------------------------------------------------------
# 2. Descomposición KAYA
#
#    Identidad: CO2 = Pob × (PIB/Pob) × (Energía/PIB) × (CO2/Energía)
#
#    Donde:
#       Pob               = población
#       PIB/Pob           = afluencia (riqueza per cápita)
#       Energía/PIB       = intensidad energética
#       CO2/Energía       = huella de carbono de la energía
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("2. Descomposición KAYA (Pob × Afluencia × Intensidad × Huella)")
print("=" * 78)

chile["affluence"] = chile["gdp_ppp_2011usd"] / chile["population"]
chile["energy_intensity"] = chile["primary_energy_gj"] / chile["gdp_ppp_2011usd"]
chile["carbon_footprint"] = chile["co2_terr_t"] / chile["primary_energy_gj"]

# Verificación de la identidad KAYA: el producto debe reproducir CO2_terr
chile["kaya_check"] = (
    chile["population"]
    * chile["affluence"]
    * chile["energy_intensity"]
    * chile["carbon_footprint"]
)
max_err = (chile["kaya_check"] - chile["co2_terr_t"]).abs().max()
print(f"   Identidad KAYA verificada (error máximo: {max_err:.2e} tCO2)")

# Tasas de crecimiento anuales compuestas
def cagr(series):
    """Compound Annual Growth Rate."""
    n = len(series) - 1
    return (series.iloc[-1] / series.iloc[0]) ** (1 / n) - 1


growth = {
    "Población": cagr(chile["population"]),
    "Afluencia (PIB/Pob)": cagr(chile["affluence"]),
    "Intensidad energética (E/PIB)": cagr(chile["energy_intensity"]),
    "Huella de carbono (CO2/E)": cagr(chile["carbon_footprint"]),
    "CO2 territorial (resultado)": cagr(chile["co2_terr_t"]),
}
print("\n   Tasas de crecimiento anuales compuestas (1990–2013):")
for k, v in growth.items():
    print(f"     {k:35s}: {v*100:+6.2f} %")

# Guardar el dataframe con descomposición
chile.to_csv(DATA_DIR / "chile_kaya_decomposition.csv", index=False)


# -----------------------------------------------------------------------------
# 3. Visualización: trayectoria histórica de emisiones y factores KAYA
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("3. Generando figuras (trayectoria histórica)")
print("=" * 78)

fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))

# (A) Emisiones totales
axes[0, 0].plot(
    chile["year"], chile["co2_terr_t"] / 1e6, color=SAGE_DARK, lw=2.5, marker="o", ms=4
)
axes[0, 0].fill_between(
    chile["year"], chile["co2_terr_t"] / 1e6, alpha=0.15, color=SAGE
)
axes[0, 0].set_title("Emisiones territoriales de CO₂", fontweight="bold")
axes[0, 0].set_ylabel("MtCO₂ / año")
axes[0, 0].set_xlabel("")
axes[0, 0].grid(alpha=0.3, ls="--")

# (B) Afluencia (PIB per cápita PPP)
axes[0, 1].plot(
    chile["year"],
    chile["affluence"],
    color=ACCENT_AMBER,
    lw=2.5,
    marker="o",
    ms=4,
)
axes[0, 1].set_title("Afluencia (PIB PPP per cápita)", fontweight="bold")
axes[0, 1].set_ylabel("USD constantes 2011")
axes[0, 1].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
axes[0, 1].grid(alpha=0.3, ls="--")

# (C) Intensidad energética (energía/PIB)
axes[1, 0].plot(
    chile["year"],
    chile["energy_intensity"] * 1e9,
    color=ACCENT_RED,
    lw=2.5,
    marker="o",
    ms=4,
)
axes[1, 0].set_title("Intensidad energética (Energía / PIB)", fontweight="bold")
axes[1, 0].set_ylabel("GJ por miles de USD")
axes[1, 0].grid(alpha=0.3, ls="--")

# (D) Huella de carbono de la energía (CO2/Energía)
axes[1, 1].plot(
    chile["year"],
    chile["carbon_footprint"] * 1e9,
    color=SAGE,
    lw=2.5,
    marker="o",
    ms=4,
)
axes[1, 1].set_title("Huella de carbono de la energía (CO₂ / Energía)", fontweight="bold")
axes[1, 1].set_ylabel("tCO₂ por GJ")
axes[1, 1].grid(alpha=0.3, ls="--")

fig.suptitle(
    "Chile: descomposición KAYA de las emisiones de CO₂ (1990–2013)",
    fontweight="bold",
    fontsize=13,
    color=SLATE,
)
fig.tight_layout()
fig.savefig(FIG_DIR / "01_kaya_decomposition.png", bbox_inches="tight")
plt.close(fig)
print(f"   ✓ figures/01_kaya_decomposition.png")


# -----------------------------------------------------------------------------
# 4. Proyecciones a 2050: BAU vs. escenario sostenible
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("4. Proyecciones a 2050 (BAU y escenario sostenible)")
print("=" * 78)

LAST_YEAR = int(chile["year"].iloc[-1])
PROJ_YEARS = np.arange(LAST_YEAR, 2051)
n_proj = len(PROJ_YEARS)

# --- Escenario Business-as-Usual ---
g_pop = growth["Población"]
g_affl = growth["Afluencia (PIB/Pob)"]
g_eint = growth["Intensidad energética (E/PIB)"]
g_cfoot = growth["Huella de carbono (CO2/E)"]


def project(start_value, rate, n):
    return start_value * np.power(1 + rate, np.arange(n))


bau = pd.DataFrame({"year": PROJ_YEARS})
bau["population"] = project(chile["population"].iloc[-1], g_pop, n_proj)
bau["affluence"] = project(chile["affluence"].iloc[-1], g_affl, n_proj)
bau["energy_intensity"] = project(chile["energy_intensity"].iloc[-1], g_eint, n_proj)
bau["carbon_footprint"] = project(chile["carbon_footprint"].iloc[-1], g_cfoot, n_proj)
bau["co2_terr_t"] = (
    bau["population"]
    * bau["affluence"]
    * bau["energy_intensity"]
    * bau["carbon_footprint"]
)

# --- Escenario sostenible (alineado a NDC chilena: -30% sobre 2007) ---
# Tasa de descenso anual estimada para llegar a la NDC en 2030
# NDC: 30% menos emisiones por unidad de PIB para 2030 vs. 2007
co2_2007 = chile.loc[chile["year"] == 2007, "co2_terr_t"].iloc[0]
ndc_target_2030 = co2_2007 * 0.70

# Calculamos la tasa anual necesaria para descender desde 2013 hasta NDC 2030
n_to_2030 = 2030 - LAST_YEAR
target_decline_2030 = (ndc_target_2030 / chile["co2_terr_t"].iloc[-1]) ** (
    1 / n_to_2030
) - 1

# Asumimos que la mayor parte del esfuerzo va a la huella de carbono y la intensidad energética
# Mantenemos crecimiento de población y afluencia (más realistas)
g_eint_sust = g_eint - 0.025  # eficiencia energética acelerada
g_cfoot_sust = g_cfoot - 0.025  # descarbonización acelerada

sust = pd.DataFrame({"year": PROJ_YEARS})
sust["population"] = project(chile["population"].iloc[-1], g_pop, n_proj)
sust["affluence"] = project(chile["affluence"].iloc[-1], g_affl, n_proj)
sust["energy_intensity"] = project(
    chile["energy_intensity"].iloc[-1], g_eint_sust, n_proj
)
sust["carbon_footprint"] = project(
    chile["carbon_footprint"].iloc[-1], g_cfoot_sust, n_proj
)
sust["co2_terr_t"] = (
    sust["population"]
    * sust["affluence"]
    * sust["energy_intensity"]
    * sust["carbon_footprint"]
)

# Combinar histórico + proyecciones para visualizar
historical = chile[["year", "co2_terr_t"]].copy()
historical["scenario"] = "Histórico (1990–2013)"
bau_plot = bau[["year", "co2_terr_t"]].copy()
bau_plot["scenario"] = "BAU (proyección)"
sust_plot = sust[["year", "co2_terr_t"]].copy()
sust_plot["scenario"] = "Sostenible (proyección)"

print(f"\n   CO2 proyectado a 2030 — BAU       : {bau.loc[bau['year']==2030, 'co2_terr_t'].iloc[0]/1e6:.1f} MtCO2")
print(f"   CO2 proyectado a 2030 — Sostenible: {sust.loc[sust['year']==2030, 'co2_terr_t'].iloc[0]/1e6:.1f} MtCO2")
print(f"   Meta NDC Chile (2030)             : {ndc_target_2030/1e6:.1f} MtCO2")

# Figura 2: proyecciones
fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(
    historical["year"],
    historical["co2_terr_t"] / 1e6,
    color=SLATE,
    lw=2.5,
    marker="o",
    ms=5,
    label="Histórico (datos reales 1990–2013)",
)
ax.plot(
    bau_plot["year"],
    bau_plot["co2_terr_t"] / 1e6,
    color=ACCENT_RED,
    lw=2.5,
    ls="--",
    label="Business-as-Usual",
)
ax.plot(
    sust_plot["year"],
    sust_plot["co2_terr_t"] / 1e6,
    color=SAGE_DARK,
    lw=2.5,
    label="Transición a sostenibilidad",
)
ax.axhline(
    ndc_target_2030 / 1e6,
    color=ACCENT_AMBER,
    ls=":",
    lw=2,
    label=f"Meta NDC Chile 2030 ({ndc_target_2030/1e6:.0f} MtCO₂)",
)
ax.axvline(2030, color="grey", lw=0.8, alpha=0.5)
ax.text(2030.3, ax.get_ylim()[1] * 0.95, "2030", color="grey", fontsize=9)

ax.set_title(
    "Chile: trayectoria de emisiones de CO₂ y dos escenarios al 2050",
    fontweight="bold",
    fontsize=13,
)
ax.set_xlabel("Año")
ax.set_ylabel("Emisiones territoriales de CO₂ (MtCO₂)")
ax.legend(loc="upper left", frameon=True, framealpha=0.92)
ax.grid(alpha=0.3, ls="--")

fig.tight_layout()
fig.savefig(FIG_DIR / "02_projections_2050.png", bbox_inches="tight")
plt.close(fig)
print(f"\n   ✓ figures/02_projections_2050.png")


# -----------------------------------------------------------------------------
# 5. Análisis STIRPAT cross-country (90 países, año 2002)
#
#    Modelo log-log:
#       ln(CO2) = β0 + β1·ln(Pob) + β2·ln(PIB/Pob) + β3·ln(Energía) + ε
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("5. Análisis STIRPAT (90 países, año 2002)")
print("=" * 78)

cc = scipy.io.loadmat(DATA_DIR / "CC02.mat")
countries_raw = cc["countries"]
countries = [str(x[0][0]) for x in countries_raw]
co2_terr_cc = cc["co2_terr"].flatten()
co2_cons_cc = cc["co2_cons"].flatten()
gdp_ppp_cc = cc["gdp_ppp"].flatten()
fec_cc = cc["fec"].flatten()
land_cc = cc["land"].flatten()
mat_cons_cc = cc["mat_cons"].flatten()

cross = pd.DataFrame(
    {
        "country": countries,
        "co2_terr": co2_terr_cc,
        "co2_cons": co2_cons_cc,
        "gdp_ppp": gdp_ppp_cc,
        "final_energy_cons": fec_cc,
        "land_km2": land_cc,
        "material_cons": mat_cons_cc,
    }
)
cross = cross[(cross["co2_terr"] > 0) & (cross["gdp_ppp"] > 0) & (cross["final_energy_cons"] > 0)]

# Aproximación: para STIRPAT necesitamos población; usamos CO2 per cápita ≈ derivada
# Aquí usamos PIB total como proxy de "afluencia" sin separar pob para consistencia con
# el dataset. El modelo original también usaba versiones con/sin población.
log_co2 = np.log(cross["co2_terr"])
log_gdp = np.log(cross["gdp_ppp"])
log_energy = np.log(cross["final_energy_cons"])

X = pd.DataFrame({"const": 1.0, "ln_GDP_PPP": log_gdp, "ln_Energy": log_energy})
y = log_co2
model = sm.OLS(y, X).fit()
print("\n", model.summary().as_text())

# Guardar tabla de coeficientes
coef_table = pd.DataFrame(
    {
        "coef": model.params,
        "std_err": model.bse,
        "t": model.tvalues,
        "p>|t|": model.pvalues,
        "ci_low": model.conf_int()[0],
        "ci_high": model.conf_int()[1],
    }
)
coef_table.to_csv(DATA_DIR / "stirpat_coefficients.csv")
print(f"\n   ✓ data/stirpat_coefficients.csv")

# Figura 3: scatter ln(GDP) vs ln(CO2) con línea de regresión
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(log_gdp, log_co2, color=SAGE, s=60, alpha=0.65, edgecolor=SAGE_DARK, linewidth=0.7)

x_line = np.linspace(log_gdp.min(), log_gdp.max(), 100)
# Línea sólo de la regresión bivariada para visualización
slope = np.polyfit(log_gdp, log_co2, 1)
ax.plot(x_line, np.polyval(slope, x_line), color=ACCENT_RED, lw=2.5, label=f"Tendencia: pendiente = {slope[0]:.2f}")

ax.set_title(
    f"STIRPAT: relación entre PIB PPP y emisiones territoriales\n"
    f"(N = {len(cross)} países, año 2002, escala logarítmica)",
    fontweight="bold",
    fontsize=12,
)
ax.set_xlabel("ln(PIB PPP, USD)")
ax.set_ylabel("ln(CO₂ territorial, tCO₂)")
ax.legend(loc="upper left", frameon=True)
ax.grid(alpha=0.3, ls="--")

fig.tight_layout()
fig.savefig(FIG_DIR / "03_stirpat_scatter.png", bbox_inches="tight")
plt.close(fig)
print(f"   ✓ figures/03_stirpat_scatter.png")


# -----------------------------------------------------------------------------
# 6. Coeficientes de Gini globales (desigualdad en consumo de recursos)
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("6. Coeficientes de Gini globales (90 países)")
print("=" * 78)


def gini(arr):
    """Coeficiente de Gini sobre un array no negativo."""
    arr = np.sort(np.array(arr, dtype=float))
    arr = arr[arr >= 0]
    n = len(arr)
    if n == 0 or arr.sum() == 0:
        return np.nan
    cum = np.cumsum(arr)
    return (n + 1 - 2 * (cum.sum() / arr[-1] / n)) / n if False else (
        (2 * np.sum((np.arange(1, n + 1)) * arr)) / (n * arr.sum())
    ) - (n + 1) / n


gini_results = {
    "PIB PPP": gini(cross["gdp_ppp"]),
    "CO₂ territorial": gini(cross["co2_terr"]),
    "CO₂ consumo": gini(cross["co2_cons"]),
    "Energía final": gini(cross["final_energy_cons"]),
    "Material (consumo)": gini(cross["material_cons"].dropna() if cross["material_cons"].notna().any() else cross["material_cons"]),
}

print("\n   Coeficientes de Gini (0 = igualdad, 1 = desigualdad máxima):")
for k, v in gini_results.items():
    print(f"     {k:25s}: {v:.3f}")

gini_df = pd.DataFrame(
    {"variable": list(gini_results.keys()), "gini": list(gini_results.values())}
)
gini_df.to_csv(DATA_DIR / "gini_coefficients.csv", index=False)

# Figura 4: gráfico de barras de coeficientes Gini
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(
    gini_df["variable"],
    gini_df["gini"],
    color=[SAGE, SAGE_DARK, SAGE, ACCENT_AMBER, ACCENT_RED][: len(gini_df)],
    edgecolor=SLATE,
    linewidth=0.8,
)
for bar, value in zip(bars, gini_df["gini"]):
    ax.text(
        value + 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}",
        va="center",
        fontweight="bold",
        color=SLATE,
    )

ax.set_xlim(0, 1)
ax.set_xlabel("Coeficiente de Gini")
ax.set_title(
    "Desigualdad global en distribución de recursos y emisiones (90 países, 2002)",
    fontweight="bold",
    fontsize=12,
)
ax.grid(alpha=0.3, ls="--", axis="x")
ax.invert_yaxis()

fig.tight_layout()
fig.savefig(FIG_DIR / "04_gini_global.png", bbox_inches="tight")
plt.close(fig)
print(f"\n   ✓ figures/04_gini_global.png")


# -----------------------------------------------------------------------------
# 7. Figura resumen / thumbnail del proyecto
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("7. Generando thumbnail para el portafolio")
print("=" * 78)

fig, ax = plt.subplots(figsize=(8, 5))
ax.fill_between(
    historical["year"],
    historical["co2_terr_t"] / 1e6,
    alpha=0.25,
    color=SAGE,
)
ax.plot(
    historical["year"],
    historical["co2_terr_t"] / 1e6,
    color=SAGE_DARK,
    lw=3,
    marker="o",
    ms=5,
    label="Histórico",
)
ax.plot(
    bau_plot["year"],
    bau_plot["co2_terr_t"] / 1e6,
    color=ACCENT_RED,
    lw=2.5,
    ls="--",
    label="BAU",
)
ax.plot(
    sust_plot["year"],
    sust_plot["co2_terr_t"] / 1e6,
    color=SAGE_DARK,
    lw=2.5,
    label="Sostenible",
)
ax.set_title("Chile: emisiones de CO₂ y proyecciones a 2050", fontweight="bold", fontsize=13)
ax.set_xlabel("Año")
ax.set_ylabel("MtCO₂")
ax.legend(loc="upper left", frameon=True)
ax.grid(alpha=0.3, ls="--")

fig.tight_layout()
fig.savefig(FIG_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig)
print(f"   ✓ figures/00_thumbnail.png")

print("\n" + "=" * 78)
print("ANÁLISIS COMPLETO ✓")
print("=" * 78)
