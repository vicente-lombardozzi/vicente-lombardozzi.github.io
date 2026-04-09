"""
================================================================================
ANÁLISIS DE SENTIMIENTO EN ESPAÑOL — Comparación de enfoques
================================================================================

Compara tres enfoques de clasificación de sentimiento sobre reseñas en español:
    1. Diccionario de palabras (lexicon-based)
    2. Bag-of-words + Logistic Regression
    3. TF-IDF + Linear SVM

Este proyecto se conecta directamente con StratNova, el emprendimiento del
autor en IA conversacional para automatización de ventas, y con su experiencia
previa en Outlier (2024-2025) entrenando LLMs en español e inglés.

Para evitar dependencias pesadas (transformers/torch), aquí usamos enfoques
clásicos de scikit-learn que igualmente entregan resultados sólidos.

Autor: Vicente Lombardozzi
Fecha: 2026
================================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support, confusion_matrix
)

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
DATA_DIR = HERE / "data"
FIG_DIR = HERE / "data" / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 1. Dataset sintético de reseñas en español (estilo MercadoLibre / Amazon ES)
# =============================================================================
positivos = [
    "excelente producto, muy recomendado",
    "el servicio fue impecable y la atención muy amable",
    "calidad superior, vale completamente lo que cuesta",
    "lo amo, lo compraré de nuevo sin dudarlo",
    "envío rapidísimo y empaque cuidadoso",
    "increíble relación calidad-precio",
    "funciona perfecto, mejor de lo que esperaba",
    "todo perfecto, lo recomiendo cien por ciento",
    "encantada con la compra, muy buen producto",
    "atención al cliente excepcional, resolvieron todo",
    "rápido, eficiente y como lo describían",
    "muy contento con el resultado, gracias",
    "fantástico, superó todas mis expectativas",
    "la mejor compra que he hecho este año",
    "calidad premium, recomendado totalmente",
    "vendedor muy profesional, todo correcto",
    "producto tal cual la descripción, perfecto",
    "rendimiento extraordinario, muy satisfecho",
    "diseño elegante y funcional, me encanta",
    "compra exitosa, todo según lo prometido",
] * 5

negativos = [
    "pésimo producto, no lo recomiendo a nadie",
    "llegó roto y el vendedor no responde",
    "horrible calidad, perdí mi dinero",
    "la peor compra que he hecho, devuelvan mi plata",
    "tardó muchísimo en llegar y vino dañado",
    "muy mala atención, prepotentes y poco profesionales",
    "no funciona como dice la descripción, falsa publicidad",
    "decepcionante en todo sentido, no compren",
    "se rompió en una semana, basura",
    "el peor servicio que he visto, evítenlo",
    "calidad penosa, no vale ni un peso",
    "estafa total, jamás llegó el producto",
    "fatal experiencia, nunca más",
    "muy malo, exijo reembolso",
    "no recomiendo para nada, pésima calidad",
    "vendedor irresponsable, no responde mensajes",
    "producto defectuoso desde el primer día",
    "una decepción total, desperdicio de dinero",
    "llegó incompleto, faltaban piezas",
    "terrible experiencia, no compren aquí",
] * 5

neutros = [
    "producto correcto, cumple lo básico",
    "es lo que se esperaba, ni más ni menos",
    "regular, ni bueno ni malo",
    "funcionalmente está bien, sin más",
    "cumple su función, podría mejorar el empaque",
    "normal, hace lo que tiene que hacer",
    "está ok, nada extraordinario",
    "aceptable por el precio que pagué",
    "cumple, pero esperaba un poco más",
    "ni encantado ni decepcionado",
    "uso normal, sin problemas hasta ahora",
    "esta bien, dentro de lo esperado",
    "producto estándar, sin sorpresas",
    "todo dentro de lo normal",
    "razonable, podría ser mejor o peor",
    "funcional, sin más comentarios",
    "discreto pero útil",
    "promedio, nada destacable",
    "regular, esperaba algo distinto",
    "lo justo y necesario",
] * 5

corpus = pd.DataFrame({
    "text": positivos + negativos + neutros,
    "label": ["positivo"] * len(positivos) + ["negativo"] * len(negativos) + ["neutro"] * len(neutros),
})
corpus = corpus.sample(frac=1, random_state=42).reset_index(drop=True)
corpus.to_csv(DATA_DIR / "dataset_resenas.csv", index=False, encoding="utf-8")
print(f"Dataset: {len(corpus)} reseñas ({(corpus['label'] == 'positivo').sum()} pos, "
      f"{(corpus['label'] == 'negativo').sum()} neg, {(corpus['label'] == 'neutro').sum()} neu)")


# =============================================================================
# 2. Lexicon simple en español
# =============================================================================
LEXICON_POSITIVO = {
    "excelente", "increíble", "perfecto", "amo", "encanta", "fantástico",
    "extraordinario", "premium", "amable", "rápido", "rapidísimo", "satisfecho",
    "profesional", "recomendado", "recomiendo", "elegante", "impecable",
    "calidad", "superior", "encantada", "contento", "exitosa", "buena",
    "buen", "bueno", "mejor",
}
LEXICON_NEGATIVO = {
    "pésimo", "pesimo", "horrible", "mala", "malo", "peor", "decepcionante",
    "dañado", "roto", "estafa", "basura", "fatal", "terrible", "irresponsable",
    "defectuoso", "desperdicio", "decepción", "decepcion", "exijo", "penosa",
    "evítenlo", "evitenlo", "incompleto", "tardó",
}


def predict_lexicon(text):
    tokens = set(text.lower().split())
    pos_count = len(tokens & LEXICON_POSITIVO)
    neg_count = len(tokens & LEXICON_NEGATIVO)
    if pos_count > neg_count:
        return "positivo"
    if neg_count > pos_count:
        return "negativo"
    return "neutro"


# =============================================================================
# 3. Train-test split
# =============================================================================
X_train_text, X_test_text, y_train, y_test = train_test_split(
    corpus["text"].values, corpus["label"].values,
    test_size=0.30, random_state=42, stratify=corpus["label"].values
)
print(f"\nTrain: {len(X_train_text)} | Test: {len(X_test_text)}")


# =============================================================================
# 4. Modelo 1: Lexicon
# =============================================================================
print("\n" + "=" * 78)
print("Modelo 1 — Lexicon basado en diccionarios")
print("=" * 78)
y_pred_lex = np.array([predict_lexicon(t) for t in X_test_text])
acc_lex = accuracy_score(y_test, y_pred_lex)
print(f"Accuracy: {acc_lex:.3f}")


# =============================================================================
# 5. Modelo 2: Bag-of-words + Logistic Regression
# =============================================================================
print("\n" + "=" * 78)
print("Modelo 2 — Bag-of-Words + Logistic Regression")
print("=" * 78)

bow = CountVectorizer(min_df=1, ngram_range=(1, 2))
X_train_bow = bow.fit_transform(X_train_text)
X_test_bow = bow.transform(X_test_text)

lr = LogisticRegression(max_iter=1000, solver="lbfgs")
lr.fit(X_train_bow, y_train)
y_pred_lr = lr.predict(X_test_bow)
acc_lr = accuracy_score(y_test, y_pred_lr)
print(f"Accuracy: {acc_lr:.3f}")


# =============================================================================
# 6. Modelo 3: TF-IDF + Linear SVM
# =============================================================================
print("\n" + "=" * 78)
print("Modelo 3 — TF-IDF + Linear SVM")
print("=" * 78)

tfidf = TfidfVectorizer(min_df=1, ngram_range=(1, 2), sublinear_tf=True)
X_train_tfidf = tfidf.fit_transform(X_train_text)
X_test_tfidf = tfidf.transform(X_test_text)

svm = LinearSVC(C=1.0)
svm.fit(X_train_tfidf, y_train)
y_pred_svm = svm.predict(X_test_tfidf)
acc_svm = accuracy_score(y_test, y_pred_svm)
print(f"Accuracy: {acc_svm:.3f}")


# =============================================================================
# 7. Comparación final
# =============================================================================
results = pd.DataFrame({
    "modelo": ["Lexicon", "BoW + LogReg", "TF-IDF + SVM"],
    "accuracy": [acc_lex, acc_lr, acc_svm],
})
print("\n" + "=" * 78)
print("RESULTADOS FINALES")
print("=" * 78)
print(results.to_string(index=False))
results.to_csv(DATA_DIR / "results_comparison.csv", index=False)


# =============================================================================
# 8. Visualización: comparación de accuracy
# =============================================================================
fig, ax = plt.subplots(figsize=(9, 5.5))
colors = [SAGE_LIGHT, SAGE, SAGE_DARK]
bars = ax.bar(results["modelo"], results["accuracy"], color=colors, edgecolor=SLATE, linewidth=0.8)
for bar, val in zip(bars, results["accuracy"]):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.2%}",
            ha="center", fontweight="bold", color=SLATE)
ax.set_ylim(0, 1.1)
ax.set_ylabel("Accuracy")
ax.set_title("Comparación de modelos de sentimiento en español",
             fontweight="bold", fontsize=13)
ax.grid(alpha=0.3, ls="--", axis="y")
fig.tight_layout()
fig.savefig(FIG_DIR / "01_model_comparison.png", bbox_inches="tight")
plt.close(fig)
print(f"\n✓ data/figures/01_model_comparison.png")


# =============================================================================
# 9. Matriz de confusión del mejor modelo
# =============================================================================
best_pred = y_pred_svm if acc_svm >= max(acc_lr, acc_lex) else y_pred_lr if acc_lr >= acc_lex else y_pred_lex
best_name = "TF-IDF + SVM" if acc_svm >= max(acc_lr, acc_lex) else "BoW + LogReg" if acc_lr >= acc_lex else "Lexicon"

labels_order = ["negativo", "neutro", "positivo"]
cm = confusion_matrix(y_test, best_pred, labels=labels_order)

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(cm, cmap="Greens", aspect="auto")
ax.set_xticks(range(3))
ax.set_yticks(range(3))
ax.set_xticklabels(labels_order)
ax.set_yticklabels(labels_order)
ax.set_xlabel("Predicción")
ax.set_ylabel("Real")
ax.set_title(f"Matriz de confusión — {best_name}", fontweight="bold", fontsize=12)
for i in range(3):
    for j in range(3):
        ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                color=CREAM if cm[i, j] > cm.max() / 2 else SLATE, fontweight="bold")
fig.tight_layout()
fig.savefig(FIG_DIR / "02_confusion_matrix.png", bbox_inches="tight")
plt.close(fig)
print(f"✓ data/figures/02_confusion_matrix.png")


# =============================================================================
# 10. Thumbnail
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(results["modelo"], results["accuracy"] * 100, color=colors, edgecolor=SLATE)
for bar, val in zip(bars, results["accuracy"]):
    ax.text(bar.get_x() + bar.get_width() / 2, val * 100 + 2, f"{val:.0%}",
            ha="center", fontweight="bold", color=SLATE)
ax.set_ylim(0, 110)
ax.set_ylabel("Accuracy (%)")
ax.set_title("NLP Sentiment Análisis en español", fontweight="bold", fontsize=13)
ax.grid(alpha=0.3, ls="--", axis="y")
fig.tight_layout()
fig.savefig(FIG_DIR / "00_thumbnail.png", bbox_inches="tight", dpi=200)
plt.close(fig)
print(f"✓ data/figures/00_thumbnail.png")

print("\n=== NLP COMPLETO ===")
