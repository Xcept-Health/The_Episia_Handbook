

<div align="center">

# The Episia Handbook

Practical tutorials, case studies, and best practices for Episia – the open-source epidemiology and biostatistics library for Python

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

The_Episia_Handbook/
├── 01_biostatistics/
│   ├── risk_ratio_tutorial.ipynb
│   ├── diagnostic_test_evaluation.ipynb
│   └── sample_size_calculations.ipynb
│
├── 02_epidemic_models/
│   ├── seir_burkina_faso.ipynb
│   ├── model_calibration_fitting.ipynb
│   └── monte_carlo_sensitivity.ipynb
│
├── 03_surveillance_data/
│   ├── meningitis_alert_system.ipynb
│   ├── working_with_dhis2.ipynb
│   └── epidemic_curves_and_trends.ipynb
│
├── 04_reporting/
│   └── automated_bulletins.ipynb
│
├── 05_visualization/
│   └── plotly_matplotlib_guide.ipynb
│
├── 06_case_studies/
│   ├── meningitis_outbreak_kaya/
│   ├── hiv_cascade_burkina/
│   └── malaria_rdt_evaluation/
│
├── 07_advanced/
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
