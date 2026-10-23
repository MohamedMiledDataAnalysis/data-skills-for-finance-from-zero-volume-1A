"""
nbcharts.py - the Northbridge Bank chart style.

Import it at the top of every chart script:

    from nbcharts import nb_style, PALETTE, add_titles, save_chart

Call nb_style() once, before you create a figure.
"""

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.ticker import FuncFormatter

# The house colours, by name.
PALETTE = {
    "navy": "#1F2A44",
    "gold": "#C9A227",
    "teal": "#2E7D7A",
    "slate": "#6B7A90",
    "red": "#B23A48",
    "sand": "#E9DFC4",
    "grid": "#E6E8EC",
}

# The order in which series receive a colour.
SERIES_ORDER = ["navy", "teal", "gold", "slate"]

SOURCE = "Source: Northbridge Bank (synthetic data)"


def nb_style():
    """Apply the Northbridge chart style to every new figure."""
    colours = [PALETTE[name] for name in SERIES_ORDER]
    plt.rcParams.update({
        "figure.figsize": (6, 3.6),
        "figure.dpi": 100,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlecolor": PALETTE["navy"],
        "axes.labelsize": 9,
        "axes.labelcolor": "#333333",
        "axes.edgecolor": "#9AA3B2",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "xtick.color": "#444444",
        "ytick.color": "#444444",
        "legend.fontsize": 8,
        "legend.frameon": False,
        "lines.linewidth": 1.4,
        "axes.prop_cycle": cycler(color=colours),
    })


def add_titles(ax, title, subtitle=SOURCE):
    """Write a bold title and a grey subtitle above the plot."""
    ax.set_title(title, pad=20)
    ax.text(0, 1.03, subtitle, transform=ax.transAxes,
            fontsize=8, color=PALETTE["slate"], va="bottom")


def save_chart(fig, filename, book_name=None):
    """Save to output/; copy to figures/ when book_name is given."""
    out = Path("output") / filename
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print("Saved", out.as_posix())
    if book_name:
        figs = Path("figures")
        figs.mkdir(exist_ok=True)
        shutil.copy(out, figs / book_name)
        print("Copied to", (figs / book_name).as_posix())


# Ready-made tick formatters.
gbp = FuncFormatter(lambda x, pos: f"£{x:,.0f}")
gbp_m = FuncFormatter(lambda x, pos: f"£{x:,.0f}m")
pct = FuncFormatter(lambda x, pos: f"{x:.0f}%")
thousands = FuncFormatter(lambda x, pos: f"{x:,.0f}")
