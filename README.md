# Twin-Severe-Outcome

**Early Postnatal Risk Stratification for Severe Adverse Outcomes in Twin Neonates Using Interpretable Machine Learning**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/)
[![SHAP](https://img.shields.io/badge/SHAP-0.42.1-red.svg)](https://github.com/slundberg/shap)

---

## Overview

This repository contains the source code and analysis pipeline for developing and temporally validating an interpretable machine-learning model to predict severe composite adverse outcomes in twin neonates admitted to the NICU.

The final Gradient Boosting model uses **10 routinely available clinical predictors** obtainable within 24 hours of admission and achieves an AUC of **0.844 (95% CI: 0.812–0.875)** in temporal validation.

> **Manuscript:** *Early postnatal risk stratification for severe adverse outcomes in twin neonates admitted to the NICU: development and temporal validation of an interpretable machine-learning model*
>
> **Journal:** Translational Pediatrics (Manuscript ID: TP-2026-1-0007-CL)

---

## Study Design

```
Twin neonates admitted to NICU (Shanxi Children's Hospital)
│
├── Derivation Cohort (n=912, July 2022 – June 2023)
│   ├── Training Set (70%, n=638)
│   └── Testing Set  (30%, n=274)
│
└── Temporal Validation Cohort (n=592, July – December 2023)
```

**Composite Outcome:** Transfusion-requiring anemia, RDS, EOS, IVH grade III/IV, BPD, hsPDA, NEC ≥ stage IIA, PVL, and pulmonary hypertension.

**10 LASSO-Selected Predictors:**

| Neonatal Factors | Maternal–Perinatal Factors |
|:---|:---|
| Gestational age | Chorionicity |
| Birth weight | Gestational hypertension |
| Neonatal hypoglycemia | Gestational hypothyroidism |
| Congenital malformation | Intrahepatic cholestasis |
| | Gestational anemia |
| | Grade III meconium staining |

---

## Modeling Pipeline

The analysis pipeline includes:

1. **Data preprocessing** — Missing data imputation (MICE), multicollinearity check (VIF), twin-pair–aware data splitting
2. **Feature selection** — Four strategies compared: LASSO, LightGBM, K-Best (ANOVA F-value), and intersection approach
3. **Model training** — 10 ML algorithms × 4 feature sets = 40 candidate models, with SMOTE and grid-search hyperparameter tuning via 5-fold cross-validation
4. **Model evaluation** — AUC, Brier score, calibration plots, precision–recall curves, decision curve analysis (DCA), composite performance score
5. **Temporal validation** — Frozen model applied to an independent temporal cohort
6. **Interpretability** — SHAP summary plots and individual waterfall plots
7. **Sensitivity analysis** — Within-pair concordance and cluster-robust bootstrap
8. **Clinical translation** — Web-based risk calculator (Streamlit)

### Algorithms Evaluated

| Algorithm | Abbreviation |
|:---|:---|
| Logistic Regression | LR |
| Artificial Neural Network | ANN |
| Decision Tree | DT |
| Extremely Randomized Trees | ET |
| **Gradient Boosting** | **GB (final model)** |
| K-Nearest Neighbors | KNN |
| LightGBM | LGBM |
| Random Forest | RF |
| Support Vector Machine | SVM |
| XGBoost | XGB |

---

## Repository Structure

```
Twin-Severe-Outcome/
├── README.md
├── requirements.txt
├── notebooks/
│   └── Lasso_feature_selection_and_modeling.ipynb   # Full analysis pipeline
├── app/
│   └── streamlit_app.py                             # Web-based risk calculator
├── figures/
│   ├── Figure1_study_flow.pdf
│   ├── Figure2_LASSO_coefficients_correlation.png
│   ├── Figure3_internal_testing_performance.png
│   ├── Figure4_temporal_validation_performance.png
│   └── Figure5_SHAP_and_calculator.png
└── supplementary/
    ├── Supplementary_Table_S1.xlsx    # All 40 model configurations
    ├── Supplementary_Table_S2.xlsx    # Derivation vs temporal cohort comparison
    ├── Supplementary_Table_S3.xlsx    # Hyperparameter search spaces
    ├── Supplementary_Table_S4.xlsx    # Within-pair concordance & bootstrap
    ├── Supplementary_Table_S5.xlsx    # Outcome operational definitions
    ├── Supplementary_Methods.docx     # Composite score calculation
    ├── FigureS1.png                   # Alternative feature importance
    ├── FigureS2.png                   # ROC curves (all 10 algorithms)
    ├── FigureS3.jpg                   # Radar plot (RF vs GB)
    └── FigureS4.png                   # Cluster bootstrap analysis
```

---

## Installation

```bash
git clone https://github.com/MdXuDeKai/Twin-Severe-Outcome.git
cd Twin-Severe-Outcome
pip install -r requirements.txt
```

### Requirements

```
streamlit>=1.28.0
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
shap==0.42.1
imbalanced-learn==0.11.0
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.15.0
lightgbm
xgboost
```

Python ≥ 3.12 is recommended.

---

## Usage

### Run the Analysis Notebook

```bash
jupyter notebook notebooks/Lasso_feature_selection_and_modeling.ipynb
```

The notebook covers the full pipeline from data loading through SHAP interpretation. Note that the raw clinical data are not included in this repository due to patient privacy regulations; the notebook is provided for methodological transparency.

### Launch the Web-Based Risk Calculator

```bash
streamlit run app/streamlit_app.py
```

The calculator accepts 10 clinical inputs and returns a predicted probability of severe adverse outcomes with a risk category and SHAP-based explanation.

---

## Key Results

| Metric | Internal Testing | Temporal Validation |
|:---|:---:|:---:|
| **AUC** | 0.848 | 0.844 (95% CI: 0.812–0.875) |
| **Brier Score** | 0.158 | 0.162 |
| **Accuracy** | — | 0.771 |
| **Sensitivity** | — | 0.659 |
| **Specificity** | — | 0.853 |
| **F1 Score** | — | 0.647 |

Cluster-robust bootstrap (accounting for within-pair twin correlation) yielded a similar AUC of 0.846 (95% CI: 0.806–0.884) with a CI width ratio of 1.25, confirming model robustness.

---

## Data Availability

The clinical datasets are not publicly available due to patient privacy and institutional regulations. Requests for data access should be directed to the corresponding author. The trained model is made available through the web-based risk calculator for research purposes.

---

## Citation

If you use this code or find this work helpful, please cite:

```bibtex
@article{xu2026twin,
  title   = {Early postnatal risk stratification for severe adverse outcomes 
             in twin neonates admitted to the {NICU}: development and temporal 
             validation of an interpretable machine-learning model},
  author  = {Xu, DeKai and others},
  journal = {Translational Pediatrics},
  year    = {2026},
  note    = {Manuscript ID: TP-2026-1-0007-CL}
}
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

This work was supported by the National Clinical Key Specialty Neonatal Construction Funding.
