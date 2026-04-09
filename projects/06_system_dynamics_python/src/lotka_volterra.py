"""
================================================================================
SYSTEM DYNAMICS — Modelos portados de Vensim a Python
================================================================================

Re-implementación en Python (scipy.integrate) de modelos de dinámica de
sistemas que originalmente construí en Vensim durante mi MSc en Economía
Ecológica (University of Leeds, 2019), Assignment 2 del curso "Tools and
Techniques in Ecological Economics".

Modelos incluidos:
    1. Lotka-Volterra (depredador-presa) — base ecológica
    2. Modelo savings-income (acumulación de capital)
    3. Modelo extendido de stock-flow para recursos renovables

Por qué Python en lugar de Vensim:
    - Vensim es software cerrado y de pago. Python es abierto y reproducible.
    - Los notebooks Jupyter pueden ejecutarse en cualquier computadora.
    - Permite versionar y compartir los modelos en repositorios públicos.
    - scipy.integrate.odeint resuelve EDOs con la misma precisión.

Autor: Vicente Lombardozzi
Fecha: 2026 (port del original 2019)
================================================================================
"""

from pathlib import Path
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Estética
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
FIG_DIR = HERE / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 1. MODELO LOTKA-VOLTERRA (depredador-presa)
#
#    dx/dt = α·x − β·x·y       (presas)
#    dy/dt = δ·x·y − γ·y       (depredadores)
#
#    α: tasa de natalidad de presas (en ausencia de depredadores)
#    β: tasa de depredación
#    δ: eficiencia de conversión de presas a depredadores
#    γ: tasa de mortalidad de depredadores
# =============================================================================
print("=" * 78)
print("1. MODELO LOTKA-VOLTERRA (port de Vensim → Python)")
print("=" * 78)


def lotka_volterra(state, t, alpha, beta, delta, gamma):
    x, y = state
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]


# Parámetros del modelo original (mismos que en Vensim 2019)
alpha = 1.0   # natalidad de presas
beta = 0.1    # tasa de depredación
delta = 0.075 # eficiencia conversión
gamma = 1.5   # mortalidad depredadores

# Condiciones iniciales
x0 = 10  # presas iniciales
y0 = 5   # depredadores iniciales

# Integración temporal
t = np.linspace(0, 50, 5_001)
sol = odeint(lotka_volterra, [x0, y0], t, args=(alpha, beta, delta, gamma))

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# (a) Series temporales
axes[0].plot(t, sol[:, 0], lw=2.5, color=SAGE_DARK, label="Presas (x)")
axes[0].plot(t, sol[:, 1], lw=2.5, color=ACCENT_RED, label="Depredadores (y)")
axes[0].set_title("Lotka-Volterra: oscilaciones temporales", fontweight="bold")
axes[0].set_xlabel("Tiempo")
axes[0].set_ylabel("Población")
axes[0].legend(loc="upper right", frameon=True)
axes[0].grid(alpha=0.3, ls="--")

# (b) Plano de fase
axes[1].plot(sol[:, 0], sol[:, 1], lw=1.5, color=SAGE)
axes[1].scatter([x0], [y0], color=ACCENT_AMBER, s=80, zorder=10, label="Estado inicial")
axes[1].set_title("Lotka-Volterra: plano de fase", fontweight="bold")
axes[1].set_xlabel("Presas")
axes[1].set_ylabel("Depredadores")
axes[1].legend(loc="upper right", frameon=True)
axes[1].grid(alpha=0.3, ls="--")

fig.tight_layout()
fig.savefig(FIG_DIR / "01_lotka_volterra.png", bbox_inches="tight")
plt.close(fig)
print(f"   ✓ figures/01_lotka_volterra.png")
print(f"   Parámetros: α={alpha}, β={beta}, δ={delta}, γ={gamma}")
print(f"   Período aprox.: {2*np.pi/np.sqrt(alpha*gamma):.2f} unidades de tiempo")


# =============================================================================
# 2. MODELO SAVINGS-INCOME (acumulación de capital simple)
#
#    Un modelo de stock-flow:
#       dS/dt = sY − dS    (S = stock de capital, Y = ingreso)
#       Y = aS             (la producción es función del capital)
#
#    s: tasa de ahorro
#    d: tasa de depreciación
#    a: productividad marginal del capital
# =============================================================================
print("\n" + "=" * 78)
print("2. MODELO SAVINGS-INCOME (acumulación de capital)")
print("=" * 78)


def savings_income(state, t, savings_rate, depreciation, productivity):
    K = state[0]  # stock de capital
    Y = productivity * K  # ingreso
    dKdt = savings_rate * Y - depreciation * K
    return [dKdt]


savings_rate = 0.20      # ahorra 20% del ingreso
depreciation = 0.05      # 5% depreciación anual
productivity = 0.40      # productividad del capital
K0 = 100                 # capital inicial
t2 = np.linspace(0, 60, 601)

sol2 = odeint(savings_income, [K0], t2, args=(savings_rate, depreciation, productivity))
income = productivity * sol2[:, 0]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(t2, sol2[:, 0], lw=2.5, color=SAGE_DARK, label="Stock de capital (K)")
ax.plot(t2, income, lw=2.5, color=ACCENT_AMBER, label="Ingreso anual (Y = aK)")
ax.set_title(
    "Modelo Savings-Income — acumulación dinámica de capital",
    fontweight="bold", fontsize=12
)
ax.set_xlabel("Año")
ax.set_ylabel("Unidades monetarias")
ax.legend(loc="upper left", frameon=True)
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(FIG_DIR / "02_savings_income.png", bbox_inches="tight")
plt.close(fig)
print(f"   ✓ figures/02_savings_income.png")
print(f"   Equilibrio: K* = {K0 * savings_rate * productivity / depreciation:.0f} (cuando dK/dt=0)")


# =============================================================================
# 3. MODELO STOCK-FLOW DE RECURSO RENOVABLE (extensión)
#
#    Un recurso renovable bajo extracción humana:
#       dR/dt = g·R·(1 − R/K) − h·R
#
#    R: stock del recurso (e.g., bosque, pesquería)
#    g: tasa intrínseca de crecimiento
#    K: capacidad de carga
#    h: tasa de extracción humana
# =============================================================================
print("\n" + "=" * 78)
print("3. MODELO RECURSO RENOVABLE (logístico con extracción)")
print("=" * 78)


def renewable_resource(state, t, g, K, h):
    R = state[0]
    dRdt = g * R * (1 - R / K) - h * R
    return [dRdt]


# Comparación de 3 escenarios de extracción
scenarios = {
    "Extracción sostenible (h=0.10)": 0.10,
    "Extracción intermedia (h=0.20)": 0.20,
    "Extracción excesiva (h=0.35)": 0.35,
}
g, K, R0 = 0.30, 1000, 800
t3 = np.linspace(0, 100, 1001)

fig, ax = plt.subplots(figsize=(10, 5.5))
colors = [SAGE_DARK, ACCENT_AMBER, ACCENT_RED]

for (name, h), color in zip(scenarios.items(), colors):
    sol3 = odeint(renewable_resource, [R0], t3, args=(g, K, h))
    ax.plot(t3, sol3[:, 0], lw=2.5, color=color, label=f"{name}")

ax.axhline(K, color=SLATE, ls="--", lw=1, alpha=0.5, label="Capacidad de carga (K)")
ax.set_title(
    "Modelo de recurso renovable bajo distintas tasas de extracción",
    fontweight="bold", fontsize=12
)
ax.set_xlabel("Tiempo (años)")
ax.set_ylabel("Stock del recurso")
ax.legend(loc="lower right", frameon=True)
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(FIG_DIR / "03_renewable_resource.png", bbox_inches="tight")
plt.close(fig)
print(f"   ✓ figures/03_renewable_resource.png")


# =============================================================================
# 4. Thumbnail
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(t, sol[:, 0], lw=2.5, color=SAGE_DARK, label="Presas")
ax.plot(t, sol[:, 1], lw=2.5, color=ACCENT_RED, label="Depredadores")
ax.fill_between(t, sol[:, 0], alpha=0.2, color=SAGE)
ax.set_title("System Dynamics — Lotka-Volterra (Python port)", fontweight="bold", fontsize=13)
ax.set_xlabel("Tiempo")
ax.set_ylabel("Población")
ax.legend(loc="upper right", frameon=True)
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(FIG_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig)
print(f"\n   ✓ figures/00_thumbnail.png")

print("\n" + "=" * 78)
print("MODELOS COMPLETOS ✓")
print("=" * 78)
