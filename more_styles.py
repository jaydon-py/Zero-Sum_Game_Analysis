# More Styles

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
import matplotlib as mpl
from matplotlib import font_manager
from adjustText import adjust_text

available = {f.name for f in font_manager.fontManager.ttflist}
font = next((f for f in ['Inter', 'Helvetica Neue', 'Helvetica', 'Arial', 'Segoe UI'] if f in available),
            'DejaVu Sans')

BG, FG, MUTED = '#191724', '#e0def4', '#908caa'   # rose-pine base / text / muted

mpl.rcParams.update({
    'font.family': font,
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': FG, 'axes.labelcolor': MUTED,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'xtick.major.size': 0, 'ytick.major.size': 0,       # no tick marks
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.spines.left': False, 'axes.spines.bottom': False,
    'axes.grid': True, 'axes.grid.axis': 'y',
    'grid.color': FG, 'grid.alpha': 0.07, 'grid.linewidth': 0.6,
    'axes.axisbelow': True,
    'figure.dpi': 110, 'savefig.dpi': 220,
    'legend.frameon': False,
})

LINE_KW = dict(
    linewidth=1.1,         
    alpha=0.85,            
    marker='o',
    markersize=3.5,       
    markeredgewidth=0,     
    solid_joinstyle='round',
)

def soften_axes(ax, ref_y=None, ref_label=None):
    """Light horizontal grid, no top/right spines, muted ticks."""
    ax.grid(axis='y', color='white', alpha=0.08, linewidth=0.6)
    ax.grid(axis='x', visible=False)
    ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_alpha(0.3)
    ax.tick_params(colors='#908caa', labelsize=9, length=3)
    if ref_y is not None:
        ax.axhline(ref_y, color='#908caa', linestyle=(0, (4, 4)),
                   linewidth=0.8, alpha=0.6, label=ref_label)

def soften_legend(ax):
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0),
                    frameon=False, fontsize=9, labelcolor='#e0def4',
                    handlelength=1.5, markerscale=1.2)
    return leg

def title_block(fig, ax, title, subtitle=None):
    """Left-aligned headline + muted subtitle, like a news/Bloomberg chart."""
    fig.text(0.06, 0.965, title, fontsize=20, fontweight='bold', color=FG, ha='left', va='top')
    if subtitle:
        fig.text(0.06, 0.915, subtitle, fontsize=11.5, color=MUTED, ha='left', va='top')

def end_labels(ax, series, min_gap):
    """
    series: list of (label, x_last, y_last, colour).
    Writes the name at the end of each line and nudges labels apart so they don't overlap.
    """
    series = sorted(series, key=lambda s: s[2])
    placed = []
    for label, x, y, c in series:
        y_text = y if not placed else max(y, placed[-1] + min_gap)
        placed.append(y_text)
        ax.annotate(label, xy=(x, y), xytext=(x + 0.6, y_text),
                    color=c, fontsize=10, fontweight='bold', va='center',
                    arrowprops=dict(arrowstyle='-', color=c, alpha=0.35, lw=0.6,
                                    shrinkA=0, shrinkB=2))

def footer(fig, text=""):
    fig.text(0.06, 0.015, text, fontsize=8.5, color=MUTED, ha='left')

# --- CUMULATIVE PROFIT ----

# ── Font: first available, else matplotlib default ───────────────────────

# ── Helpers ──────────────────────────────────────────────────────────────
def profit_title_block(fig, ax, title, subtitle=None):
    """Left-aligned headline + muted subtitle."""
    fig.text(0.06, 0.965, title, fontsize=20, fontweight='bold', color=FG, ha='left', va='top')
    if subtitle:
        fig.text(0.06, 0.915, subtitle, fontsize=11.5, color=MUTED, ha='left', va='top')

def profit_end_labels(ax, series, min_gap=None, x_offset=0.8):

    texts = []

    for label, x, y, c in series:
        texts.append(
            ax.text(
                x + x_offset, y, label,
                color=c,
                fontsize=9,
                fontweight='bold',
                ha='left',
                va='center',
                bbox=dict(
                    facecolor=BG,
                    edgecolor='none',
                    alpha=0.9,
                    pad=2
                ),
                zorder=10
            )
        )

    adjust_text(
        texts,
        ax=ax,
        only_move={'text': 'xy', 'static': 'xy', 'explode': 'xy', 'pull': 'xy'},
        force_text=(0.5, 0.8),
        force_static=(0.5, 0.8),
        force_pull=(0.02, 0.02),
        expand=(1.2, 1.4),
        arrowprops=dict(
            arrowstyle='-',
            color=MUTED,
            alpha=0.5,
            lw=0.7
        )
    )

    return texts

def profit_footer(fig, text=""):
    fig.text(0.06, 0.015, text, fontsize=8.5, color=MUTED, ha='left')

def profit_gbp(v, _=None):
    pound = '\u00a3'
    return f'-{pound}{abs(v):,.0f}' if v < 0 else f'{pound}{v:,.0f}'