"""
================================================================================
COST-BENEFIT ANALYSIS — Paneles solares Liceo Alfredo Nazar Feres
================================================================================

Re-implementación en Python del análisis costo-beneficio que originalmente
realicé en Excel durante mi MSc en University of Leeds (2019), evaluando la
viabilidad económica de instalar 70 kWp de paneles solares en el Liceo
Técnico Alfredo Nazar Feres (Valparaíso, Chile) bajo el programa
"Techos Solares Públicos" del Ministerio de Energía.

Datos reales del proyecto:
    - 1.200 estudiantes
    - 280 paneles fotovoltaicos de 250 Wp = 70 kWp
    - 805 m² de techo útil
    - Producción anual estimada: 103.110 kWh
    - 35,7 toneladas CO2 reducidas por año
    - 2 propuestas reales de empresas chilenas (Ecoambiente y Ecolife)
    - Vida útil del proyecto: 20 años
    - Tasa de descuento (HM Treasury Green Book 2018): 3,5%
    - Precio CO2 (EEX 2018): USD 17,6/ton

Versión 2026: incluye actualización de parámetros con valores más recientes
y análisis de sensibilidad multivariable.

Autor: Vicente Lombardozzi
Fecha: 2026 (re-análisis del original mayo 2019)
================================================================================
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# -----------------------------------------------------------------------------
# Estética
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
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["figure.facecolor"] = CREAM
rcParams["axes.facecolor"] = CREAM
rcParams["savefig.facecolor"] = CREAM
rcParams["savefig.dpi"] = 150

HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"
FIG_DIR = HERE / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 1. Parámetros del proyecto
# =============================================================================
LIFESPAN = 20             # años
DISCOUNT_RATE = 0.035     # 3.5% (HM Treasury Green Book)
DISCOUNT_RATE_CL = 0.10   # 10% (tasa social Chile, MDS)

# Precio del CO2 (USD por tonelada)
CO2_PRICE_2018 = 17.6     # EEX 2018 (precio original del estudio)
CO2_PRICE_2026 = 85.0     # ETS UE 2026 (~5x el original)

# Parámetros físicos del Liceo
ANNUAL_KWH = 103_110      # producción anual estimada
CO2_REDUCTION_T = 35.7    # toneladas CO2 evitadas / año
ELEC_PRICE_USD = 0.10     # USD / kWh (precio del estudio original)
ELEC_DEGRADATION_Y1 = 0.02  # 2% el primer año
ELEC_DEGRADATION_REST = 0.007  # 0.7% en años siguientes

# Costos de instalación (USD) — datos reales de las dos propuestas
PROPOSAL_1 = {
    "name": "Ecoambiente Ingeniería",
    "detail_engineering": 2_018,
    "pv_modules": 31_907,
    "inverter": 12_610,
    "anchor_structure": 7_350,
    "other_equipment": 9_944,
    "workforce": 11_241,
    "administrative": 2_162,
    "pv_connection": 275,
    "measuring_device": 422,
    "general_5pct": 3_896,
    "utilities": 7_793,
    "iva_19pct": 17_027,
}

PROPOSAL_2 = {
    "name": "Ecolife",
    "detail_engineering": 3_864,
    "pv_modules": 32_723,
    "inverter": 11_113,
    "anchor_structure": 1_203,
    "other_equipment": 1_806,
    "workforce": 4_857,
    "administrative": 1_722,
    "pv_connection": 696,
    "measuring_device": 555,
    "general_5pct": 3_468,
    "utilities": 3_468,
    "iva_19pct": 14_497,
}

# Costos de mantención anual (USD)
MAINTENANCE = {
    "cleaning_distilled_water": 17,
    "six_visits_2h_each": 51,
    "annual_specialist_check": 36,
}

# Costos de reemplazo de capital (USD)
CAPITAL_REPLACEMENT = {
    10: {"inverter": 648},
    6: {"battery": 128},
    12: {"battery": 128},
    18: {"battery": 128},
}


# =============================================================================
# 2. Construcción de los flujos de caja anuales
# =============================================================================
def total_install_cost(proposal):
    return sum(proposal[k] for k in proposal if isinstance(proposal[k], (int, float)))


def annual_electricity_savings():
    """Genera los ahorros de electricidad año a año, considerando degradación."""
    savings = []
    kwh = ANNUAL_KWH
    for year in range(1, LIFESPAN + 1):
        if year == 1:
            kwh *= (1 - ELEC_DEGRADATION_Y1)
        else:
            kwh *= (1 - ELEC_DEGRADATION_REST)
        savings.append(kwh * ELEC_PRICE_USD)
    return savings


def build_cashflow(install_cost, co2_price, discount_rate):
    """
    Construye el flujo de caja descontado a 20 años.
    Devuelve un DataFrame con todas las componentes y el VAN final.
    """
    years = np.arange(0, LIFESPAN + 1)
    rows = []
    elec_savings = [0] + annual_electricity_savings()  # año 0 = inversión

    for y in years:
        # Inversión inicial
        invest = -install_cost if y == 0 else 0

        # Mantención anual
        maint = -sum(MAINTENANCE.values()) if y > 0 else 0

        # Reemplazo de capital
        cap_repl = -sum(CAPITAL_REPLACEMENT.get(y, {}).values())

        # Ahorro electricidad
        elec = elec_savings[y]

        # Beneficio CO2 evitado
        co2_benefit = CO2_REDUCTION_T * co2_price if y > 0 else 0

        net = invest + maint + cap_repl + elec + co2_benefit
        discounted = net / (1 + discount_rate) ** y

        rows.append(
            {
                "year": y,
                "investment": invest,
                "maintenance": maint,
                "capital_replacement": cap_repl,
                "electricity_savings": elec,
                "co2_benefit": co2_benefit,
                "net_flow": net,
                "discounted_flow": discounted,
            }
        )

    df = pd.DataFrame(rows)
    df["cumulative_npv"] = df["discounted_flow"].cumsum()
    return df


# =============================================================================
# 3. Escenario base + escenarios de sensibilidad
# =============================================================================
print("=" * 78)
print("COST-BENEFIT ANALYSIS — Paneles solares Liceo Alfredo Nazar Feres")
print("=" * 78)

cost_p1 = total_install_cost(PROPOSAL_1)
cost_p2 = total_install_cost(PROPOSAL_2)
print(f"\nCosto total instalación Propuesta 1 (Ecoambiente): USD {cost_p1:>10,.0f}")
print(f"Costo total instalación Propuesta 2 (Ecolife)    : USD {cost_p2:>10,.0f}")
print(f"Diferencia                                       : USD {cost_p1-cost_p2:>10,.0f}")

# Escenario BAU = no hacer nada (solo costo de electricidad de la red)
print("\n" + "-" * 78)
print("Escenario base — sin proyecto solar (BAU)")
print("-" * 78)
bau_npv = -ANNUAL_KWH * ELEC_PRICE_USD * sum(
    1 / (1 + DISCOUNT_RATE) ** y for y in range(1, LIFESPAN + 1)
)
print(f"VAN BAU = USD {bau_npv:,.0f}")

# Escenarios principales (precio CO2 2018 - como en el estudio original)
scenarios = {}

scenarios["P1 — Ecoambiente, dr=3.5%"] = build_cashflow(cost_p1, CO2_PRICE_2018, DISCOUNT_RATE)
scenarios["P2 — Ecolife, dr=3.5%"] = build_cashflow(cost_p2, CO2_PRICE_2018, DISCOUNT_RATE)
scenarios["P2 — Ecolife, dr=10% (Chile)"] = build_cashflow(cost_p2, CO2_PRICE_2018, DISCOUNT_RATE_CL)
scenarios["P2 — Ecolife, +20% precio elec"] = build_cashflow(
    cost_p2, CO2_PRICE_2018, DISCOUNT_RATE
)
# Para "+20% precio elec" recalcular con precio modificado
def cashflow_with_elec_change(proposal, co2_price, discount_rate, elec_factor):
    install_cost = total_install_cost(proposal)
    years = np.arange(0, LIFESPAN + 1)
    rows = []
    base_savings = annual_electricity_savings()
    elec_savings = [0] + [s * elec_factor for s in base_savings]
    for y in years:
        invest = -install_cost if y == 0 else 0
        maint = -sum(MAINTENANCE.values()) if y > 0 else 0
        cap_repl = -sum(CAPITAL_REPLACEMENT.get(y, {}).values())
        elec = elec_savings[y]
        co2_benefit = CO2_REDUCTION_T * co2_price if y > 0 else 0
        net = invest + maint + cap_repl + elec + co2_benefit
        discounted = net / (1 + discount_rate) ** y
        rows.append({"year": y, "discounted_flow": discounted, "net_flow": net})
    df = pd.DataFrame(rows)
    df["cumulative_npv"] = df["discounted_flow"].cumsum()
    return df


scenarios["P2 — Ecolife, +20% precio elec"] = cashflow_with_elec_change(
    PROPOSAL_2, CO2_PRICE_2018, DISCOUNT_RATE, 1.20
)
scenarios["P2 — Ecolife, -20% precio elec"] = cashflow_with_elec_change(
    PROPOSAL_2, CO2_PRICE_2018, DISCOUNT_RATE, 0.80
)
scenarios["Peor escenario (P1, +20% elec, dr=10%)"] = cashflow_with_elec_change(
    PROPOSAL_1, CO2_PRICE_2018, DISCOUNT_RATE_CL, 1.20
)

# Escenario actualizado a 2026 (CO2 5x más caro, mismo todo)
scenarios["P2 — actualizado 2026 (CO2 USD 85)"] = build_cashflow(
    cost_p2, CO2_PRICE_2026, DISCOUNT_RATE
)

# -----------------------------------------------------------------------------
# 4. Tabla comparativa de NPV
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("VAN final por escenario (a 20 años)")
print("=" * 78)

summary = []
for name, df in scenarios.items():
    npv = df["discounted_flow"].sum()
    summary.append({"Escenario": name, "NPV (USD)": npv})

summary_df = pd.DataFrame(summary)
summary_df["NPV (USD)"] = summary_df["NPV (USD)"].round(0)
print(summary_df.to_string(index=False))

summary_df.to_csv(DATA_DIR / "npv_summary.csv", index=False)
print(f"\n✓ data/npv_summary.csv")

# Guardar el flujo detallado del escenario base
scenarios["P2 — Ecolife, dr=3.5%"].to_csv(
    DATA_DIR / "cashflow_p2_base.csv", index=False
)
print(f"✓ data/cashflow_p2_base.csv")


# -----------------------------------------------------------------------------
# 5. Visualización de los flujos de caja acumulados
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6))

palette = [SAGE_DARK, SAGE, ACCENT_AMBER, ACCENT_RED, "#888"]
to_plot = [
    "P2 — Ecolife, dr=3.5%",
    "P1 — Ecoambiente, dr=3.5%",
    "P2 — Ecolife, +20% precio elec",
    "P2 — Ecolife, -20% precio elec",
    "Peor escenario (P1, +20% elec, dr=10%)",
]

for name, color in zip(to_plot, palette):
    df = scenarios[name]
    ax.plot(
        df["year"],
        df["cumulative_npv"],
        lw=2.5,
        marker="o",
        ms=4,
        color=color,
        label=name,
    )

ax.axhline(0, color=SLATE, lw=1, ls="--", alpha=0.6)
ax.set_title(
    "VAN acumulado a 20 años — Liceo Alfredo Nazar Feres (Valparaíso)",
    fontweight="bold",
    fontsize=13,
)
ax.set_xlabel("Año del proyecto")
ax.set_ylabel("VAN acumulado (USD)")
ax.legend(loc="lower right", frameon=True, fontsize=9)
ax.grid(alpha=0.3, ls="--")

fig.tight_layout()
fig.savefig(FIG_DIR / "01_npv_scenarios.png", bbox_inches="tight")
plt.close(fig)
print(f"✓ figures/01_npv_scenarios.png")


# -----------------------------------------------------------------------------
# 6. Comparación 2019 vs 2026 (impacto del nuevo precio del CO2)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5))

df_2019 = scenarios["P2 — Ecolife, dr=3.5%"]
df_2026 = scenarios["P2 — actualizado 2026 (CO2 USD 85)"]

ax.plot(
    df_2019["year"], df_2019["cumulative_npv"], lw=3, color=SAGE,
    marker="o", ms=4, label="2019 — CO₂ a USD 17,6/ton"
)
ax.plot(
    df_2026["year"], df_2026["cumulative_npv"], lw=3, color=SAGE_DARK,
    marker="o", ms=4, label="2026 — CO₂ a USD 85/ton"
)
ax.axhline(0, color=SLATE, lw=1, ls="--", alpha=0.6)
ax.fill_between(
    df_2019["year"], df_2019["cumulative_npv"], df_2026["cumulative_npv"],
    alpha=0.18, color=SAGE_DARK, label="Beneficio adicional por mayor precio CO₂"
)

ax.set_title(
    "Impacto del nuevo precio del CO₂ en el VAN — Liceo Alfredo Nazar (Propuesta 2)",
    fontweight="bold", fontsize=12
)
ax.set_xlabel("Año del proyecto")
ax.set_ylabel("VAN acumulado (USD)")
ax.legend(loc="lower right", frameon=True)
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(FIG_DIR / "02_2019_vs_2026.png", bbox_inches="tight")
plt.close(fig)
print(f"✓ figures/02_2019_vs_2026.png")


# -----------------------------------------------------------------------------
# 7. Análisis de sensibilidad (tornado chart)
# -----------------------------------------------------------------------------
def npv_for_params(install_cost, co2_price, dr, elec_factor):
    return cashflow_with_elec_change(
        PROPOSAL_2 if install_cost == cost_p2 else PROPOSAL_1,
        co2_price, dr, elec_factor
    )["discounted_flow"].sum()


base_npv = npv_for_params(cost_p2, CO2_PRICE_2018, DISCOUNT_RATE, 1.0)

sensitivity = []
sensitivity.append({"variable": "Tasa de descuento 10% (Chile)", "low": npv_for_params(cost_p2, CO2_PRICE_2018, 0.10, 1.0), "high": base_npv})
sensitivity.append({"variable": "Precio elec −20%", "low": npv_for_params(cost_p2, CO2_PRICE_2018, DISCOUNT_RATE, 0.8), "high": base_npv})
sensitivity.append({"variable": "Precio elec +20%", "low": base_npv, "high": npv_for_params(cost_p2, CO2_PRICE_2018, DISCOUNT_RATE, 1.2)})
sensitivity.append({"variable": "Costo P1 (más caro)", "low": npv_for_params(cost_p1, CO2_PRICE_2018, DISCOUNT_RATE, 1.0), "high": base_npv})
sensitivity.append({"variable": "CO2 a USD 85 (2026)", "low": base_npv, "high": npv_for_params(cost_p2, CO2_PRICE_2026, DISCOUNT_RATE, 1.0)})

sens_df = pd.DataFrame(sensitivity)
sens_df["range"] = (sens_df["high"] - sens_df["low"]).abs()
sens_df = sens_df.sort_values("range", ascending=True)

fig, ax = plt.subplots(figsize=(10, 5.5))
y_pos = np.arange(len(sens_df))
ax.barh(
    y_pos, sens_df["high"] - sens_df["low"], left=sens_df["low"],
    color=SAGE, edgecolor=SLATE, linewidth=0.8
)
ax.axvline(base_npv, color=ACCENT_RED, lw=2, ls="--", label=f"VAN base: USD {base_npv:,.0f}")
ax.set_yticks(y_pos)
ax.set_yticklabels(sens_df["variable"])
ax.set_xlabel("VAN (USD)")
ax.set_title(
    "Análisis de sensibilidad — VAN del proyecto solar",
    fontweight="bold", fontsize=12
)
ax.legend(loc="lower right", frameon=True)
ax.grid(alpha=0.3, ls="--", axis="x")
fig.tight_layout()
fig.savefig(FIG_DIR / "03_sensitivity.png", bbox_inches="tight")
plt.close(fig)
print(f"✓ figures/03_sensitivity.png")


# -----------------------------------------------------------------------------
# 8. Thumbnail
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
df = scenarios["P2 — Ecolife, dr=3.5%"]
ax.fill_between(df["year"], df["cumulative_npv"], 0, where=df["cumulative_npv"] >= 0,
                color=SAGE, alpha=0.3, interpolate=True)
ax.fill_between(df["year"], df["cumulative_npv"], 0, where=df["cumulative_npv"] < 0,
                color=ACCENT_RED, alpha=0.3, interpolate=True)
ax.plot(df["year"], df["cumulative_npv"], color=SAGE_DARK, lw=3, marker="o", ms=5)
ax.axhline(0, color=SLATE, lw=1)
ax.set_title("CBA Paneles Solares — Liceo Alfredo Nazar", fontweight="bold", fontsize=13)
ax.set_xlabel("Año")
ax.set_ylabel("VAN acumulado (USD)")
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(FIG_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig)
print(f"✓ figures/00_thumbnail.png")

print("\n" + "=" * 78)
print("CBA COMPLETO ✓")
print("=" * 78)
