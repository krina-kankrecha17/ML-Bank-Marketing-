"""
termora/config.py
=================
Central configuration for the Termora application.
All paths, colours, model metadata, and domain look-up tables live here.
"""

import os

# ---------------------------------------------------------------------------
# Paths (relative to the project root)
# ---------------------------------------------------------------------------
ROOT_DIR   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Model path (primary: model/ directory; fallback: project root)
_primary_model = os.path.join(ROOT_DIR, "model", "bank_marketing_model.pkl")
MODEL_PATH     = _primary_model if os.path.exists(_primary_model) else os.path.join(ROOT_DIR, "bank_marketing_model.pkl")

# Meta path (primary: model/ directory; fallback: project root)
_primary_meta = os.path.join(ROOT_DIR, "model", "model_meta.json")
META_PATH     = _primary_meta if os.path.exists(_primary_meta) else os.path.join(ROOT_DIR, "model_meta.json")

# Data path (primary: data/ directory; fallback: bank+marketing nested dir)
_primary_data = os.path.join(ROOT_DIR, "data", "bank-additional-full.csv")
DATA_PATH     = _primary_data if os.path.exists(_primary_data) else os.path.join(
    ROOT_DIR, "bank+marketing", "bank-additional", "bank-additional", "bank-additional-full.csv"
)

# ---------------------------------------------------------------------------
# Brand colours
# ---------------------------------------------------------------------------
COLORS = {
    "navy":        "#0A1628",
    "navy_light":  "#0F2040",
    "navy_card":   "#111D35",
    "accent":      "#1E6FD9",
    "accent_soft": "#2B82F0",
    "teal":        "#0D9488",
    "teal_soft":   "#14B8A6",
    "gold":        "#F59E0B",
    "success":     "#10B981",
    "danger":      "#EF4444",
    "warning":     "#F59E0B",
    "text_primary":   "#F0F4FF",
    "text_secondary": "#94A3B8",
    "text_muted":     "#64748B",
    "border":      "#1E2D4A",
    "bg_card":     "#0D1B2E",
    "bg_input":    "#0F2040",
    "white":       "#FFFFFF",
    "chart_palette": [
        "#1E6FD9", "#0D9488", "#F59E0B", "#8B5CF6",
        "#EC4899", "#10B981", "#EF4444", "#06B6D4"
    ],
}

# ---------------------------------------------------------------------------
# Hard-coded model performance data (from build_final_model.py output)
# ---------------------------------------------------------------------------
BASELINE_RESULTS = [
    {"Model": "Logistic Regression",        "Accuracy": 0.8330, "Precision": 0.3637, "Recall": 0.6444, "F1-Score": 0.4650, "ROC-AUC": 0.8013},
    {"Model": "Decision Tree",              "Accuracy": 0.8717, "Precision": 0.4661, "Recall": 0.3852, "F1-Score": 0.4218, "ROC-AUC": 0.6278},
    {"Model": "K-Nearest Neighbors",        "Accuracy": 0.8860, "Precision": 0.5622, "Recall": 0.3378, "F1-Score": 0.4217, "ROC-AUC": 0.7393},
    {"Model": "Support Vector Classification", "Accuracy": 0.8836, "Precision": 0.5445, "Recall": 0.3185, "F1-Score": 0.4018, "ROC-AUC": 0.6846},
    {"Model": "Random Forest",              "Accuracy": 0.8952, "Precision": 0.6261, "Recall": 0.3956, "F1-Score": 0.4848, "ROC-AUC": 0.7841},
]

CV_RESULTS = [
    {"Model": "Logistic Regression",        "Mean CV Accuracy": 0.8321, "Mean CV Precision": 0.3620, "Mean CV Recall": 0.6390, "Mean CV F1": 0.4614, "Mean CV ROC-AUC": 0.7894, "Std Dev (ROC-AUC)": 0.0063},
    {"Model": "Decision Tree",              "Mean CV Accuracy": 0.8649, "Mean CV Precision": 0.4230, "Mean CV Recall": 0.3710, "Mean CV F1": 0.3953, "Mean CV ROC-AUC": 0.6248, "Std Dev (ROC-AUC)": 0.0083},
    {"Model": "K-Nearest Neighbors",        "Mean CV Accuracy": 0.8801, "Mean CV Precision": 0.5198, "Mean CV Recall": 0.3156, "Mean CV F1": 0.3930, "Mean CV ROC-AUC": 0.7185, "Std Dev (ROC-AUC)": 0.0082},
    {"Model": "Support Vector Classification", "Mean CV Accuracy": 0.8811, "Mean CV Precision": 0.5210, "Mean CV Recall": 0.3089, "Mean CV F1": 0.3883, "Mean CV ROC-AUC": 0.6722, "Std Dev (ROC-AUC)": 0.0182},
    {"Model": "Random Forest",              "Mean CV Accuracy": 0.8901, "Mean CV Precision": 0.5926, "Mean CV Recall": 0.3701, "Mean CV F1": 0.4559, "Mean CV ROC-AUC": 0.7708, "Std Dev (ROC-AUC)": 0.0068},
]

TUNING_RESULTS = [
    {"Model": "Logistic Regression",        "Best CV ROC-AUC": 0.7958, "Test Accuracy": 0.8330, "Test Precision": 0.3637, "Test Recall": 0.6444, "Test F1": 0.4650, "Test ROC-AUC": 0.8013, "Best Params": "C=1, class_weight=balanced, solver=liblinear"},
    {"Model": "Decision Tree",              "Best CV ROC-AUC": 0.6520, "Test Accuracy": 0.8781, "Test Precision": 0.4923, "Test Recall": 0.3778, "Test F1": 0.4274, "Test ROC-AUC": 0.6721, "Best Params": "max_depth=10, criterion=gini, class_weight=balanced"},
    {"Model": "K-Nearest Neighbors",        "Best CV ROC-AUC": 0.7237, "Test Accuracy": 0.8871, "Test Precision": 0.5705, "Test Recall": 0.3393, "Test F1": 0.4253, "Test ROC-AUC": 0.7467, "Best Params": "n_neighbors=15, weights=distance, metric=manhattan"},
    {"Model": "SVC",                        "Best CV ROC-AUC": 0.6793, "Test Accuracy": 0.8836, "Test Precision": 0.5445, "Test Recall": 0.3185, "Test F1": 0.4018, "Test ROC-AUC": 0.6893, "Best Params": "C=1, kernel=rbf, gamma=scale, class_weight=balanced"},
    {"Model": "Random Forest",              "Best CV ROC-AUC": 0.7731, "Test Accuracy": 0.8971, "Test Precision": 0.6398, "Test Recall": 0.3941, "Test F1": 0.4879, "Test ROC-AUC": 0.7902, "Best Params": "n_estimators=200, max_depth=20, class_weight=balanced"},
]

# ---------------------------------------------------------------------------
# Feature options for Customer Assessment form
# ---------------------------------------------------------------------------
JOB_OPTIONS = [
    "admin.", "blue-collar", "entrepreneur", "housemaid", "management",
    "retired", "self-employed", "services", "student", "technician",
    "unemployed", "unknown"
]

MARITAL_OPTIONS = ["married", "single", "divorced", "unknown"]

EDUCATION_OPTIONS = [
    "illiterate", "basic.4y", "basic.6y", "basic.9y",
    "high.school", "professional.course", "university.degree", "unknown"
]

EDUCATION_LABELS = {
    "illiterate":         "Illiterate",
    "basic.4y":           "Primary School (4 years)",
    "basic.6y":           "Primary School (6 years)",
    "basic.9y":           "Junior High School (9 years)",
    "high.school":        "High School",
    "professional.course":"Professional Course",
    "university.degree":  "University Degree",
    "unknown":            "Unknown",
}

DEFAULT_YESNO = ["yes", "no", "unknown"]

CONTACT_OPTIONS = ["cellular", "telephone"]

MONTH_OPTIONS = ["jan", "feb", "mar", "apr", "may", "jun",
                 "jul", "aug", "sep", "oct", "nov", "dec"]
MONTH_LABELS = {
    "jan": "January",   "feb": "February",  "mar": "March",
    "apr": "April",     "may": "May",        "jun": "June",
    "jul": "July",      "aug": "August",    "sep": "September",
    "oct": "October",   "nov": "November",  "dec": "December",
}

DAY_OPTIONS = ["mon", "tue", "wed", "thu", "fri"]
DAY_LABELS = {
    "mon": "Monday", "tue": "Tuesday", "wed": "Wednesday",
    "thu": "Thursday", "fri": "Friday",
}

POUTCOME_OPTIONS = ["nonexistent", "failure", "success"]
POUTCOME_LABELS = {
    "nonexistent": "No Previous Contact",
    "failure":     "Previous Campaign Failed",
    "success":     "Previous Campaign Succeeded",
}

# Feature order expected by the saved pipeline (from model_meta.json)
FEATURE_ORDER = [
    "Age", "Job", "Marital Status", "Education", "Credit Default",
    "Housing Loan", "Personal Loan", "Contact Method", "Contact Month",
    "Contact Day", "Campaign Contacts", "Days Since Previous Contact",
    "Previous Contacts", "Previous Campaign Outcome",
    "Employment Variation Rate", "Consumer Price Index",
    "Consumer Confidence Index", "Euribor 3 Month Rate", "Number of Employees"
]

# Human-readable feature descriptions for the Dataset page
FEATURE_INFO = [
    {"Feature": "Age",                      "Type": "Numeric",    "Description": "Customer age in years"},
    {"Feature": "Job",                      "Type": "Categorical","Description": "Type of occupation"},
    {"Feature": "Marital Status",           "Type": "Categorical","Description": "Marital status of the customer"},
    {"Feature": "Education",                "Type": "Ordinal",    "Description": "Highest level of education attained"},
    {"Feature": "Credit Default",           "Type": "Binary",     "Description": "Has the customer ever defaulted on credit?"},
    {"Feature": "Housing Loan",             "Type": "Binary",     "Description": "Does the customer have a housing loan?"},
    {"Feature": "Personal Loan",            "Type": "Binary",     "Description": "Does the customer have a personal loan?"},
    {"Feature": "Contact Method",           "Type": "Categorical","Description": "Channel used to contact the customer"},
    {"Feature": "Contact Month",            "Type": "Categorical","Description": "Month of the last contact in the campaign"},
    {"Feature": "Contact Day",              "Type": "Categorical","Description": "Day of the week of the last contact"},
    {"Feature": "Campaign Contacts",        "Type": "Numeric",    "Description": "Number of contacts during this campaign"},
    {"Feature": "Days Since Previous Contact","Type": "Numeric",  "Description": "Days since last contact in a prior campaign (999 = not contacted)"},
    {"Feature": "Previous Contacts",        "Type": "Numeric",    "Description": "Number of contacts before this campaign"},
    {"Feature": "Previous Campaign Outcome","Type": "Categorical","Description": "Outcome of the prior marketing campaign"},
    {"Feature": "Employment Variation Rate","Type": "Numeric",    "Description": "Quarterly employment variation rate (economic indicator)"},
    {"Feature": "Consumer Price Index",     "Type": "Numeric",    "Description": "Monthly consumer price index"},
    {"Feature": "Consumer Confidence Index","Type": "Numeric",    "Description": "Monthly consumer confidence index"},
    {"Feature": "Euribor 3 Month Rate",     "Type": "Numeric",    "Description": "Euro interbank lending rate (3-month)"},
    {"Feature": "Number of Employees",      "Type": "Numeric",    "Description": "Quarterly number of bank employees (economic indicator)"},
    {"Feature": "Term Deposit Subscription","Type": "Target",     "Description": "Did the customer subscribe to a term deposit? (Yes / No)"},
]
