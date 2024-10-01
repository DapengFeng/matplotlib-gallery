import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import argparse
import numpy as np
from adjustText import adjust_text
import matplotlib

import platform

# sns.set_style("darkgrid")

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Times New Roman'
else:
    print("Please use Windows to draw again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tornado Chart')
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('output', type=str, help='Output file')
    args = parser.parse_args()

    data = pd.read_excel(args.input)

    fig, ax1 = plt.subplots(figsize=(4, 3))
    # ax1.set_xlabel('Points')
    # ax1.set_ylabel('PSNR')
    ax1.text(0.65, -0.04, 'Points', va='top', ha='left', color='black', transform=ax1.get_xaxis_transform(), clip_on=False)
    ax1.text(-0.01, 0.96, 'PSNR', va='center', ha='right', color='black', transform=ax1.get_yaxis_transform(), clip_on=False)

    methods = data['method'].unique()
    ticks = np.arange(0, 6) / 5
    y_labels = (ticks * 10 + 15).round(1)
    x_labels = [f'$10^{int(y)}$' for y in (ticks * 5 + 3)]
    ax1.set_xticks(ticks=ticks, labels=x_labels)
    ax1.set_yticks(ticks=ticks, labels=y_labels)

    marker = ['o', '^', 'D', 'v', 'd', '*']
    palette = sns.color_palette("bright", len(marker))
    palette_idx = [0, 1, 2, 4, 5, 3]

    texts = []
    for idx, method in enumerate(methods):
        psnr = (data[data['method'] == method]['psnr'].median() - 15) / 10
        points = (np.log10(data[data['method'] == method]['points'].median()) - 3) / 5
        ax1.scatter(points, psnr, s=20, color=palette[palette_idx[idx]], label=method, marker=marker[idx])
        if method == 'Ours':
            ax1.scatter(points, psnr, s=200, color=palette[palette_idx[idx]], marker=marker[idx])
        else:
            ax1.scatter(points, psnr, s=50, color=palette[palette_idx[idx]], marker=marker[idx])
        texts.append(plt.annotate(
            f"($10^{{{np.log10(data[data['method'] == method]['points'].median()):.1f}}}$, {data[data['method'] == method]['psnr'].median().round(1)})",
            (points, psnr), color=palette[palette_idx[idx]], ha='left', va='bottom', fontsize=7))

    adjust_text(texts, force_text=(0.05, 0.05))

    plt.legend(ncols=2, fontsize=5)
    plt.savefig(args.output, pad_inches=0, bbox_inches='tight')