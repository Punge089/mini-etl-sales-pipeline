"""Report and visualization module."""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


CHART_COLORS = [
    "#2563eb",
    "#16a34a",
    "#f97316",
    "#9333ea",
    "#dc2626",
    "#0891b2",
    "#ca8a04",
    "#4f46e5",
]


def _format_currency(value: float, _: int) -> str:
    """Format chart axis values as compact dollars."""
    if abs(value) >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def save_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    output_path: str | Path,
) -> None:
    """Save a polished bar chart from a DataFrame."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    labels = df[x_column].astype(str)
    values = df[y_column]
    colors = [CHART_COLORS[index % len(CHART_COLORS)] for index in range(len(df))]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.2)

    ax.set_title(title, fontsize=18, fontweight="bold", color="#111827", pad=18)
    ax.set_xlabel(x_column.replace("_", " ").title(), fontsize=11, color="#4b5563")
    ax.set_ylabel(y_column.replace("_", " ").title(), fontsize=11, color="#4b5563")
    ax.yaxis.set_major_formatter(FuncFormatter(_format_currency))
    ax.grid(axis="y", color="#e5e7eb", linewidth=0.9)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelrotation=35, labelsize=10, colors="#374151")
    ax.tick_params(axis="y", labelsize=10, colors="#374151")
    ax.margins(y=0.15)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#d1d5db")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            _format_currency(value, 0),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#111827",
        )

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def write_markdown_report(
    metrics: dict[str, pd.DataFrame],
    output_path: str | Path,
) -> None:
    """Write SQL metrics into a Markdown report file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Sales Data Pipeline Report",
        "",
        "This report was generated from cleaned sales data loaded into a SQLite database.",
        "",
    ]

    for section_name, metric_df in metrics.items():
        title = section_name.replace("_", " ").title()
        lines.append(f"## {title}")
        lines.append("")
        lines.append(metric_df.to_markdown(index=False))
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
