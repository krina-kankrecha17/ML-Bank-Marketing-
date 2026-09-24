"""
termora/pages/model_insights.py
================================
Model Insights page — baseline comparison, CV results, tuning results,
radar chart, bar chart, and stability chart.
"""

import streamlit as st
import pandas as pd
from termora.config import BASELINE_RESULTS, CV_RESULTS, TUNING_RESULTS
from termora.utils.charts import (
    model_comparison_radar,
    model_bar_comparison,
    cv_stability_chart,
)


def _metric_pill(value: float, *, bold: bool = False, highlight: bool = False) -> str:
    color = "#1E6FD9" if highlight else "#94A3B8"
    weight = "700" if bold else "500"
    return f'<span style="color:{color}; font-weight:{weight};">{value:.3f}</span>'


def _render_table(data: list[dict], winner: str = "Logistic Regression") -> None:
    df = pd.DataFrame(data)

    # Build HTML table
    cols = list(df.columns)
    header = "".join(f"<th>{c}</th>" for c in cols)
    rows = ""
    for _, row in df.iterrows():
        is_winner = row.get("Model", row.get("Model", "")) == winner
        row_style = "background:rgba(30,111,217,0.07);" if is_winner else ""
        cells = ""
        for c in cols:
            v = row[c]
            if isinstance(v, float):
                val_str = _metric_pill(v, highlight=(is_winner and c != "Model"))
            else:
                val_str = (
                    f'<span style="color:#F0F4FF; font-weight:600;">{v}</span>'
                    if c == "Model" else f'<span style="color:#94A3B8;">{v}</span>'
                )
            if is_winner and c == "Model":
                val_str += ' <span class="model-winner-badge" style="margin-left:6px; font-size:10px;">★ SELECTED</span>'
            cells += f"<td>{val_str}</td>"
        rows += f"<tr style='{row_style}'>{cells}</tr>"

    html = f"""
    <div style="overflow-x:auto;">
      <table class="styled-table">
        <thead><tr>{header}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render():
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
      <div class="page-header-eyebrow">TERMORA — MODEL INSIGHTS</div>
      <div class="page-header-title">Model Insights</div>
      <div class="page-header-desc">
        Evaluation of five candidate classifiers on the Bank Marketing dataset.
        Logistic Regression was selected as the production model based on generalised
        ROC-AUC performance and training stability.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Winner summary card ───────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card" style="border-color:rgba(245,158,11,0.25);">
      <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
        <div>
          <div class="section-card-title" style="font-size:16px; margin-bottom:4px;">
            <span class="model-winner-badge">★ SELECTED MODEL</span>
          </div>
          <div style="font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:700;
                      color:#F0F4FF; margin:6px 0;">
            Logistic Regression
          </div>
          <div style="font-size:13px; color:#94A3B8; line-height:1.65; max-width:700px;">
            Chosen for highest generalised ROC-AUC (0.801) on the held-out test set,
            lowest cross-validation standard deviation (±0.006), zero overfitting,
            and sub-5-second training time suitable for real-time deployment.
            Class imbalance is addressed via <em>class_weight='balanced'</em>.
          </div>
        </div>
        <div style="display:flex; gap:16px; flex-wrap:wrap; margin-left:auto;">
          <div class="metric-card" style="padding:14px 20px; min-width:100px; text-align:center;">
            <div class="metric-label">Test ROC-AUC</div>
            <div class="metric-value" style="font-size:24px; color:#1E6FD9;">0.801</div>
          </div>
          <div class="metric-card" style="padding:14px 20px; min-width:100px; text-align:center;">
            <div class="metric-label">Recall</div>
            <div class="metric-value" style="font-size:24px; color:#0D9488;">0.644</div>
          </div>
          <div class="metric-card" style="padding:14px 20px; min-width:100px; text-align:center;">
            <div class="metric-label">Accuracy</div>
            <div class="metric-value" style="font-size:24px; color:#10B981;">0.833</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "  Baseline Comparison  ",
        "  Cross-Validation  ",
        "  Hyperparameter Tuning  ",
        "  Visual Comparison  ",
    ])

    with tab1:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-card-title" style="margin-bottom:12px;">Baseline Model Evaluation</div>
        <div class="section-card-desc" style="margin-bottom:16px;">
          All models trained with default hyperparameters on an 80/20 stratified split.
          Evaluated on the held-out test set (8,238 records).
        </div>
        """, unsafe_allow_html=True)
        _render_table(BASELINE_RESULTS)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-callout">
          <strong style="color:#F0F4FF;">Why not Random Forest?</strong> While Random Forest
          achieves the highest accuracy (0.895) and F1 (0.485), it shows severe overfitting
          and its CV ROC-AUC (0.771) is significantly lower than its test score.
          Logistic Regression achieves the highest <em>generalised</em> ROC-AUC with
          no overfitting and the lowest variance — making it the safer production choice.
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-card-title" style="margin-bottom:12px;">5-Fold Stratified Cross-Validation</div>
        <div class="section-card-desc" style="margin-bottom:16px;">
          Stratified K-Fold (k=5) on the training set (32,950 records).
          Std Dev quantifies model stability across different data splits.
        </div>
        """, unsafe_allow_html=True)
        _render_table(CV_RESULTS)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.plotly_chart(cv_stability_chart(CV_RESULTS), width="stretch",
                        config={"displayModeBar": False})

        st.markdown("""
        <div class="info-callout" style="margin-top:8px;">
          The error bars represent ± 1 standard deviation across 5 CV folds.
          Logistic Regression and Random Forest show the most stable results.
          SVC has the highest variance (±0.018), indicating sensitivity to data splits.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-card-title" style="margin-bottom:12px;">Hyperparameter Tuning Results</div>
        <div class="section-card-desc" style="margin-bottom:16px;">
          Randomised search with 3-fold CV, optimising for ROC-AUC.
          Best parameters and resulting test-set scores shown below.
        </div>
        """, unsafe_allow_html=True)

        # Separate params from scores for better display
        display_cols = [
            {"Model": r["Model"], "Best CV ROC-AUC": r["Best CV ROC-AUC"],
             "Test Accuracy": r["Test Accuracy"], "Test Precision": r["Test Precision"],
             "Test Recall": r["Test Recall"], "Test F1": r["Test F1"],
             "Test ROC-AUC": r["Test ROC-AUC"]}
            for r in TUNING_RESULTS
        ]
        _render_table(display_cols)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Best params callout
        st.markdown("""
        <div class="section-card-title" style="margin:16px 0 10px; font-size:14px;">
          Best Hyperparameters per Model
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(len(TUNING_RESULTS))
        palette = ["#1E6FD9", "#0D9488", "#8B5CF6", "#F59E0B", "#10B981"]
        for col, row, clr in zip(cols, TUNING_RESULTS, palette):
            with col:
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid rgba({','.join(str(int(clr.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.25);
                             border-radius:10px; padding:14px; height:100%;">
                  <div style="font-size:12px; font-weight:700; color:{clr}; margin-bottom:8px;">{row['Model']}</div>
                  <div style="font-size:11px; color:#94A3B8; line-height:1.7;">{row['Best Params']}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab4:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        metric_choice = st.selectbox(
            "Select metric for bar comparison",
            ["ROC-AUC", "Accuracy", "Precision", "Recall", "F1-Score"],
            key="metric_bar_select",
        )

        col_radar, col_bar = st.columns([1, 1])
        with col_radar:
            st.plotly_chart(model_comparison_radar(BASELINE_RESULTS),
                            width="stretch", config={"displayModeBar": False})

        with col_bar:
            st.plotly_chart(model_bar_comparison(BASELINE_RESULTS, metric=metric_choice),
                            width="stretch", config={"displayModeBar": False})

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Model overview cards ──────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header" style="margin-top:12px;">
      <div class="page-header-eyebrow">MODELS EVALUATED</div>
      <div class="page-header-title">Candidate Classifiers</div>
    </div>
    """, unsafe_allow_html=True)

    models_info = [
        ("Logistic Regression", "#1E6FD9", "Linear boundary classifier. Best generalisation and interpretability. Selected for production.", True),
        ("Decision Tree",       "#0D9488", "Rule-based tree. Highly interpretable but prone to severe overfitting on this dataset.",        False),
        ("K-Nearest Neighbors", "#8B5CF6", "Instance-based classifier. Moderate performance; computationally expensive at prediction time.", False),
        ("Support Vector Classification", "#F59E0B", "Margin-maximising classifier. Requires long training; unstable CV performance here.",   False),
        ("Random Forest",       "#10B981", "Ensemble of trees. High accuracy but significant overfitting; CV gap too wide for deployment.",   False),
    ]

    cols = st.columns(len(models_info))
    for col, (name, clr, desc, selected) in zip(cols, models_info):
        with col:
            border = f"rgba({','.join(str(int(clr.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.35)"
            winner_label = '<div class="model-winner-badge" style="margin-top:8px; font-size:10px;">★ SELECTED</div>' if selected else ""
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid {border};
                        border-radius:12px; padding:16px; height:100%; text-align:center;">
              <div style="font-size:12px; font-weight:700; color:{clr}; margin-bottom:8px; line-height:1.3;">{name}</div>
              <div style="font-size:11px; color:#94A3B8; line-height:1.65;">{desc}</div>
              {winner_label}
            </div>
            """, unsafe_allow_html=True)
