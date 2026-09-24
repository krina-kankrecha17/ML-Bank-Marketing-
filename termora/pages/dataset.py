"""
termora/pages/dataset.py
=========================
Dataset information page — metadata card, feature table, and sample data.
"""

import streamlit as st
from termora.config import FEATURE_INFO


def render():

    # ── Page header ───────────────────────────────────────────────────────────
    st.html("""<div class="page-header">
  <div class="page-header-eyebrow">TERMORA — DATASET</div>
  <div class="page-header-title">Dataset Overview</div>
  <div class="page-header-desc">
    The UCI Bank Marketing dataset records direct marketing campaign calls
    made by a Portuguese banking institution between 2008 and 2013.
  </div>
</div>""")

    # ── Dataset identity card ─────────────────────────────────────────────────
    d1, d2 = st.columns([2, 1])

    with d1:
        st.html("""<div class="section-card">
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px 32px;">
    <div>
      <div class="metric-label">Dataset</div>
      <div style="font-size:18px; font-weight:700; color:#F0F4FF; margin-top:4px;">Bank Marketing</div>
    </div>
    <div>
      <div class="metric-label">Source</div>
      <div style="font-size:14px; color:#94A3B8; margin-top:4px;">UCI Machine Learning Repository</div>
    </div>
    <div>
      <div class="metric-label">Records</div>
      <div style="font-size:18px; font-weight:700; color:#1E6FD9; margin-top:4px;">41,188</div>
    </div>
    <div>
      <div class="metric-label">Features</div>
      <div style="font-size:18px; font-weight:700; color:#0D9488; margin-top:4px;">20</div>
    </div>
    <div>
      <div class="metric-label">Problem Type</div>
      <div style="font-size:14px; color:#94A3B8; margin-top:4px;">Binary Classification</div>
    </div>
    <div>
      <div class="metric-label">Target Variable</div>
      <div style="font-size:14px; color:#94A3B8; margin-top:4px;">Term Deposit Subscription</div>
    </div>
    <div>
      <div class="metric-label">Class Distribution</div>
      <div style="font-size:14px; color:#94A3B8; margin-top:4px;">
        <span style="color:#EF4444; font-weight:600;">88.7%</span> No ·
        <span style="color:#10B981; font-weight:600;">11.3%</span> Yes
      </div>
    </div>
    <div>
      <div class="metric-label">Time Period</div>
      <div style="font-size:14px; color:#94A3B8; margin-top:4px;">May 2008 – November 2010</div>
    </div>
  </div>
</div>""")

    with d2:
        st.html("""<div class="section-card" style="height:100%;">
  <div class="section-card-title" style="margin-bottom:12px;">Feature Categories</div>
  <div style="display:flex; flex-direction:column; gap:10px;">
    <div>
      <div style="font-size:11px; font-weight:600; color:#64748B; margin-bottom:4px;">DEMOGRAPHIC (7)</div>
      <div style="font-size:12px; color:#94A3B8; line-height:1.6;">
        Age, Job, Marital Status, Education, Credit Default, Housing Loan, Personal Loan
      </div>
    </div>
    <div>
      <div style="font-size:11px; font-weight:600; color:#64748B; margin-bottom:4px;">CAMPAIGN (8)</div>
      <div style="font-size:12px; color:#94A3B8; line-height:1.6;">
        Contact Method, Month, Day, Campaign Contacts, Days Since Previous Contact,
        Previous Contacts, Previous Outcome <em style="color:#64748B;">(Call Duration excluded — leaky feature)</em>
      </div>
    </div>
    <div>
      <div style="font-size:11px; font-weight:600; color:#64748B; margin-bottom:4px;">ECONOMIC (5)</div>
      <div style="font-size:12px; color:#94A3B8; line-height:1.6;">
        Employment Variation Rate, Consumer Price Index, Consumer Confidence Index,
        Euribor 3-Month Rate, Number of Employees
      </div>
    </div>
  </div>
</div>""")

    # ── Feature information table ──────────────────────────────────────────────
    st.html("""<div class="page-header" style="margin-top:20px;">
  <div class="page-header-eyebrow">FEATURE REFERENCE</div>
  <div class="page-header-title">Feature Information</div>
</div>""")

    # Build HTML table cleanly with no indentation
    type_colors = {
        "Numeric":    ("#1E6FD9", "rgba(30,111,217,0.12)"),
        "Categorical":("#0D9488", "rgba(13,148,136,0.12)"),
        "Ordinal":    ("#8B5CF6", "rgba(139,92,246,0.12)"),
        "Binary":     ("#F59E0B", "rgba(245,158,11,0.12)"),
        "Target":     ("#EF4444", "rgba(239,68,68,0.12)"),
    }

    rows_parts = []
    for item in FEATURE_INFO:
        clr, bg = type_colors.get(item["Type"], ("#94A3B8", "rgba(148,163,184,0.1)"))
        rows_parts.append(
            f'<tr>'
            f'<td style="color:#F0F4FF; font-weight:600; padding:11px 16px; border-bottom:1px solid rgba(30,45,74,0.5);">{item["Feature"]}</td>'
            f'<td style="padding:11px 16px; border-bottom:1px solid rgba(30,45,74,0.5);">'
            f'<span style="background:{bg}; border:1px solid {clr}44; color:{clr}; font-size:10px; font-weight:700; padding:3px 10px; border-radius:20px; letter-spacing:0.5px;">{item["Type"].upper()}</span>'
            f'</td>'
            f'<td style="color:#94A3B8; padding:11px 16px; border-bottom:1px solid rgba(30,45,74,0.5);">{item["Description"]}</td>'
            f'</tr>'
        )
    rows_html = "".join(rows_parts)

    table_html = (
        f'<div style="overflow-x:auto; background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius); margin-bottom:28px;">'
        f'<table style="width:100%; border-collapse:collapse; font-size:13px;">'
        f'<thead>'
        f'<tr>'
        f'<th style="background:rgba(30,111,217,0.12); color:#2B82F0; font-weight:600; font-size:11px; letter-spacing:1px; text-transform:uppercase; padding:12px 16px; text-align:left; border-bottom:1px solid var(--border);">Feature Name</th>'
        f'<th style="background:rgba(30,111,217,0.12); color:#2B82F0; font-weight:600; font-size:11px; letter-spacing:1px; text-transform:uppercase; padding:12px 16px; text-align:left; border-bottom:1px solid var(--border);">Data Type</th>'
        f'<th style="background:rgba(30,111,217,0.12); color:#2B82F0; font-weight:600; font-size:11px; letter-spacing:1px; text-transform:uppercase; padding:12px 16px; text-align:left; border-bottom:1px solid var(--border);">Description</th>'
        f'</tr>'
        f'</thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table>'
        f'</div>'
    )
    st.html(table_html)


    # ── Preprocessing summary ──────────────────────────────────────────────────
    st.html("""<div class="section-card">
  <div class="section-card-title" style="margin-bottom:12px;">Preprocessing Pipeline</div>
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px;">
    <div>
      <div style="font-size:11px; font-weight:600; color:#1E6FD9; margin-bottom:6px; letter-spacing:1px;">
        NUMERIC FEATURES (9)
      </div>
      <div style="font-size:12px; color:#94A3B8; line-height:1.7;">
        • Median imputation for missing values<br>
        • Robust scaling (handles outliers)
      </div>
    </div>
    <div>
      <div style="font-size:11px; font-weight:600; color:#0D9488; margin-bottom:6px; letter-spacing:1px;">
        NOMINAL FEATURES (9)
      </div>
      <div style="font-size:12px; color:#94A3B8; line-height:1.7;">
        • Most-frequent imputation<br>
        • One-hot encoding (handle_unknown=ignore)
      </div>
    </div>
    <div>
      <div style="font-size:11px; font-weight:600; color:#8B5CF6; margin-bottom:6px; letter-spacing:1px;">
        ORDINAL FEATURES (1)
      </div>
      <div style="font-size:12px; color:#94A3B8; line-height:1.7;">
        • Most-frequent imputation<br>
        • Ordinal encoding (education level order preserved)
      </div>
    </div>
  </div>
</div>""")
