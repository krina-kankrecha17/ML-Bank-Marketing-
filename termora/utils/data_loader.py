"""
termora/utils/data_loader.py
=============================
Loads and caches the raw dataset, computes reusable derived columns,
and exposes helper functions for the analytics and dataset pages.
"""

import pandas as pd
import numpy as np
import streamlit as st
from termora.config import DATA_PATH


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load, rename, and enrich the dataset. Cached for the entire session."""
    df = pd.read_csv(DATA_PATH, sep=";")

    # Map target
    df["y"] = df["y"].map({"no": 0, "yes": 1})

    # Human-readable column names (same mapping used during training)
    rename_mapping = {
        "age":          "Age",
        "job":          "Job",
        "marital":      "Marital Status",
        "education":    "Education",
        "default":      "Credit Default",
        "housing":      "Housing Loan",
        "loan":         "Personal Loan",
        "contact":      "Contact Method",
        "month":        "Contact Month",
        "day_of_week":  "Contact Day",
        "duration":     "Call Duration",
        "campaign":     "Campaign Contacts",
        "pdays":        "Days Since Previous Contact",
        "previous":     "Previous Contacts",
        "poutcome":     "Previous Campaign Outcome",
        "emp.var.rate": "Employment Variation Rate",
        "cons.price.idx":"Consumer Price Index",
        "cons.conf.idx":"Consumer Confidence Index",
        "euribor3m":    "Euribor 3 Month Rate",
        "nr.employed":  "Number of Employees",
        "y":            "Term Deposit Subscription",
    }
    df.rename(columns=rename_mapping, inplace=True)

    # Replace 'unknown' strings with NaN
    df.replace("unknown", np.nan, inplace=True)

    # Derived: Age group buckets
    bins   = [17, 24, 34, 44, 54, 64, 120]
    labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

    # Derived: Subscription label
    df["Subscribed"] = df["Term Deposit Subscription"].map({1: "Yes", 0: "No"})

    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """Return high-level summary statistics for the dashboard."""
    return {
        "total_records":    len(df),
        "subscription_rate": df["Term Deposit Subscription"].mean() * 100,
        "avg_age":          df["Age"].mean(),
        "avg_duration":     df["Call Duration"].mean() if "Call Duration" in df.columns else 0,
        "subscribers":      df["Term Deposit Subscription"].sum(),
    }
