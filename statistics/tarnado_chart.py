import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import argparse
from matplotlib.ticker import ScalarFormatter
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
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0,0))

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_xlabel(None)
    # palettes = ["viridis", "cividis", "inferno", "magma", "plasma", "Blues", "Greens", "Reds", "Oranges", "Purples", "Browns", "Greys"]
    palette = sns.color_palette("Blues_r", 5)
    
    x = np.flip(data['Seq'].unique())
    points0 = np.flip(data[data['lr'] == 0].groupby('Seq')['Points'].mean() / data['Points'].max())
    points1 =  np.flip(data[data['lr'] == 1e-3].groupby('Seq')['Points'].mean() / data['Points'].max())
    points2 = np.flip(data[data['lr'] == 1e-2].groupby('Seq')['Points'].mean() / data['Points'].max())
    psnr0 = np.flip((data[data['lr'] == 0].groupby('Seq')['PSNR'].mean() - data['PSNR'].min()) / (data['PSNR'].max() - data['PSNR'].min()))
    psnr1 = np.flip((data[data['lr'] == 1e-3].groupby('Seq')['PSNR'].mean() - data['PSNR'].min()) / (data['PSNR'].max() - data['PSNR'].min()))
    psnr2 = np.flip((data[data['lr'] == 1e-2].groupby('Seq')['PSNR'].mean() - data['PSNR'].min()) / (data['PSNR'].max() - data['PSNR'].min()))
    ax1.barh(x, points0, height=0.5, color=palette[2], label='0e+0', edgecolor='none', zorder=3)
    ax1.barh(x, points1, height=0.5, color=palette[1], label='1e-3', edgecolor='none', zorder=3)
    ax1.barh(x, points2, height=0.5, color=palette[0], label='1e-2', edgecolor='none', zorder=3)
    ax1.barh(x, -psnr0, height=0.5, color=palette[2], edgecolor='none', zorder=3)
    ax1.barh(x, -psnr1, height=0.5, color=palette[1], edgecolor='none', zorder=3)
    ax1.barh(x, -psnr2, height=0.5, color=palette[0], edgecolor='none', zorder=3)
    ax1.axvline(0, color='k', linestyle='--', linewidth=0.9, zorder=4)
    ticks = np.arange(-4, 5) / 4
    psnrs = -np.arange(-4, 0) / 4 * (data['PSNR'].max() - data['PSNR'].min()) + data['PSNR'].min()
    points = np.arange(0, 5) / 4 * data['Points'].max() // 1000 * 1000
    labels = [(int(x) if x < 100 else f"{int(x // 1000)}k")for x in np.concatenate([psnrs, points])]
    plt.xticks(ticks=ticks, labels=labels)
    plt.text(0.01, 0.01, 'PSNR', va='bottom', ha='left', transform=plt.gca().transAxes)
    plt.text(0.99, 0.01, 'Points', va='bottom', ha='right', transform=plt.gca().transAxes)

    ax1.legend()
    ax1.grid(False, axis='y')

    plt.savefig(args.output, pad_inches=0, bbox_inches='tight')
