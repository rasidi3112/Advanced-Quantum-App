import os
from typing import Dict, Optional, List

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

DARK_BG = "#0d1117"
DARK_SURFACE = "#161b22"
DARK_BORDER = "#30363d"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"

GRADIENT_COLORS = [
    "#7c3aed",
    "#6366f1",
    "#3b82f6",
    "#06b6d4",
    "#10b981",
    "#22d3ee",
    "#a78bfa",
    "#818cf8",
]

ACCENT_PALETTES = {
    "entanglement": ["#f472b6", "#ec4899", "#db2777", "#be185d"],
    "grover": ["#34d399", "#10b981", "#059669", "#047857"],
    "teleportation": ["#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"],
    "qft": ["#a78bfa", "#8b5cf6", "#7c3aed", "#6d28d9"],
    "phase_estimation": ["#fbbf24", "#f59e0b", "#d97706", "#b45309"],
    "vqe": ["#fb923c", "#f97316", "#ea580c", "#c2410c"],
    "quantum_walk": ["#2dd4bf", "#14b8a6", "#0d9488", "#0f766e"],
    "error_correction": ["#f87171", "#ef4444", "#dc2626", "#b91c1c"],
    "deutsch_jozsa": ["#c084fc", "#a855f7", "#9333ea", "#7e22ce"],
    "bernstein_vazirani": ["#67e8f9", "#22d3ee", "#06b6d4", "#0891b2"],
    "simon": ["#86efac", "#4ade80", "#22c55e", "#16a34a"],
    "ghz": ["#fca5a1", "#f87171", "#ef4444", "#dc2626"],
}


def _apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor": DARK_SURFACE,
        "axes.edgecolor": DARK_BORDER,
        "axes.labelcolor": TEXT_PRIMARY,
        "text.color": TEXT_PRIMARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
        "grid.color": DARK_BORDER,
        "grid.alpha": 0.3,
        "font.family": "sans-serif",
        "font.size": 12,
    })


def plot_histogram_premium(
    counts: Dict[str, int],
    title: str = "Quantum Results",
    save_path: Optional[str] = None,
    palette_key: Optional[str] = None,
    figsize: tuple = (14, 7),
    show: bool = True,
) -> Optional[str]:
    _apply_dark_theme()

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    states = [f"|{s}⟩" for s, _ in sorted_items]
    values = [c for _, c in sorted_items]
    total_shots = sum(values)

    if palette_key and palette_key in ACCENT_PALETTES:
        base_colors = ACCENT_PALETTES[palette_key]
    else:
        base_colors = GRADIENT_COLORS

    colors = [base_colors[i % len(base_colors)] for i in range(len(states))]

    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.bar(states, values, color=colors, edgecolor="none", width=0.7,
                  alpha=0.9, zorder=3)

    for bar, color in zip(bars, colors):
        ax.bar(bar.get_x() + bar.get_width() / 2, bar.get_height(),
               width=bar.get_width() * 1.15, alpha=0.15, color=color,
               zorder=2, align='center')

    for bar, value in zip(bars, values):
        probability = (value / total_shots) * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.02,
            f"{value}\n({probability:.1f}%)",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold",
            color=TEXT_PRIMARY, alpha=0.9,
        )

    ax.set_xlabel("Quantum State", fontsize=13, fontweight="bold",
                  labelpad=10, color=TEXT_SECONDARY)
    ax.set_ylabel("Count", fontsize=13, fontweight="bold",
                  labelpad=10, color=TEXT_SECONDARY)
    ax.set_title(title, fontsize=18, fontweight="bold", pad=20,
                 color=TEXT_PRIMARY)

    ax.grid(axis="y", alpha=0.15, color=TEXT_SECONDARY, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(DARK_BORDER)
    ax.spines["bottom"].set_color(DARK_BORDER)

    if len(states) > 8:
        plt.xticks(rotation=45, ha="right", fontsize=9)
    else:
        plt.xticks(fontsize=10)

    ax.text(
        0.98, 0.97,
        f"Total shots: {total_shots:,}",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=10, color=TEXT_SECONDARY,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_SURFACE,
                  edgecolor=DARK_BORDER, alpha=0.8),
    )

    plt.tight_layout()

    saved_path = None
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=DARK_BG, edgecolor="none")
        saved_path = save_path

    if show:
        plt.show()
    else:
        plt.close(fig)

    return saved_path


def plot_comparison(
    results: Dict[str, Dict[str, int]],
    title: str = "Algorithm Comparison",
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[str]:
    _apply_dark_theme()

    n = len(results)
    cols = min(3, n)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(7 * cols, 5 * rows))
    if n == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]

    palette_keys = list(ACCENT_PALETTES.keys())

    for idx, (name, counts) in enumerate(results.items()):
        if idx >= len(axes):
            break

        ax = axes[idx]
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:8]
        states = [f"|{s}⟩" for s, _ in sorted_items]
        values = [c for _, c in sorted_items]

        palette_key = palette_keys[idx % len(palette_keys)]
        base_colors = ACCENT_PALETTES[palette_key]
        colors = [base_colors[i % len(base_colors)] for i in range(len(states))]

        ax.bar(states, values, color=colors, edgecolor="none", width=0.7, alpha=0.9)
        ax.set_title(name, fontsize=12, fontweight="bold", color=TEXT_PRIMARY, pad=10)
        ax.grid(axis="y", alpha=0.15, color=TEXT_SECONDARY, linestyle="--")
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        if len(states) > 6:
            ax.tick_params(axis='x', rotation=45, labelsize=8)

    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle(title, fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=1.02)
    plt.tight_layout()

    saved_path = None
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=DARK_BG, edgecolor="none")
        saved_path = save_path

    if show:
        plt.show()
    else:
        plt.close(fig)

    return saved_path
