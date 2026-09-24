"""
termora/pages/assessment.py
============================
Customer Assessment page — 3-section form + prediction result.
"""

import streamlit as st
import pandas as pd
from termora.utils.model_loader import predict
from termora.utils.charts import gauge_chart
from termora.config import (
    JOB_OPTIONS, MARITAL_OPTIONS, EDUCATION_OPTIONS, EDUCATION_LABELS,
    DEFAULT_YESNO, CONTACT_OPTIONS, MONTH_OPTIONS, MONTH_LABELS,
    DAY_OPTIONS, DAY_LABELS, POUTCOME_OPTIONS, POUTCOME_LABELS,
)


def _label(options: list, labels: dict) -> list:
    return [labels.get(o, o.title()) for o in options]


def render():
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
      <div class="page-header-eyebrow">TERMORA — ASSESSMENT</div>
      <div class="page-header-title">Customer Assessment</div>
      <div class="page-header-desc">
        Fill in the customer's profile, contact details, and economic context.
        Termora will estimate the likelihood of term-deposit subscription.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION 1: Customer Profile ───────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-card-title">
        <span class="step-badge">Section 1</span>
        Customer Profile
      </div>
      <div class="section-card-desc">Demographic and financial background of the customer.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age", min_value=18, max_value=100, value=35, step=1)

        edu_label = st.selectbox(
            "Education Level",
            options=_label(EDUCATION_OPTIONS, EDUCATION_LABELS),
            index=6,
        )
        edu = EDUCATION_OPTIONS[_label(EDUCATION_OPTIONS, EDUCATION_LABELS).index(edu_label)]

        housing = st.selectbox("Housing Loan", options=DEFAULT_YESNO, format_func=str.title)

    with c2:
        job_label = st.selectbox(
            "Occupation",
            options=[o.replace(".", "").title() if o != "unknown" else "Unknown" for o in JOB_OPTIONS],
        )
        job_idx = [o.replace(".", "").title() if o != "unknown" else "Unknown" for o in JOB_OPTIONS].index(job_label)
        job = JOB_OPTIONS[job_idx]

        credit = st.selectbox("Credit Default History", options=DEFAULT_YESNO, format_func=str.title, index=1)

        loan = st.selectbox("Personal Loan", options=DEFAULT_YESNO, format_func=str.title, index=1)

    with c3:
        marital = st.selectbox("Marital Status", options=MARITAL_OPTIONS, format_func=str.title)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(30,111,217,0.06); border:1px solid rgba(30,111,217,0.15);
                    border-radius:8px; padding:12px 14px; font-size:12px; color:#94A3B8; line-height:1.6;">
          <b style="color:#F0F4FF;">Credit Default</b> captures whether the customer
          has ever defaulted on a credit obligation — a key financial risk indicator.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECTION 2: Contact & Campaign ────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-card-title">
        <span class="step-badge">Section 2</span>
        Contact &amp; Campaign
      </div>
      <div class="section-card-desc">Details about how and when the customer was contacted during this campaign.</div>
    </div>
    """, unsafe_allow_html=True)

    ca, cb, cc = st.columns(3)

    with ca:
        contact = st.selectbox(
            "Contact Method",
            options=CONTACT_OPTIONS,
            format_func=lambda x: "Mobile Phone" if x == "cellular" else "Landline",
        )

        month_label = st.selectbox(
            "Contact Month",
            options=list(MONTH_LABELS.values()),
            index=4,
        )
        month = MONTH_OPTIONS[list(MONTH_LABELS.values()).index(month_label)]

        day_label = st.selectbox(
            "Contact Day of Week",
            options=list(DAY_LABELS.values()),
        )
        day = DAY_OPTIONS[list(DAY_LABELS.values()).index(day_label)]

    with cb:
        campaign = st.number_input("Campaign Contacts (this campaign)", min_value=1, max_value=60, value=2, step=1)

        pdays = st.number_input(
            "Days Since Previous Contact",
            min_value=0, max_value=999, value=999, step=1,
            help="Enter 999 if the customer was not previously contacted.",
        )

        previous = st.number_input("Previous Campaign Contacts", min_value=0, max_value=30, value=0, step=1)

    with cc:
        pout_label = st.selectbox(
            "Previous Campaign Outcome",
            options=list(POUTCOME_LABELS.values()),
        )
        poutcome = POUTCOME_OPTIONS[list(POUTCOME_LABELS.values()).index(pout_label)]

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(13,148,136,0.06); border:1px solid rgba(13,148,136,0.18);
                    border-radius:8px; padding:12px 14px; font-size:12px; color:#94A3B8; line-height:1.6;">
          <b style="color:#F0F4FF;">Tip:</b> If this is the first ever contact with the customer,
          set <em>Days Since Previous Contact</em> to <b>999</b> and
          <em>Previous Campaign Contacts</em> to <b>0</b>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECTION 3: Economic Context ───────────────────────────────────────────
    st.markdown("""
    <div class="section-card">
      <div class="section-card-title">
        <span class="step-badge">Section 3</span>
        Economic Context
      </div>
      <div class="section-card-desc">
        Macroeconomic indicators at the time of contact. These are automatically
        available from national statistical agencies and banking system data.
      </div>
    </div>
    """, unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)

    with e1:
        emp_var = st.number_input(
            "Employment Variation Rate (%)",
            min_value=-4.0, max_value=4.0, value=1.1, step=0.1, format="%.1f",
            help="Quarterly employment variation rate. Typically ranges from -3.4 to +1.4.",
        )
        cpi = st.number_input(
            "Consumer Price Index",
            min_value=92.0, max_value=95.0, value=93.994, step=0.001, format="%.3f",
        )

    with e2:
        cci = st.number_input(
            "Consumer Confidence Index",
            min_value=-55.0, max_value=-25.0, value=-36.4, step=0.1, format="%.1f",
        )
        euribor = st.number_input(
            "Euribor 3-Month Rate (%)",
            min_value=0.5, max_value=6.0, value=4.857, step=0.001, format="%.3f",
        )

    with e3:
        nr_employed = st.number_input(
            "Number of Bank Employees (thousands)",
            min_value=4900.0, max_value=5300.0, value=5191.0, step=0.1, format="%.1f",
        )
        st.markdown("""
        <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.18);
                    border-radius:8px; padding:12px 14px; font-size:12px; color:#94A3B8;
                    line-height:1.6; margin-top:8px;">
          <b style="color:#F59E0B;">Economic context</b> significantly influences
          subscription behaviour. Lower Euribor rates and negative employment
          variation are historically linked to higher subscription rates.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Prediction button ─────────────────────────────────────────────────────
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        assess = st.button("Assess Customer", key="assess_btn", width="stretch")

    if assess:
        input_data = {
            "Age":                        int(age),
            "Job":                        job,
            "Marital Status":             marital,
            "Education":                  edu,
            "Credit Default":             credit,
            "Housing Loan":               housing,
            "Personal Loan":              loan,
            "Contact Method":             contact,
            "Contact Month":              month,
            "Contact Day":                day,
            "Campaign Contacts":          int(campaign),
            "Days Since Previous Contact":int(pdays),
            "Previous Contacts":          int(previous),
            "Previous Campaign Outcome":  poutcome,
            "Employment Variation Rate":  float(emp_var),
            "Consumer Price Index":       float(cpi),
            "Consumer Confidence Index":  float(cci),
            "Euribor 3 Month Rate":       float(euribor),
            "Number of Employees":        float(nr_employed),
        }

        with st.spinner("Running assessment…"):
            try:
                pred, proba = predict(input_data)
            except Exception as e:
                st.error(f"Assessment failed: {e}")
                return

        st.markdown("<hr>", unsafe_allow_html=True)
        _render_result(pred, proba, input_data)


def _render_result(pred: int, proba: float, inp: dict):
    """Render the professional result card."""
    pct = proba * 100

    if pct >= 65:
        band_color = "#10B981"
        verdict    = "Likely to Subscribe"
        badge_bg   = "rgba(16,185,129,0.15)"
        badge_border = "rgba(16,185,129,0.35)"
        glow_color = "rgba(16,185,129,0.15)"
        interpretation = (
            "Based on this customer's profile and current economic conditions, the model estimates "
            f"a <strong>{pct:.0f}%</strong> probability of term-deposit subscription. "
            "The combination of favourable campaign history, contact channel, and macroeconomic indicators "
            "suggests a strong candidate for outreach. Prioritising this customer is recommended."
        )
    elif pct >= 40:
        band_color = "#F59E0B"
        verdict    = "Moderate Likelihood"
        badge_bg   = "rgba(245,158,11,0.12)"
        badge_border = "rgba(245,158,11,0.30)"
        glow_color = "rgba(245,158,11,0.10)"
        interpretation = (
            f"The estimated subscription probability is <strong>{pct:.0f}%</strong>. "
            "This customer sits in an uncertain zone — neither a clear yes nor a clear no. "
            "Consider scheduling a follow-up call with tailored messaging. "
            "Improving contact timing or reducing campaign contact frequency may strengthen the response."
        )
    else:
        band_color = "#EF4444"
        verdict    = "Unlikely to Subscribe"
        badge_bg   = "rgba(239,68,68,0.12)"
        badge_border = "rgba(239,68,68,0.28)"
        glow_color = "rgba(239,68,68,0.10)"
        interpretation = (
            f"The estimated subscription probability is <strong>{pct:.0f}%</strong>. "
            "This customer's profile, combined with current economic conditions, suggests "
            "a low propensity for term-deposit subscription at this time. "
            "Resources may be better directed toward higher-probability customers."
        )

    # ── Result header ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:6px;">
      <div class="page-header-eyebrow" style="margin-bottom:6px;">CUSTOMER ASSESSMENT RESULT</div>
    </div>
    """, unsafe_allow_html=True)

    # Gauge + probability + verdict
    col_g, col_info = st.columns([1, 1])

    with col_g:
        st.html(f"""<div style="background:var(--bg-card); border:1px solid rgba({','.join(str(int(band_color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.35);
            border-radius:20px; padding:28px 20px; text-align:center; box-shadow:var(--shadow-lg); margin-bottom:12px;">
  <div class="result-badge" style="background:{badge_bg}; border:1px solid {badge_border}; color:{band_color};">
    {'HIGH PROBABILITY' if pct >= 65 else 'MODERATE PROBABILITY' if pct >= 40 else 'LOW PROBABILITY'}
  </div>
  <div class="result-probability" style="color:{band_color};">{pct:.1f}%</div>
  <div class="result-label">{verdict}</div>
  <div class="result-sublabel">to Term Deposit Subscription</div>
  <div style="margin:14px 10px 6px;">
    <div style="display:flex; justify-content:space-between; font-size:10px; color:#64748B; margin-bottom:5px;">
      <span>Low</span><span>Subscription Likelihood</span><span>High</span>
    </div>
    <div style="background:rgba(255,255,255,0.06); border-radius:50px; height:8px; overflow:hidden;">
      <div style="width:{pct:.1f}%; height:100%; background:{band_color}; border-radius:50px;
                  box-shadow:0 0 10px {band_color}44;"></div>
    </div>
  </div>
</div>""")

        # Gauge chart
        st.plotly_chart(gauge_chart(proba), width="stretch", config={"displayModeBar": False})

    with col_info:
        edu_display  = {
            "illiterate": "Illiterate", "basic.4y": "Primary (4y)", "basic.6y": "Primary (6y)",
            "basic.9y": "Junior High", "high.school": "High School",
            "professional.course": "Professional Course", "university.degree": "University Degree",
            "unknown": "Unknown",
        }.get(inp["Education"], inp["Education"])

        contact_display = "Mobile Phone" if inp["Contact Method"] == "cellular" else "Landline"
        job_display = inp["Job"].replace(".", "").title()

        # Customer snapshot
        st.markdown("""
        <div style="font-size:13px; font-weight:700; color:#F0F4FF; margin-bottom:12px;
                    padding-top:6px; letter-spacing:0.3px;">
          Customer Snapshot
        </div>
        """, unsafe_allow_html=True)

        snapshot_items = [
            ("Age",                inp["Age"]),
            ("Occupation",         job_display),
            ("Education",          edu_display),
            ("Marital Status",     inp["Marital Status"].title()),
            ("Contact Method",     contact_display),
            ("Campaign Contacts",  inp["Campaign Contacts"]),
            ("Euribor Rate",       f"{inp['Euribor 3 Month Rate']:.3f}%"),
            ("Empl. Variation",    f"{inp['Employment Variation Rate']:.1f}%"),
        ]

        for label, value in snapshot_items:
            st.markdown(f"""
            <div class="snapshot-card">
              <span class="snapshot-label">{label}</span>
              <span class="snapshot-value">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Interpretation ────────────────────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section-card">
      <div class="section-card-title" style="margin-bottom:12px;">Prediction Interpretation</div>
      <div class="info-callout">
        {interpretation}
      </div>
      <div style="margin-top:14px; font-size:11px; color:#64748B; line-height:1.7;">
        This estimate is produced by a Logistic Regression model (ROC-AUC: 0.801) trained on
        41,188 historical bank marketing contacts. The model uses customer demographics,
        campaign metadata, and macroeconomic indicators. Call duration was excluded to prevent
        data leakage. Class imbalance is corrected using balanced class weighting.
      </div>
    </div>
    """, unsafe_allow_html=True)
