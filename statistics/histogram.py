import matplotlib.pyplot as plt 
from scipy.stats import norm
import argparse
import pandas as pd
import seaborn as sns
import numpy as np

import platform

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

    palette = sns.color_palette("Blues_r", 2)

    fig, ax1 = plt.subplots(figsize=(6, 3))

    ax1.set_ylabel('Iteration', fontsize=11)
    
    x = data['seq'].unique()

    iter0 = data[data['type'] == 'pixel'].groupby('seq')['iter'].mean() / 16000
    iter1 = data[data['type'] == 'splat'].groupby('seq')['iter'].mean() / 16000
    iter0_mean = iter0.mean()
    iter1_mean = iter1.mean()

    ax1.bar(x, iter0, color=palette[0], width=0.5, label='pixel', edgecolor='k', zorder=2, alpha=0.7)
    ax1.bar(x, iter1, color=palette[1], width=0.5, label='splat', edgecolor='k', zorder=1, alpha=0.7)

    ax1.axhline(iter0_mean, color=palette[0], linestyle='--', linewidth=0.8, zorder=4)
    ax1.axhline(iter1_mean, color=palette[1], linestyle='--', linewidth=0.8, zorder=4)

    ticks = np.arange(0, 5) / 5
    ticks = np.append(ticks, [np.mean(iter0_mean), np.mean(iter1_mean)])
    labels = [f"{x}k" for x in (ticks * 16).round(1)]
    ax1.set_yticks(ticks=ticks, labels=labels)

    plt.legend()
    
    plt.savefig(args.output, pad_inches=0, bbox_inches='tight')

