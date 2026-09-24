# TERMORA — Bank Marketing Intelligence

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Termora** is a production-grade machine learning platform for bank marketing intelligence. It evaluates prospective customer profiles, campaign interaction patterns, and macroeconomic conditions to estimate the likelihood of a term deposit subscription (`yes` / `no`).

Designed with modern fintech aesthetics, Termora delivers actionable intelligence directly to bank campaign managers, relationship officers, and marketing strategists before placing customer calls.

---

## Key Features

* **Executive Dashboard:** Real-time visibility into historical campaign performance, conversion rates, and predictive feature volume.
* **Customer Assessment:** Interactive, 3-section customer risk and subscription evaluation providing an instant likelihood percentage, decision band, and business recommendations.
* **Campaign Analytics:** Visual exploration of 8 critical distribution and relationship charts including occupation conversion, education, previous campaign outcome, and correlation matrices.
* **Model Insights:** Comparative evaluation across 5 classification architectures, including baseline test-set metrics, 5-fold stratified cross-validation stability, and hyperparameter tuning analysis.
* **Dataset Reference:** Comprehensive feature dictionary, category breakdown, data-type indicators, and preprocessing methodology documentation.
* **About Platform:** In-depth documentation covering the end-to-end data science lifecycle, business context, and deployment architecture.

---

## Machine Learning Architecture

The predictive pipeline is fully self-contained and pre-fitted. User inputs pass directly into the pipeline without any runtime fitting or retraining:

```text
User Input (19 Features)
       │
       ▼
┌────────────────────────────────────────────────────────┐
│  ColumnTransformer Preprocessing Pipeline              │
│  ├─ Numeric: Median Imputer + RobustScaler             │
│  ├─ Nominal: Most-Frequent Imputer + OneHotEncoder     │
│  └─ Ordinal: Most-Frequent Imputer + OrdinalEncoder    │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│  Logistic Regression Classifier (Selected Champion)    │
│  ├─ Solved: lbfgs                                      │
│  ├─ Class Weight: Balanced                             │
│  └─ Test ROC-AUC: 0.8013                               │
└────────────────────────────────────────────────────────┘
       │
       ▼
Subscription Probability & Intelligence Verdict
```

### Models Evaluated

During development, five machine learning algorithms were trained, benchmarked, cross-validated (5-fold stratified), and tuned:

| Algorithm | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **83.30%** | **0.3637** | **0.6444** | **0.4650** | **0.8013** | **Selected Champion** |
| Random Forest | 89.52% | 0.6261 | 0.3956 | 0.4848 | 0.7841 | Overfit / High Variance |
| K-Nearest Neighbors | 88.60% | 0.5622 | 0.3378 | 0.4217 | 0.7393 | Moderate Generalization |
| Support Vector Classifier | 88.36% | 0.5445 | 0.3185 | 0.4018 | 0.6846 | High Cross-Validation Variance |
| Decision Tree | 87.17% | 0.4661 | 0.3852 | 0.4218 | 0.6278 | Severe Overfitting |

*Logistic Regression was selected due to highest test ROC-AUC (0.8013), highest recall on the minority class (64.4%), stable cross-validation folds (std dev ±0.009), and fast inference latency (<5ms).*

---

## Human-Readable Feature Mapping

All features use standardized, professional terminology across the UI:

| Feature Category | Features Included |
| :--- | :--- |
| **Customer Profile** | Age, Job, Marital Status, Education, Credit Default, Housing Loan, Personal Loan |
| **Contact & Campaign** | Contact Method, Contact Month, Contact Day of Week, Campaign Contacts, Days Since Previous Contact, Previous Contacts, Previous Campaign Outcome *(Call Duration omitted to prevent data leakage)* |
| **Macroeconomic Context**| Employment Variation Rate, Consumer Price Index, Consumer Confidence Index, Euribor 3 Month Rate, Number of Employees |
| **Target Variable** | Term Deposit Subscription (`1` = Yes, `0` = No) |

---

## Project Structure

```text
Termora/
│
├── app.py                     # Main Streamlit application entrypoint
├── requirements.txt           # Pinned production dependencies
├── .gitignore                 # Git ignore rules for clean deployment
├── README.md                  # Complete documentation
│
├── model/
│   ├── bank_marketing_model.pkl   # Serialized end-to-end Pipeline artifact
│   └── model_meta.json            # Model training metadata & feature list
│
├── assets/
│   └── logo.png               # Termora brand monogram & logo
│
├── data/
│   └── bank-additional-full.csv   # Historical dataset for Campaign Analytics
│
└── termora/
    ├── __init__.py            # Package root
    ├── config.py              # Central application configuration & paths
    ├── utils/
    │   ├── __init__.py
    │   ├── styles.py          # Custom fintech CSS styling & typography
    │   ├── charts.py          # Plotly dark-navy chart factories
    │   ├── model_loader.py    # Cached pipeline loader & prediction engine
    │   └── data_loader.py     # Cached historical dataset loader
    └── pages/
        ├── __init__.py
        ├── dashboard.py       # Executive Dashboard
        ├── assessment.py      # Customer Assessment form & prediction UI
        ├── analytics.py       # Campaign Analytics charts
        ├── model_insights.py  # Model evaluation benchmark & CV stability
        ├── dataset.py         # Dataset overview & feature dictionary
        └── about.py           # Methodology & business impact
```

---

## Local Installation & Execution

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Termora.git
cd Termora
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The application will launch automatically in your default browser at `http://localhost:8501`.

---

## Streamlit Community Cloud Deployment

Deploying Termora to Streamlit Community Cloud requires no server management:

1. **Push to GitHub:**
   Ensure all changes are committed and pushed to your public or private GitHub repository:
   ```bash
   git add .
   git commit -m "feat: prepare Termora for production deployment"
   git push origin main
   ```
2. **Access Streamlit Community Cloud:**
   Log in to [share.streamlit.io](https://share.streamlit.io/) using your GitHub account.
3. **Create New App:**
   * Click **New app**.
   * Select your repository (`your-username/Termora`).
   * Set Branch to `main`.
   * Set Main file path to `app.py`.
4. **Deploy:**
   * Click **Deploy!**
   * Streamlit Community Cloud will install dependencies from `requirements.txt` and launch the app with a secure HTTPS URL.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
