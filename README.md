

<div align="center">

# The Episia Handbook

Practical tutorials, case studies, and best practices for Episia, the open-source epidemiology and biostatistics library for Python

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Episia](https://img.shields.io/badge/Episia-0.1.1-orange?style=flat-square)](https://github.com/Xcept-Health/episia)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=flat-square&logo=jupyter)](https://jupyter.org)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

Learn by doing – real epidemiological workflows with Episia

</div>

---

## Purpose

This handbook is a companion resource to the Episia library.  
It provides ready-to-run tutorials, case studies, and best practices for using Episia in real-world epidemiology and public health, with a focus on resource-limited settings, especially Africa.

Episia core library: https://github.com/Xcept-Health/episia

---

## What you will find here

- Jupyter Notebooks: step-by-step tutorials from basic biostatistics to advanced modeling  
- Real-world case studies: outbreak analysis, surveillance data, DHIS2 integration, vaccination campaigns  
- Visualization guides: creating publication-ready plots (Plotly / Matplotlib)  
- Workflow templates: reusable scripts for sample size calculation, epidemic forecasting, report generation  
- Validation examples: reproduce OpenEpi comparisons and interpret results  
- Tips and troubleshooting: common pitfalls, performance optimization, offline usage  

---

## Repository structure

```

TThe_Episia_Handbook/
├── 01_biostatistics/
│   ├── fundamentals/
│   │   ├── proportions.ipynb
│   │   ├── risk_ratio.ipynb
│   │   └── odds_ratio.ipynb
│   ├── diagnostic_tests/
│   │   ├── sensitivity_specificity.ipynb
│   │   ├── predictive_values.ipynb
│   │   └── roc_analysis.ipynb
│   └── sample_size/
│       ├── cohort_sample_size.ipynb
│       └── case_control_sample_size.ipynb
│
├── 02_epidemic_models/
│   ├── deterministic/
│   │   ├── sir_model.ipynb
│   │   ├── seir_model.ipynb
│   │   └── seird_model.ipynb
│   ├── calibration/
│   │   ├── parameter_fitting.ipynb
│   │   └── optimization_methods.ipynb
│   └── simulation/
│       ├── monte_carlo.ipynb
│       └── scenario_analysis.ipynb
│
├── 03_surveillance_data/
│   ├── dhis2/
│   │   ├── data_extraction.ipynb
│   │   └── api_integration.ipynb
│   ├── outbreak_detection/
│   │   ├── alert_thresholds.ipynb
│   │   └── endemic_channel.ipynb
│   └── time_series/
│       ├── epidemic_curves.ipynb
│       └── trend_analysis.ipynb
│
├── 04_reporting/
│   ├── automated_reports/
│   │   ├── epi_report.ipynb
│   │   └── bulletin_generation.ipynb
│   └── export_formats/
│       ├── html_export.ipynb
│       ├── pdf_export.ipynb
│       └── json_export.ipynb
│
├── 05_visualization/
│   ├── matplotlib/
│   │   ├── basic_plots.ipynb
│   │   └── publication_style.ipynb
│   ├── plotly/
│   │   ├── interactive_plots.ipynb
│   │   └── dashboards.ipynb
│   └── animations/
│       └── epidemic_animation.ipynb
│
├── 06_case_studies/
│   ├── meningitis_kaya/
│   │   ├── data.csv
│   │   └── analysis.ipynb
│   ├── hiv_burkina/
│   │   ├── cascade_analysis.ipynb
│   │   └── targets.ipynb
│   └── malaria_rdt/
│       ├── evaluation.ipynb
│       └── roc_curve.ipynb
│
├── 07_advanced/
│   ├── stochastic_models/
│   │   ├── stochastic_sir.ipynb
│   │   └── gillespie_algorithm.ipynb
│   ├── spatial_models/
│   │   ├── spatial_spread.ipynb
│   │   └── geospatial_analysis.ipynb
│   └── bayesian_methods/
│       ├── bayesian_inference.ipynb
│       └── mcmc_epidemic.ipynb
│
├── 08_machine_learning/
│   ├── sklearn/
│   │   ├── classification/
│   │   │   ├── logistic_regression.ipynb
│   │   │   ├── random_forest.ipynb
│   │   │   └── svm.ipynb
│   │   ├── regression/
│   │   │   ├── linear_regression.ipynb
│   │   │   └── ridge_lasso.ipynb
│   │   └── preprocessing/
│   │       ├── scaling.ipynb
│   │       └── feature_engineering.ipynb
│   │
│   └── workflows/
│       ├── pipeline_epidemiology.ipynb
│       └── model_evaluation.ipynb
│
├── 09_deep_learning/
│   ├── tensorflow/
│   │   ├── basics/
│   │   │   └── keras_intro.ipynb
│   │   ├── time_series/
│   │   │   └── lstm_forecasting.ipynb
│   │   └── models/
│   │       └── epidemic_prediction_tf.ipynb
│   │
│   ├── pytorch/
│   │   ├── basics/
│   │   │   └── torch_intro.ipynb
│   │   ├── time_series/
│   │   │   └── lstm_pytorch.ipynb
│   │   └── models/
│   │       └── epidemic_prediction_torch.ipynb
│   │
│   └── hybrid/
│       └── epi_ml_hybrid_models.ipynb
│
├── 10_agent/
│   └── episia_streamlit_agent/
│       ├── __init__.py
│       ├── app.py
│       ├── agent.py
│       ├── tools.py
│       ├── utils.py
│       ├── prompts.py
│       ├── requirements.txt
│       ├── .env.example
│       └── README.md
│
├── scripts/
│   ├── quick_report.py
│   └── fetch_dhis2_example.py
│
├── data/
│   └── meningitis_sample.csv
│
├── images/
├── CONTRIBUTING.md
├── LICENSE
└── README.md

````

---

## Quick start

### Install Episia

```bash
pip install episia
````

Optional:

```bash
pip install episia[full]
```

### Clone this handbook

```bash
git clone https://github.com/Xcept-Health/The_Episia_Handbook.git
cd The_Episia_Handbook
```

### Launch Jupyter

```bash
jupyter notebook
```

You can also use VS Code or any preferred environment.

---

## Example tutorial – Risk ratio

Open:

```
01_biostatistics/risk_ratio_tutorial.ipynb
```

Example:

```python
from episia import epi

rr = epi.risk_ratio(a=40, b=10, c=20, d=30)
print(rr)
```

Expected output:

```
Risk Ratio: 2.667 (1.514-4.696)
```

Each notebook explains the epidemiological concept, shows the Episia code, and interprets the results.

---

## Featured case studies

* Meningitis outbreak, Kaya district
  SEIR modeling, alert detection, report generation

* HIV 90-90-90 cascade, Burkina Faso
  Cascade analysis and target setting

* Malaria RDT evaluation
  Sensitivity, specificity, ROC curves

Each case study includes:

* Epidemiological context
* Anonymised data
* Full analysis with Episia
* Interpretation for public health action

---

## How to contribute

1. Fork the repository
2. Create a branch:

```bash
git checkout -b feature/new-tutorial
```

3. Add your notebook in the appropriate folder
4. Follow the notebook style guide in CONTRIBUTING.md
5. Submit a Pull Request

Ensure your notebook runs without errors and includes clear explanations.

---

## License

This handbook is provided under the MIT License, same as Episia.
You are free to use, modify, and share the content with proper attribution.

---

## Acknowledgements

* The Episia team for building the library
* OpenEpi for validation reference
* Public health professionals contributing to testing and improvement

---

## Contact and discussion

Episia discussions:
[https://github.com/Xcept-Health/episia/discussions](https://github.com/Xcept-Health/episia/discussions)

Handbook suggestions:
Open an issue in this repository

---

<div align="center">

Xcept-Health – Ouagadougou, Burkina Faso

</div>
