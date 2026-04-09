"""
================================================================================
DESIGUALDAD DE INGRESOS Y TIEMPO EN CHILE — Equivalente Python
================================================================================

Este script reproduce el análisis del archivo 'analisis_desigualdad.R' usando
Python (pandas, numpy, matplotlib). Útil para validar resultados o ejecutar el
análisis sin necesidad de instalar R.

El script R principal está en analisis_desigualdad.R y es el entregable
preferido del proyecto (más conciso, idiomático para análisis estadístico).

Autor: Vicente Lombardozzi
================================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
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
OUT_DIR = HERE / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 1. Generar datos sintéticos similares a CASEN
# =============================================================================
np.random.seed(20260409)
n = 5000

casen = pd.DataFrame({
    "hogar_id": np.arange(1, n + 1),
    "region": np.random.choice(
        ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "Los Lagos"],
        size=n,
        p=[0.40, 0.15, 0.20, 0.13, 0.12],
    ),
    "sexo": np.random.choice(["Hombre", "Mujer"], size=n),
    "ingreso_clp": np.random.lognormal(mean=13.2, sigma=0.85, size=n),
})

# Quintiles y deciles
casen["quintil"] = pd.qcut(casen["ingreso_clp"], 5, labels=range(1, 6)).astype(int)
casen["decil"] = pd.qcut(casen["ingreso_clp"], 10, labels=range(1, 11)).astype(int)

# Horas por tipo de tiempo
casen["horas_trabajo_remunerado"] = np.maximum(
    0, np.random.normal(42, 12, n) - (5 - casen["quintil"]) * 1.5
)
casen["horas_cuidados"] = np.maximum(
    0, np.random.normal(18, 10, n) + (casen["sexo"] == "Mujer") * 12
)
casen["horas_ocio"] = np.maximum(
    0, 168 - 56 - casen["horas_trabajo_remunerado"] - casen["horas_cuidados"]
)

# =============================================================================
# 2. Coeficiente de Gini y otros índices
# =============================================================================
def gini(arr):
    arr = np.sort(np.array(arr, dtype=float))
    n = len(arr)
    return (2 * np.sum((np.arange(1, n + 1)) * arr)) / (n * arr.sum()) - (n + 1) / n


def theil(arr):
    arr = np.array(arr, dtype=float)
    arr = arr[arr > 0]
    mean = arr.mean()
    return np.mean((arr / mean) * np.log(arr / mean))


def atkinson(arr, eps):
    arr = np.array(arr, dtype=float)
    arr = arr[arr > 0]
    if eps == 1:
        return 1 - np.exp(np.mean(np.log(arr))) / arr.mean()
    return 1 - (np.mean(arr ** (1 - eps)) ** (1 / (1 - eps))) / arr.mean()


g = gini(casen["ingreso_clp"])
t = theil(casen["ingreso_clp"])
a05 = atkinson(casen["ingreso_clp"], 0.5)
a1 = atkinson(casen["ingreso_clp"], 1.0)
ratio = np.quantile(casen["ingreso_clp"], 0.9) / np.quantile(casen["ingreso_clp"], 0.1)

print(f"Gini de ingresos     : {g:.3f}")
print(f"Theil                : {t:.3f}")
print(f"Atkinson (e=0.5)     : {a05:.3f}")
print(f"Atkinson (e=1.0)     : {a1:.3f}")
print(f"Ratio P90/P10        : {ratio:.2f}")

indices_df = pd.DataFrame({
    "indice": ["Gini", "Theil", "Atkinson (e=0.5)", "Atkinson (e=1.0)", "Ratio P90/P10"],
    "valor": [g, t, a05, a1, ratio],
    "interpretacion": [
        "0 = igualdad, 1 = desigualdad máxima",
        "Sensible a transferencias",
        "Sensible a colas (e bajo)",
        "Sensible a colas (e alto)",
        "P90 / P10",
    ],
})
indices_df.to_csv(OUT_DIR / "indices_desigualdad.csv", index=False)


# =============================================================================
# 3. Curva de Lorenz
# =============================================================================
sorted_inc = np.sort(casen["ingreso_clp"].values)
cum_inc = np.cumsum(sorted_inc)
p = np.arange(1, len(sorted_inc) + 1) / len(sorted_inc)
L = cum_inc / cum_inc[-1]

fig, ax = plt.subplots(figsize=(8, 6))
ax.fill_between(p, L, p, color=SAGE, alpha=0.25, label="Brecha respecto a la igualdad")
ax.plot(p, L, color=SAGE_DARK, lw=2.5, label="Curva de Lorenz observada")
ax.plot([0, 1], [0, 1], color=SLATE, ls="--", lw=1, alpha=0.7, label="Línea de igualdad perfecta")
ax.set_title("Curva de Lorenz: distribución de ingresos en Chile", fontweight="bold", fontsize=13)
ax.text(0.05, 0.85, f"Coeficiente de Gini = {g:.3f}", fontsize=12,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=CREAM, edgecolor=SAGE_DARK))
ax.set_xlabel("Población acumulada (ordenada por ingreso)")
ax.set_ylabel("Ingreso acumulado")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend(loc="upper left", frameon=True)
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(OUT_DIR / "01_lorenz_curve.png", bbox_inches="tight")
plt.close(fig)
print(f"\n✓ output/01_lorenz_curve.png")


# =============================================================================
# 4. Distribución del tiempo por quintil
# =============================================================================
tiempo = casen.groupby("quintil")[["horas_trabajo_remunerado", "horas_cuidados", "horas_ocio"]].mean()

fig, ax = plt.subplots(figsize=(10, 6))
quintiles = tiempo.index.tolist()
trabajo = tiempo["horas_trabajo_remunerado"].values
cuidados = tiempo["horas_cuidados"].values
ocio = tiempo["horas_ocio"].values

ax.bar(quintiles, trabajo, color=SAGE_DARK, label="Trabajo remunerado")
ax.bar(quintiles, cuidados, bottom=trabajo, color=ACCENT_AMBER, label="Cuidados no remunerados")
ax.bar(quintiles, ocio, bottom=trabajo + cuidados, color=SAGE_LIGHT, label="Ocio")

ax.set_title("Distribución del tiempo semanal por quintil de ingreso",
             fontweight="bold", fontsize=13)
ax.set_xlabel("Quintil de ingreso (1 = más pobre, 5 = más rico)")
ax.set_ylabel("Horas a la semana")
ax.legend(loc="upper right", frameon=True)
ax.grid(alpha=0.3, ls="--", axis="y")
fig.tight_layout()
fig.savefig(OUT_DIR / "02_tiempo_por_quintil.png", bbox_inches="tight")
plt.close(fig)
print(f"✓ output/02_tiempo_por_quintil.png")


# =============================================================================
# 5. Brecha de género en cuidados
# =============================================================================
brecha = casen.groupby(["quintil", "sexo"])["horas_cuidados"].mean().unstack()

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(brecha.index))
width = 0.38
ax.bar(x - width/2, brecha["Hombre"], width, color=SAGE, label="Hombre")
ax.bar(x + width/2, brecha["Mujer"], width, color=ACCENT_RED, label="Mujer")
ax.set_xticks(x)
ax.set_xticklabels(brecha.index)
ax.set_xlabel("Quintil de ingreso")
ax.set_ylabel("Horas semanales en cuidados")
ax.set_title("Brecha de género en cuidados no remunerados",
             fontweight="bold", fontsize=13)
ax.legend(loc="upper right", frameon=True)
ax.grid(alpha=0.3, ls="--", axis="y")
fig.tight_layout()
fig.savefig(OUT_DIR / "03_brecha_genero.png", bbox_inches="tight")
plt.close(fig)
print(f"✓ output/03_brecha_genero.png")


# =============================================================================
# 6. Thumbnail
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.fill_between(p, L, p, color=SAGE, alpha=0.25)
ax.plot(p, L, color=SAGE_DARK, lw=3, label="Lorenz")
ax.plot([0, 1], [0, 1], color=SLATE, ls="--", lw=1)
ax.set_title("Desigualdad de ingresos en Chile", fontweight="bold", fontsize=13)
ax.set_xlabel("Población acumulada")
ax.set_ylabel("Ingreso acumulado")
ax.text(0.55, 0.15, f"Gini = {g:.3f}", fontsize=14, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=CREAM, edgecolor=SAGE_DARK))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.grid(alpha=0.3, ls="--")
fig.tight_layout()
fig.savefig(OUT_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig)
print(f"✓ output/00_thumbnail.png")

print("\n=== ANÁLISIS COMPLETO ===")
