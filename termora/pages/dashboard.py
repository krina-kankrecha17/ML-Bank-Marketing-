"""
termora/pages/dashboard.py
===========================
Dashboard page — hero section, KPI cards, and CTA.
"""

import streamlit as st
from termora.utils.data_loader import load_data, get_summary_stats


def render():
    df    = load_data()
    stats = get_summary_stats(df)

    # ── Hero section ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
      <div class="hero-eyebrow">TERMORA — BANK MARKETING INTELLIGENCE</div>
      <div class="hero-headline">
        Understand customer response before the next campaign call.
      </div>
      <div class="hero-description">
        Evaluate customer and campaign characteristics to estimate the likelihood
        of term-deposit subscription. Designed for bank marketing teams who need
        clear, actionable intelligence — not raw model output.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI cards ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Customer Records</div>
          <div class="metric-value">{stats['total_records']:,}</div>
          <div class="metric-sub">in the training dataset</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Predictive Features</div>
          <div class="metric-value">19</div>
          <div class="metric-sub">demographic, campaign & economic</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Models Evaluated</div>
          <div class="metric-value">5</div>
          <div class="metric-sub">LR · DT · KNN · SVC · RF</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Best ROC-AUC</div>
          <div class="metric-value">0.801</div>
          <div class="metric-sub">Logistic Regression (selected)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-card" style="margin-top:18px;">
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
        <div>
          <div class="section-card-title" style="font-size:17px; margin-bottom:6px;">
            Ready to assess a customer?
          </div>
          <div class="section-card-desc" style="margin-bottom:0;">
            Enter customer details to receive a subscription likelihood estimate.
            The assessment uses the full trained pipeline — no retraining required.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Customer Assessment →", key="hero_cta"):
        st.session_state["target_page"] = "Customer Assessment"
        st.rerun()

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Quick-stats row ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header" style="margin-top:8px;">
      <div class="page-header-eyebrow">DATASET OVERVIEW</div>
      <div class="page-header-title">Campaign at a Glance</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Subscription Rate</div>
          <div class="metric-value" style="color:#1E6FD9;">{stats['subscription_rate']:.1f}%</div>
          <div class="metric-sub">of customers subscribed in historical data</div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Avg. Customer Age</div>
          <div class="metric-value" style="color:#0D9488;">{stats['avg_age']:.0f} yrs</div>
          <div class="metric-sub">median profile across all records</div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        sub_count = int(stats['subscribers'])
        non_count = int(stats['total_records']) - sub_count
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Class Imbalance</div>
          <div class="metric-value" style="font-size:22px; padding-top:4px;">
            <span style="color:#10B981;">{sub_count:,}</span>
            <span style="color:#64748B; font-size:18px;"> / </span>
            <span style="color:#EF4444;">{non_count:,}</span>
          </div>
          <div class="metric-sub">subscribers vs non-subscribers</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── How it works ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header" style="margin-top:8px;">
      <div class="page-header-eyebrow">WORKFLOW</div>
      <div class="page-header-title">How Termora Works</div>
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)

    steps = [
        ("01", "Input", "Enter customer demographic, contact, and economic context data."),
        ("02", "Preprocess", "Data is automatically encoded and scaled using the trained pipeline."),
        ("03", "Assess", "The Logistic Regression model computes a subscription probability."),
        ("04", "Interpret", "Results are presented as a clear likelihood estimate with context."),
    ]

    for col, (num, title, desc) in zip([w1, w2, w3, w4], steps):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding:20px;">
              <div style="font-family:'Space Grotesk',sans-serif; font-size:28px; font-weight:800;
                          background:linear-gradient(135deg,#1E6FD9,#14B8A6);
                          -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                          background-clip:text; margin-bottom:10px;">{num}</div>
              <div style="font-size:14px; font-weight:700; color:#F0F4FF; margin-bottom:6px;">{title}</div>
              <div style="font-size:12px; color:#94A3B8; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
