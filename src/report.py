"""Report and visualization module."""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def save_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    output_path: str | Path,
) -> None:
    """Save a simple bar chart from a DataFrame."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.bar(df[x_column].astype(str), df[y_column])
    plt.title(title)
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
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
