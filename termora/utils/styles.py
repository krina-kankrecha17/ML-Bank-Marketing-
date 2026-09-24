"""
termora/utils/styles.py
=======================
All custom CSS for the Termora Streamlit application.
Injected once via st.markdown(..., unsafe_allow_html=True).
"""


def get_global_css() -> str:
    return """
<style>
/* =========================================================
   GOOGLE FONTS
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* =========================================================
   RESET & ROOT
   ========================================================= */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --navy:          #0A1628;
  --navy-light:    #0F2040;
  --navy-card:     #111D35;
  --accent:        #1E6FD9;
  --accent-soft:   #2B82F0;
  --teal:          #0D9488;
  --teal-soft:     #14B8A6;
  --gold:          #F59E0B;
  --success:       #10B981;
  --danger:        #EF4444;
  --text-primary:  #F0F4FF;
  --text-secondary:#94A3B8;
  --text-muted:    #64748B;
  --border:        #1E2D4A;
  --bg-card:       #0D1B2E;
  --radius:        14px;
  --radius-sm:     8px;
  --shadow:        0 4px 24px rgba(0,0,0,0.35);
  --shadow-lg:     0 8px 40px rgba(0,0,0,0.50);
}

/* =========================================================
   APP-WIDE BASE
   ========================================================= */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background-color: var(--navy) !important;
  color: var(--text-primary) !important;
  font-family: 'Inter', sans-serif !important;
}

[data-testid="stMain"] {
  background-color: var(--navy) !important;
}

[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

/* =========================================================
   SCROLLBAR
   ========================================================= */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* =========================================================
   SIDEBAR
   ========================================================= */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070F1D 0%, #0A1628 60%, #081524 100%) !important;
  border-right: 1px solid var(--border) !important;
  width: 270px !important;
}

[data-testid="stSidebarContent"] { padding: 0 !important; }

.sidebar-brand {
  padding: 28px 24px 20px;
  border-bottom: 1px solid var(--border);
}

.sidebar-logo {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 3px;
  background: linear-gradient(135deg, #1E6FD9 0%, #14B8A6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-subtitle {
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 1.5px;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-top: 4px;
}

.sidebar-status {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 16px;
  margin: 14px 16px;
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 20px;
  font-size: 11px;
  color: #10B981;
  font-weight: 500;
}

.status-dot {
  width: 7px; height: 7px;
  background: #10B981;
  border-radius: 50%;
  box-shadow: 0 0 6px #10B981;
  animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
  0%, 100% { opacity: 1; box-shadow: 0 0 6px #10B981; }
  50%       { opacity: 0.6; box-shadow: 0 0 12px #10B981; }
}

.sidebar-nav-label {
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  padding: 14px 24px 6px;
}

/* hide default Streamlit radio styling */
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio label {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  padding: 10px 20px !important;
  margin: 1px 8px !important;
  border-radius: var(--radius-sm) !important;
  cursor: pointer !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--text-secondary) !important;
  transition: all 0.2s ease !important;
  border: 1px solid transparent !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(30,111,217,0.10) !important;
  color: var(--text-primary) !important;
  border-color: rgba(30,111,217,0.2) !important;
}

[data-testid="stSidebar"] .stRadio [data-checked="true"] > label,
[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
  background: rgba(30,111,217,0.18) !important;
  color: var(--accent-soft) !important;
  border-color: rgba(30,111,217,0.35) !important;
}

/* hide radio circles */
[data-testid="stSidebar"] .stRadio [role="radio"] { display: none !important; }
[data-testid="stSidebar"] .stRadio p { font-size: 13px !important; margin: 0 !important; }

/* =========================================================
   HIDE STREAMLIT CHROME
   ========================================================= */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* =========================================================
   CONTENT PADDING
   ========================================================= */
.main .block-container {
  padding: 28px 36px 48px !important;
  max-width: 1280px !important;
}

/* =========================================================
   TYPOGRAPHY
   ========================================================= */
h1, h2, h3, h4, h5 {
  font-family: 'Space Grotesk', sans-serif !important;
  color: var(--text-primary) !important;
}

/* =========================================================
   CUSTOM COMPONENTS
   ========================================================= */

/* Page header */
.page-header {
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}
.page-header-eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 8px;
}
.page-header-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}
.page-header-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 8px;
  line-height: 1.6;
  max-width: 640px;
}

/* Metric card */
.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px 24px;
  box-shadow: var(--shadow);
  transition: transform 0.2s ease, border-color 0.2s ease;
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent) 0%, var(--teal) 100%);
}
.metric-card:hover {
  transform: translateY(-2px);
  border-color: rgba(30,111,217,0.35);
}
.metric-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 10px;
}
.metric-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}
.metric-sub {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
}

/* Hero section */
.hero-section {
  background: linear-gradient(135deg, #0A1628 0%, #0F2040 50%, #0A1628 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 52px 52px 44px;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(30,111,217,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.hero-section::after {
  content: '';
  position: absolute;
  bottom: -60px; left: -60px;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(13,148,136,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 14px;
}
.hero-headline {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.25;
  max-width: 600px;
  margin-bottom: 16px;
}
.hero-description {
  font-size: 15px;
  color: var(--text-secondary);
  max-width: 560px;
  line-height: 1.7;
  margin-bottom: 28px;
}

/* CTA button */
.cta-button-wrapper a, .cta-button-wrapper button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #1E6FD9 0%, #2B82F0 100%);
  color: #fff !important;
  font-weight: 600;
  font-size: 14px;
  padding: 13px 28px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  text-decoration: none !important;
  box-shadow: 0 4px 16px rgba(30,111,217,0.35);
  transition: all 0.2s ease;
}
.cta-button-wrapper a:hover, .cta-button-wrapper button:hover {
  box-shadow: 0 6px 24px rgba(30,111,217,0.55);
  transform: translateY(-1px);
}

/* Section card */
.section-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 28px;
  margin-bottom: 18px;
  box-shadow: var(--shadow);
}
.section-card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-card-title .step-badge {
  background: rgba(30,111,217,0.18);
  border: 1px solid rgba(30,111,217,0.3);
  color: var(--accent-soft);
  font-size: 11px;
  font-weight: 700;
  padding: 2px 9px;
  border-radius: 20px;
}
.section-card-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

/* Result card */
.result-card {
  background: linear-gradient(135deg, #0A1628 0%, #0F2040 100%);
  border: 1px solid rgba(30,111,217,0.3);
  border-radius: 20px;
  padding: 36px 40px;
  text-align: center;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
}
.result-card-glow {
  position: absolute;
  top: -60px; left: 50%;
  transform: translateX(-50%);
  width: 300px; height: 300px;
  border-radius: 50%;
  pointer-events: none;
}
.result-badge {
  display: inline-block;
  padding: 5px 16px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 14px;
}
.result-probability {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 64px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 8px;
}
.result-label {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.result-sublabel {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

/* Likelihood bar */
.likelihood-bar-wrapper {
  background: rgba(255,255,255,0.05);
  border-radius: 50px;
  height: 8px;
  margin: 10px 0;
  overflow: hidden;
}
.likelihood-bar-fill {
  height: 100%;
  border-radius: 50px;
  transition: width 0.6s ease;
}

/* Snapshot card */
.snapshot-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.snapshot-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}
.snapshot-value {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 600;
}

/* Info callout */
.info-callout {
  background: rgba(30,111,217,0.07);
  border: 1px solid rgba(30,111,217,0.2);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-sm);
  padding: 14px 18px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
}

/* Chart container */
.chart-container {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  margin-bottom: 18px;
}
.chart-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 14px;
}

/* Model badge */
.model-winner-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(245,158,11,0.05));
  border: 1px solid rgba(245,158,11,0.35);
  color: #F59E0B;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Table */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.styled-table thead th {
  background: rgba(30,111,217,0.12);
  color: var(--accent-soft);
  font-weight: 600;
  font-size: 11px;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 11px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.styled-table tbody tr {
  border-bottom: 1px solid rgba(30,45,74,0.5);
  transition: background 0.15s ease;
}
.styled-table tbody tr:hover { background: rgba(30,111,217,0.05); }
.styled-table tbody td {
  padding: 11px 16px;
  color: var(--text-secondary);
  vertical-align: middle;
}
.styled-table tbody td:first-child { color: var(--text-primary); font-weight: 500; }

/* Streamlit widget overrides */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: #0F2040 !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-size: 13px !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(30,111,217,0.15) !important;
}

label[data-testid="stWidgetLabel"] > div > p {
  font-size: 12px !important;
  font-weight: 600 !important;
  color: var(--text-secondary) !important;
  letter-spacing: 0.3px !important;
  text-transform: uppercase !important;
}

/* Slider */
.stSlider > div > div > div > div { background: var(--accent) !important; }

/* Button */
.stButton > button {
  background: linear-gradient(135deg, #1E6FD9 0%, #2B82F0 100%) !important;
  color: #fff !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 12px 28px !important;
  border: none !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 16px rgba(30,111,217,0.35) !important;
  transition: all 0.2s ease !important;
  font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
  box-shadow: 0 6px 24px rgba(30,111,217,0.55) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* Divider */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 24px 0 !important;
}

/* Plotly chart background fix */
.js-plotly-plot .plotly, .js-plotly-plot .plotly .svg-container {
  background: transparent !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

/* Spinner */
.stSpinner > div { border-color: var(--accent) transparent transparent !important; }

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--text-muted) !important;
  padding: 9px 20px !important;
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  background: transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--accent-soft) !important;
  border-bottom-color: var(--accent-soft) !important;
  font-weight: 600 !important;
}

/* About section */
.about-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 28px;
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}
.about-card h3 {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  margin-bottom: 10px !important;
}
.about-card p, .about-card li {
  font-size: 13.5px !important;
  color: var(--text-secondary) !important;
  line-height: 1.75 !important;
}
.about-card ul { padding-left: 18px; }
.about-card a { color: var(--accent-soft); text-decoration: none; }

/* Small badge */
.tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(30,111,217,0.15);
  border: 1px solid rgba(30,111,217,0.25);
  color: var(--accent-soft);
  margin-right: 4px;
  margin-bottom: 4px;
}
.tag-teal {
  background: rgba(13,148,136,0.12);
  border-color: rgba(13,148,136,0.25);
  color: var(--teal-soft);
}
.tag-gold {
  background: rgba(245,158,11,0.12);
  border-color: rgba(245,158,11,0.25);
  color: var(--gold);
}
</style>
"""
