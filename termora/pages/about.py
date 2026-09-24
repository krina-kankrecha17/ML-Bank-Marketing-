"""
termora/pages/about.py
=======================
About page — project purpose, dataset, workflow, models, and tech stack.
"""

import streamlit as st


def render():
    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
      <div class="page-header-eyebrow">TERMORA — ABOUT</div>
      <div class="page-header-title">About Termora</div>
      <div class="page-header-desc">
        A production-quality bank marketing intelligence platform built on
        classical machine learning and a modern fintech design system.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Project purpose ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="about-card">
      <h3>Project Purpose</h3>
      <p>
        Termora helps bank marketing teams evaluate the likelihood that a given customer
        will subscribe to a term deposit — before committing campaign resources to the call.
        Rather than presenting raw model output, Termora translates the classifier's output
        into a clear, actionable probability estimate with plain-language interpretation.
      </p>
      <p style="margin-top:10px;">
        The platform addresses a real business problem: direct marketing campaigns for
        term deposits are resource-intensive. Targeting customers with a higher propensity
        to subscribe reduces wasted contacts, lowers campaign cost, and improves
        customer experience by reducing unsolicited calls.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Two-column layout for dataset and ML workflow ─────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="about-card">
          <h3>Dataset</h3>
          <p>
            The <strong>UCI Bank Marketing dataset</strong> contains 41,188 records
            from direct phone-based marketing campaigns conducted by a Portuguese
            commercial bank between May 2008 and November 2010.
          </p>
          <ul style="margin-top:10px;">
            <li>20 input features: demographic, campaign, and economic</li>
            <li>Binary target: did the customer subscribe? (yes / no)</li>
            <li>Significant class imbalance: 88.7% No, 11.3% Yes</li>
            <li>'Call duration' excluded — it is a leaky feature
                (only available after the call ends)</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="about-card">
          <h3>Machine Learning Workflow</h3>
          <ul>
            <li><strong>EDA:</strong> Distribution analysis, correlation study,
                class imbalance assessment</li>
            <li><strong>Preprocessing:</strong> Median/mode imputation, RobustScaler
                for numerics, OneHotEncoder for nominals, OrdinalEncoder for education</li>
            <li><strong>Baseline evaluation:</strong> Five classifiers benchmarked
                on identical train/test splits</li>
            <li><strong>Cross-validation:</strong> 5-fold stratified CV on training
                data for generalisation assessment</li>
            <li><strong>Hyperparameter tuning:</strong> RandomisedSearchCV optimising
                ROC-AUC with 3-fold CV</li>
            <li><strong>Model selection:</strong> Logistic Regression — highest
                generalised ROC-AUC, lowest variance</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Models evaluated ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="about-card">
      <h3>Models Evaluated</h3>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:12px; margin-top:10px;">
        <div style="background:rgba(30,111,217,0.07); border:1px solid rgba(30,111,217,0.2);
                    border-radius:8px; padding:12px 16px;">
          <div style="font-weight:700; color:#1E6FD9; font-size:13px; margin-bottom:4px;">
            ★ Logistic Regression
          </div>
          <div style="font-size:11px; color:#94A3B8;">
            Selected · ROC-AUC: 0.801 · Stable · No overfitting
          </div>
        </div>
        <div style="background:rgba(13,148,136,0.06); border:1px solid rgba(13,148,136,0.15);
                    border-radius:8px; padding:12px 16px;">
          <div style="font-weight:700; color:#0D9488; font-size:13px; margin-bottom:4px;">
            Decision Tree
          </div>
          <div style="font-size:11px; color:#94A3B8;">
            ROC-AUC: 0.628 · Severe overfitting · Eliminated
          </div>
        </div>
        <div style="background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.15);
                    border-radius:8px; padding:12px 16px;">
          <div style="font-weight:700; color:#8B5CF6; font-size:13px; margin-bottom:4px;">
            K-Nearest Neighbors
          </div>
          <div style="font-size:11px; color:#94A3B8;">
            ROC-AUC: 0.739 · Moderate overfitting · Eliminated
          </div>
        </div>
        <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.15);
                    border-radius:8px; padding:12px 16px;">
          <div style="font-weight:700; color:#F59E0B; font-size:13px; margin-bottom:4px;">
            Support Vector Classification
          </div>
          <div style="font-size:11px; color:#94A3B8;">
            ROC-AUC: 0.685 · High variance · 219s training · Eliminated
          </div>
        </div>
        <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.15);
                    border-radius:8px; padding:12px 16px;">
          <div style="font-weight:700; color:#10B981; font-size:13px; margin-bottom:4px;">
            Random Forest
          </div>
          <div style="font-size:11px; color:#94A3B8;">
            ROC-AUC: 0.784 · Severe overfitting · CV gap too wide · Eliminated
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tech stack + evaluation ───────────────────────────────────────────────
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("""
        <div class="about-card">
          <h3>Evaluation Strategy</h3>
          <ul>
            <li><strong>Primary metric:</strong> ROC-AUC — threshold-independent
                ranking performance</li>
            <li><strong>Secondary:</strong> Recall — critical for minimising
                missed subscribers</li>
            <li><strong>Class imbalance:</strong> Corrected via
                <code>class_weight='balanced'</code> in Logistic Regression</li>
            <li><strong>Data leakage prevention:</strong> 80/20 stratified split
                performed before any preprocessing fit operations</li>
            <li><strong>Stability:</strong> Assessed via 5-fold stratified CV
                standard deviation across folds</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_d:
        st.markdown("""
        <div class="about-card">
          <h3>Technology Stack</h3>
          <ul>
            <li><strong>Data:</strong> pandas, NumPy</li>
            <li><strong>Preprocessing:</strong> scikit-learn pipelines
                (ColumnTransformer, SimpleImputer, RobustScaler,
                OneHotEncoder, OrdinalEncoder)</li>
            <li><strong>Models:</strong> scikit-learn classifiers</li>
            <li><strong>Serialisation:</strong> joblib (model pipeline pkl)</li>
            <li><strong>Frontend:</strong> Streamlit with custom CSS</li>
            <li><strong>Visualisation:</strong> Plotly (interactive charts)</li>
            <li><strong>Deployment target:</strong> Streamlit Community Cloud
                or containerised FastAPI + Streamlit stack</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Deployment note ───────────────────────────────────────────────────────
    
    # ── Footer ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:32px 0 16px; border-top:1px solid #1E2D4A; margin-top:24px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:18px; font-weight:700;
                  background:linear-gradient(135deg,#1E6FD9,#14B8A6);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  background-clip:text; margin-bottom:6px;">
        TERMORA
      </div>
      <div style="font-size:11px; color:#64748B; letter-spacing:1px;">
        BANK MARKETING INTELLIGENCE
      </div>
    </div>
    """, unsafe_allow_html=True)
