"""
app.py — Termora: Bank Marketing Intelligence
===============================================
Entry point for the Streamlit application.
Run with: streamlit run app.py
"""

import sys
import os

# Ensure the project root is on the Python path so `termora` is importable.
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from termora.utils.styles import get_global_css
from termora.pages import dashboard, assessment, analytics, model_insights, dataset, about

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Termora — Bank Marketing Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# INJECT GLOBAL CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(get_global_css(), unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand logo
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=220)
    else:
        st.markdown("""
        <div class="sidebar-brand">
          <div class="sidebar-logo">TERMORA</div>
          <div class="sidebar-subtitle">Bank Marketing Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

    # System status
    st.markdown("""
    <div class="sidebar-status">
      <div class="status-dot"></div>
      Model Ready
    </div>
    """, unsafe_allow_html=True)

    # Navigation label
    st.markdown('<div class="sidebar-nav-label">Navigation</div>', unsafe_allow_html=True)

    # Navigation (radio styled as a menu)
    nav_icons = {
        "Dashboard":          "◈",
        "Customer Assessment":"◉",
        "Campaign Analytics": "◎",
        "Model Insights":     "◇",
        "Dataset":            "◻",
        "About":              "◌",
    }

    pages = list(nav_icons.keys())
    labels = [f" {icon}  {name}" for name, icon in nav_icons.items()]

    # Handle external page navigation (e.g. hero CTA button)
    if "target_page" in st.session_state:
        target = st.session_state.pop("target_page")
        if target in pages:
            st.session_state["nav_radio"] = labels[pages.index(target)]

    if "nav_radio" not in st.session_state:
        st.session_state["nav_radio"] = labels[0]

    selection_label = st.radio(
        "nav",
        options=labels,
        label_visibility="collapsed",
        key="nav_radio",
    )

    # Map label back to page name
    selected_page = pages[labels.index(selection_label)]

    # Always sync session state with current radio selection
    st.session_state["page"] = selected_page

  

# ──────────────────────────────────────────────────────────────────────────────
# PAGE ROUTING
# ──────────────────────────────────────────────────────────────────────────────
_PAGE_ROUTER = {
    "Dashboard":          dashboard.render,
    "Customer Assessment":assessment.render,
    "Campaign Analytics": analytics.render,
    "Model Insights":     model_insights.render,
    "Dataset":            dataset.render,
    "About":              about.render,
}

render_fn = _PAGE_ROUTER.get(selected_page, dashboard.render)
render_fn()
