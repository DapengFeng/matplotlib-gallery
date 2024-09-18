import matplotlib.pyplot as plt 
from scipy.stats import norm
import argparse
import pandas as pd
import seaborn as sns
import numpy as np

import platform

sns.set_style("darkgrid")

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Times New Roman'
else:
    print("Please use Windows to draw again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tornado Chart')
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('output', type=str, help='Output file')
    args = parser.parse_args()

    linewidth = 1.0

    data = pd.read_excel(args.input)

    palette1 = sns.color_palette("dark", 2)
    palette2 = sns.color_palette("bright", 2)

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.set_xlabel('Keyframe', fontsize=11)

    x = data[data['type'] == 'w/o']['frame']
    y1 = data[data['type'] == 'w/o']['Iter'] / 300
    z1 = data[data['type'] == 'w/o']['PSNR'] / 40
    y2 = data[data['type'] == 'w/']['Iter'] / 300
    z2 = data[data['type'] == 'w/']['PSNR'] / 40
    ax1.set_ylabel('Iteration', color=palette1[0], fontsize=11)
    ax1.plot(x, y1, '--', color=palette1[0], label='w/o', linewidth=linewidth, zorder=3)
    ax1.plot(x, y2, color=palette1[0], label='w/', linewidth=linewidth, zorder=3)
    ax1.axhline(np.mean(y1), color=palette1[0], linestyle='--', linewidth=0.8, zorder=2, alpha=0.7)
    ax1.axhline(np.mean(y2), color=palette1[0], linewidth=0.8, zorder=2, alpha=0.7)

    ticks = np.arange(0, 6) / 5
    labels = (ticks * 300).round(0).astype(np.int32)
    ax1.set_yticks(ticks=ticks, labels=labels)
    ax1.tick_params(axis='y', labelcolor=palette1[0])

    ax1.axhline(np.mean(z1), color=palette2[1], linestyle='--', linewidth=0.8, zorder=2, alpha=0.7)
    ax1.axhline(np.mean(z2), color=palette2[1], linewidth=0.8, zorder=2, alpha=0.7)

    ax2 = ax1.twinx()
    ax2.set_ylabel('PSNR', color=palette2[1], fontsize=11)

    ax2.plot(x, z1, '--', color=palette2[1], label='w/o', linewidth=linewidth, zorder=3)
    ax2.plot(x, z2, color=palette2[1], label='w/', linewidth=linewidth, zorder=3)

    labels = (ticks * 40).astype(np.int32)
    ticks = np.append(ticks, [np.mean(z1), np.mean(z2)])
    labels = np.append(labels, [np.mean(z1) *  40, np.mean(z2) *  40]).round(1)
    ax2.set_yticks(ticks=ticks, labels=labels)
    ax2.tick_params(axis='y', labelcolor=palette2[1])

    max_ylim = max(ax1.get_ylim()[1], ax2.get_ylim()[1])
    min_ylim = min(ax1.get_ylim()[0], ax2.get_ylim()[0])
    ax1.set_ylim(min_ylim, max_ylim)
    ax2.set_ylim(min_ylim, max_ylim)
    ax2.grid(False)

    legend_elements = [plt.Line2D([0], [0], linestyle='--', color='k', linewidth=linewidth, label='w/o'),
                       plt.Line2D([0], [0], color='k', linewidth=linewidth, label='w/')]


    plt.legend(handles=legend_elements)
    
    plt.savefig(args.output, pad_inches=0, bbox_inches='tight')