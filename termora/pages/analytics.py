"""
termora/pages/analytics.py
===========================
Campaign Analytics page — KPI row + 8 interactive Plotly charts.
"""

import streamlit as st
from termora.utils.data_loader import load_data, get_summary_stats
from termora.utils.charts import (
    subscription_donut,
    subscription_by_category,
    age_distribution,
    campaign_contacts_vs_subscription,
    poutcome_chart,
    correlation_heatmap,
)


def render():
    df    = load_data()
    stats = get_summary_stats(df)

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
      <div class="page-header-eyebrow">TERMORA — ANALYTICS</div>
      <div class="page-header-title">Campaign Analytics</div>
      <div class="page-header-desc">
        Explore historical campaign performance across customer segments, contact methods,
        and macroeconomic conditions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI row ───────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("Total Customers",    f"{stats['total_records']:,}",           "in the dataset"),
        ("Subscription Rate",  f"{stats['subscription_rate']:.1f}%",    "of contacts subscribed"),
        ("Average Age",        f"{stats['avg_age']:.0f} yrs",           "typical customer profile"),
        ("Avg. Call Duration", f"{stats['avg_duration']:.0f}s",         "per contact (excl. from model)"),
    ]
    for col, (label, val, sub) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{val}</div>
              <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Row 1: Donut + Job ───────────────────────────────────────────────────
    r1a, r1b = st.columns([1, 2])

    with r1a:
        st.plotly_chart(subscription_donut(df), width="stretch",
                        config={"displayModeBar": False})

    with r1b:
        st.plotly_chart(
            subscription_by_category(df, "Job", "Subscription by Occupation"),
            width="stretch", config={"displayModeBar": False},
        )

    # ── Row 2: Education + Contact Method ─────────────────────────────────────
    r2a, r2b = st.columns(2)

    with r2a:
        st.plotly_chart(
            subscription_by_category(df, "Education", "Subscription by Education Level"),
            width="stretch", config={"displayModeBar": False},
        )

    with r2b:
        st.plotly_chart(
            subscription_by_category(df, "Contact Method", "Subscription by Contact Method"),
            width="stretch", config={"displayModeBar": False},
        )

    # ── Row 3: Age Group + Month ───────────────────────────────────────────────
    r3a, r3b = st.columns(2)

    with r3a:
        st.plotly_chart(
            subscription_by_category(df, "Age Group", "Subscription by Age Group"),
            width="stretch", config={"displayModeBar": False},
        )

    with r3b:
        st.plotly_chart(age_distribution(df), width="stretch",
                        config={"displayModeBar": False})

    # ── Row 4: Campaign Contacts + poutcome ────────────────────────────────────
    r4a, r4b = st.columns(2)

    with r4a:
        st.plotly_chart(campaign_contacts_vs_subscription(df), width="stretch",
                        config={"displayModeBar": False})

    with r4b:
        st.plotly_chart(poutcome_chart(df), width="stretch",
                        config={"displayModeBar": False})

    # ── Full-width: Correlation heatmap ────────────────────────────────────────
    st.plotly_chart(correlation_heatmap(df), width="stretch",
                    config={"displayModeBar": False})

    # ── Key insights callout ─────────────────────────────────────────────────
    st.markdown("""
    <div class="info-callout" style="margin-top:8px;">
      <strong style="color:#F0F4FF;">Key Insights from Historical Data</strong><br><br>
      <strong>Contact method matters:</strong> Customers contacted via mobile phone subscribe at
      significantly higher rates than those reached by landline.<br><br>
      <strong>Previous success is the strongest signal:</strong> Customers with a successful prior
      campaign outcome subscribe at rates exceeding 60%, vs. &lt;8% for non-contacted customers.<br><br>
      <strong>Fewer calls, better results:</strong> Subscription rates decline sharply with increasing
      campaign contacts. One or two contacts typically yield the highest conversion rates.<br><br>
      <strong>Education correlates positively:</strong> Customers with university degrees and
      professional courses show the highest subscription propensity.
    </div>
    """, unsafe_allow_html=True)
