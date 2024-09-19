import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import argparse
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

    data = pd.read_excel(args.input)

    fig, ax1 = plt.subplots(figsize=(6, 4), subplot_kw=dict(polar=True))

    # ax1.set_theta_offset(np.pi / 2)
    # ax1.set_theta_direction(-1)
    ax1.set_ylim(-0.1, 1.05)
    ax1.grid(True, zorder=1)
    ax1.spines['polar'].set_visible(False)
    fontsize = 7

    x = data['seq'].unique().tolist()
    y = data['type'].unique().tolist()
    x = ['avg.'] + x
    angles = np.linspace(0, 2 * np.pi, len(x), endpoint=False).tolist()
    palette = sns.color_palette("Set1", len(y))
    ax1.set_xticks(angles, x, zorder=10)
    ticks = np.arange(0, 5) / 4
    labels = (ticks * 10 + 28).round(1)
    ax1.set_yticks(ticks=ticks, labels=labels, zorder=100, fontsize=fontsize)
    ax1.set_rlabel_position(40)

    angles += angles[:1]
    sign = [-1.5, 0.7, 0, 0.7, -1.5]
    x_offset = [0, -12, 0, 0, 0]
    for idx, key in enumerate(y):  
        if key == 'w/o pyramid':
            continue
        value = ((data[data['type'] == key].groupby('seq')['psnr'].median() - 28) / 10)
        value = [value.mean()] + value.tolist()
        value += value[:1]
        ax1.plot(angles, value, color=palette[idx], linewidth=1, label=key)
        ax1.scatter(angles, value, s=8, color=palette[idx], zorder=10)
        ax1.annotate(f"{value[0] * 10 + 28:.1f}", (angles[0], value[0]), textcoords="offset pixels", xytext=(x_offset[idx], sign[idx] * 6), fontsize=fontsize+1, color=palette[idx], zorder=40, fontweight='bold')
    

    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncols=len(y)-1, frameon=False, facecolor='none')

    plt.savefig(args.output, pad_inches=0, bbox_inches='tight')

