import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# GENERAR HISTOGRAMAS
# =========================
for i, col in enumerate(df_numeric.columns):

    data = df_numeric[col].dropna()

    mean = data.mean()
    std = data.std()

    color = colors[i % len(colors)]

    plt.figure(figsize=(8, 5))

    plt.hist(
        data,
        bins=35,
        color=color,
        alpha=0.7
    )

    # Media
    plt.axvline(
        mean,
        linestyle='--',
        color=color,
        linewidth=2,
        label=f'Mean: {mean:.4f}'
    )

    # -1 sigma
    plt.axvline(
        mean - std,
        linestyle=':',
        color=color,
        linewidth=2,
        label=f'-1σ: {mean - std:.4f}'
    )

    # +1 sigma
    plt.axvline(
        mean + std,
        linestyle=':',
        color=color,
        linewidth=2,
        label=f'+1σ: {mean + std:.4f}'
    )

    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')

    plt.grid(True)
    plt.legend()

    # Guardar imagen
    save_path = os.path.join(output_dir, f"{col}_hist.png")

    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

    print(f"Saved: {save_path}")

print("\nDone.")
