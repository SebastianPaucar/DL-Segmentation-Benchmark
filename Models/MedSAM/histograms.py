import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# =========================
# ARGUMENTS
# =========================
parser = argparse.ArgumentParser()

parser.add_argument(
    "--csv_path",
    type=str,
    required=True,
    help="Path to metrics_results.csv"
)

parser.add_argument(
    "--output_dir",
    type=str,
    required=True,
    help="Directory to save histograms"
)

args = parser.parse_args()
csv_path = args.csv_path
output_dir = args.output_dir

# =========================
# CREATE OUTPUT DIR
# =========================
os.makedirs(output_dir, exist_ok=True)

# =========================
# LOAD CSV
# =========================
df = pd.read_csv(csv_path)

# Excluir columnas que NO quieres graficar
excluded_cols = ["TP", "TN", "FP", "FN"]

# Seleccionar columnas numéricas válidas
df_numeric = df.select_dtypes(include=[np.number]).drop(columns=excluded_cols)

# Paleta de colores
colors = plt.cm.tab10.colors

# =========================
# CONFIGURAR SUBPLOTS
# =========================
n_cols = 3  # número de columnas en la grilla
n_features = len(df_numeric.columns)
n_rows = math.ceil(n_features / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
axes = axes.flatten()  # facilita iterar aunque haya 1 fila/columna

# =========================
# GENERAR HISTOGRAMAS EN LA GRILLA
# =========================
for i, col in enumerate(df_numeric.columns):
    ax = axes[i]
    data = df_numeric[col].dropna()
    mean = data.mean()
    std = data.std()
    color = colors[i % len(colors)]

    ax.hist(data, bins=35, color=color, alpha=0.7)
    ax.axvline(mean, linestyle='--', color=color, linewidth=2, label=f'Mean: {mean:.4f}')
    ax.axvline(mean - std, linestyle=':', color=color, linewidth=2, label=f'-1σ: {mean - std:.4f}')
    ax.axvline(mean + std, linestyle=':', color=color, linewidth=2, label=f'+1σ: {mean + std:.4f}')
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
    ax.grid(True)
    ax.legend(fontsize=8)

# Ocultar ejes vacíos si hay más subplots que columnas
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

plt.tight_layout()

# =========================
# GUARDAR UNA SOLA IMAGEN
# =========================
save_path = os.path.join(output_dir, "histograms_grid.png")
plt.savefig(save_path, dpi=300)
plt.close()
print(f"Saved grid histogram: {save_path}")
