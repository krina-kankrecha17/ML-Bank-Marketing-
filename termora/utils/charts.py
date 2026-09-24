"""
termora/utils/charts.py
========================
All Plotly chart factory functions used across pages.
Each function returns a go.Figure styled for the Termora dark-navy theme.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from termora.config import COLORS

# Shared layout defaults
_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=COLORS["text_secondary"], size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor=COLORS["border"],
        borderwidth=1,
        font=dict(size=11, color=COLORS["text_secondary"]),
    ),
    xaxis=dict(
        gridcolor=COLORS["border"],
        zerolinecolor=COLORS["border"],
        showgrid=True,
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor=COLORS["border"],
        zerolinecolor=COLORS["border"],
        showgrid=True,
        tickfont=dict(size=11),
    ),
)


def _apply_base(fig: go.Figure) -> go.Figure:
    fig.update_layout(**_LAYOUT_BASE)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# ANALYTICS CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def subscription_donut(df: pd.DataFrame) -> go.Figure:
    counts = df["Subscribed"].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.62,
        marker=dict(colors=[COLORS["accent"], COLORS["border"]],
                    line=dict(color=COLORS["navy"], width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color=COLORS["text_primary"]),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text="Subscribers", x=0.5, y=0.52, showarrow=False,
        font=dict(size=12, color=COLORS["text_muted"]),
    )
    sub_pct = counts.get("Yes", 0) / counts.sum() * 100
    fig.add_annotation(
        text=f"<b>{sub_pct:.1f}%</b>", x=0.5, y=0.42, showarrow=False,
        font=dict(size=22, color=COLORS["text_primary"]),
    )
    fig.update_layout(**_LAYOUT_BASE, title=dict(text="Subscription Distribution", font=dict(size=14, color=COLORS["text_primary"])))
    return fig


def subscription_by_category(df: pd.DataFrame, col: str, title: str, max_cats: int = 12) -> go.Figure:
    grp = (
        df.groupby([col, "Subscribed"], observed=False)
        .size()
        .reset_index(name="Count")
    )
    # Limit categories
    order = df[col].value_counts().head(max_cats).index.tolist()
    grp = grp[grp[col].isin(order)]

    fig = px.bar(
        grp, x=col, y="Count", color="Subscribed",
        color_discrete_map={"Yes": COLORS["accent"], "No": COLORS["border"]},
        barmode="group",
        labels={"Count": "Customers"},
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=COLORS["text_primary"])),
        xaxis_tickangle=-30,
        bargap=0.2, bargroupgap=0.05,
        legend_title_text="",
    )
    return fig


def age_distribution(df: pd.DataFrame) -> go.Figure:
    sub_yes = df[df["Term Deposit Subscription"] == 1]["Age"]
    sub_no  = df[df["Term Deposit Subscription"] == 0]["Age"]

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=sub_no, name="No", nbinsx=30,
        marker_color=COLORS["border"],
        opacity=0.75,
        hovertemplate="Age: %{x}<br>Count: %{y}<extra>Not subscribed</extra>",
    ))
    fig.add_trace(go.Histogram(
        x=sub_yes, name="Yes", nbinsx=30,
        marker_color=COLORS["accent"],
        opacity=0.85,
        hovertemplate="Age: %{x}<br>Count: %{y}<extra>Subscribed</extra>",
    ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        barmode="overlay",
        title=dict(text="Age Distribution by Subscription", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis_title="Age",
        yaxis_title="Customers",
        legend_title_text="Subscribed",
    )
    return fig


def campaign_contacts_vs_subscription(df: pd.DataFrame) -> go.Figure:
    grp = (
        df.groupby("Campaign Contacts")["Term Deposit Subscription"]
        .agg(["mean", "count"])
        .reset_index()
    )
    grp = grp[grp["count"] >= 30].head(15)
    grp["mean"] *= 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grp["Campaign Contacts"], y=grp["mean"],
        marker=dict(
            color=grp["mean"],
            colorscale=[[0, COLORS["border"]], [0.5, COLORS["accent"]], [1, COLORS["teal"]]],
            showscale=False,
            line=dict(width=0),
        ),
        hovertemplate="Contacts: %{x}<br>Subscription Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        title=dict(text="Campaign Contacts vs Subscription Rate", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis_title="Number of Campaign Contacts",
        yaxis_title="Subscription Rate (%)",
    )
    return fig


def poutcome_chart(df: pd.DataFrame) -> go.Figure:
    grp = (
        df.groupby("Previous Campaign Outcome")["Term Deposit Subscription"]
        .agg(["mean", "count"])
        .reset_index()
    )
    grp["rate"] = grp["mean"] * 100
    colors = [COLORS["border"], COLORS["danger"], COLORS["success"]]

    fig = go.Figure(go.Bar(
        x=grp["Previous Campaign Outcome"],
        y=grp["rate"],
        marker=dict(color=colors[:len(grp)], line=dict(width=0)),
        text=[f"{v:.1f}%" for v in grp["rate"]],
        textposition="outside",
        textfont=dict(color=COLORS["text_secondary"], size=12),
        hovertemplate="Outcome: %{x}<br>Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        title=dict(text="Previous Campaign Outcome vs Subscription Rate", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis_title="Previous Campaign Outcome",
        yaxis_title="Subscription Rate (%)",
        yaxis_range=[0, grp["rate"].max() * 1.2],
    )
    return fig


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    numeric_cols = [
        "Age", "Campaign Contacts", "Days Since Previous Contact",
        "Previous Contacts", "Employment Variation Rate",
        "Consumer Price Index", "Consumer Confidence Index",
        "Euribor 3 Month Rate", "Number of Employees",
        "Term Deposit Subscription"
    ]
    corr = df[numeric_cols].corr()

    # Custom diverging colorscale: red-white-blue → navy palette
    colorscale = [
        [0.0,  "#EF4444"],
        [0.25, "#7F1D1D"],
        [0.5,  "#1E2D4A"],
        [0.75, "#1E3A6E"],
        [1.0,  "#1E6FD9"],
    ]
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale=colorscale,
        zmid=0,
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}",
        textfont=dict(size=9, color=COLORS["text_primary"]),
        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.2f}<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        title=dict(text="Feature Correlation Heatmap", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis_tickangle=-40,
        xaxis=dict(tickfont=dict(size=9), showgrid=False),
        yaxis=dict(tickfont=dict(size=9), showgrid=False),
        height=480,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# MODEL INSIGHTS CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def model_comparison_radar(results: list[dict]) -> go.Figure:
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    palette = COLORS["chart_palette"]
    fig = go.Figure()
    for i, row in enumerate(results):
        values = [row[m] for m in metrics] + [row[metrics[0]]]
        hex_c = palette[i % len(palette)].lstrip("#")
        r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics + [metrics[0]],
            fill="toself",
            fillcolor=f"rgba({r},{g},{b},0.12)",
            line=dict(color=palette[i % len(palette)], width=2),
            name=row["Model"],
            hovertemplate="<b>" + row["Model"] + "</b><br>%{theta}: %{r:.3f}<extra></extra>",
        ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 1],
                tickfont=dict(size=9, color=COLORS["text_muted"]),
                gridcolor=COLORS["border"],
                linecolor=COLORS["border"],
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=COLORS["text_secondary"]),
                gridcolor=COLORS["border"],
                linecolor=COLORS["border"],
            ),
        ),
        title=dict(text="Model Performance Radar", font=dict(size=14, color=COLORS["text_primary"])),
        showlegend=True,
        height=420,
    )
    return fig


def model_bar_comparison(results: list[dict], metric: str = "ROC-AUC") -> go.Figure:
    df = pd.DataFrame(results).sort_values(metric, ascending=True)
    palette = COLORS["chart_palette"]

    fig = go.Figure(go.Bar(
        x=df[metric],
        y=df["Model"],
        orientation="h",
        marker=dict(
            color=palette[:len(df)],
            line=dict(width=0),
        ),
        text=[f"{v:.3f}" for v in df[metric]],
        textposition="outside",
        textfont=dict(size=12, color=COLORS["text_primary"]),
        hovertemplate="<b>%{y}</b><br>" + metric + ": %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        title=dict(text=f"Model Comparison — {metric}", font=dict(size=14, color=COLORS["text_primary"])),
        xaxis=dict(range=[0, 1.05], title=metric),
        yaxis=dict(title=""),
        height=300,
        margin=dict(l=10, r=60, t=40, b=10),
    )
    return fig


def cv_stability_chart(cv_results: list[dict]) -> go.Figure:
    df = pd.DataFrame(cv_results)
    palette = COLORS["chart_palette"]
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Model"]], y=[row["Mean CV ROC-AUC"]],
            mode="markers",
            marker=dict(size=14, color=palette[i % len(palette)], line=dict(width=2, color=COLORS["navy"])),
            error_y=dict(type="constant", value=row["Std Dev (ROC-AUC)"], visible=True,
                         color=palette[i % len(palette)], thickness=2, width=6),
            name=row["Model"],
            hovertemplate=(
                "<b>%{x}</b><br>"
                f"Mean CV ROC-AUC: {row['Mean CV ROC-AUC']:.4f}<br>"
                f"± Std Dev: {row['Std Dev (ROC-AUC)']:.4f}<extra></extra>"
            ),
        ))
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_layout(
        title=dict(text="Cross-Validation Stability (Mean ROC-AUC ± Std Dev)", font=dict(size=14, color=COLORS["text_primary"])),
        yaxis=dict(title="Mean CV ROC-AUC", range=[0.55, 0.86]),
        xaxis=dict(title=""),
        showlegend=False,
        height=320,
    )
    return fig


def gauge_chart(probability: float) -> go.Figure:
    """Circular gauge for the prediction result card."""
    if probability >= 0.65:
        color = COLORS["success"]
    elif probability >= 0.40:
        color = COLORS["gold"]
    else:
        color = COLORS["danger"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        number=dict(suffix="%", font=dict(size=36, color=COLORS["text_primary"], family="Space Grotesk")),
        gauge=dict(
            axis=dict(range=[0, 100], tickfont=dict(size=10, color=COLORS["text_muted"]), tickwidth=1),
            bar=dict(color=color, thickness=0.22),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[0, 40],  color="rgba(239,68,68,0.08)"),
                dict(range=[40, 65], color="rgba(245,158,11,0.08)"),
                dict(range=[65, 100],color="rgba(16,185,129,0.08)"),
            ],
            threshold=dict(line=dict(color=color, width=3), thickness=0.75, value=probability * 100),
        ),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLORS["text_secondary"]),
        height=200,
        margin=dict(l=20, r=20, t=20, b=10),
    )
    return fig
