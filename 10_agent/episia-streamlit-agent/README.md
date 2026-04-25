# EpisiaAgent 🧬

> First AI epidemiologist for sub-Saharan Africa  
> **LangChain + Groq LPU + Episia validated algorithms**

---

## What is it?

EpisiaAgent is a conversational AI that answers epidemiological questions 
using validated statistical tools from the [Episia](https://github.com/Xcept-Health/episia) library.

Ask questions in **English or French**, get back validated results with clinical interpretation.

---

## Quick start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API key
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
# Get a free key at: https://console.groq.com
```

### 3. Run
```bash
streamlit run app.py --server.port 8502
```

---

## Project structure

```
episia-agent/
├── app.py                  # Streamlit UI
├── agent/
│   ├── __init__.py
│   ├── agent.py            # LangChain + Groq agent
│   ├── tools.py            # 10 episia tools
│   └── prompts.py          # EN/FR system prompts
├── requirements.txt
└── .env.example
```

---

## Available tools (10)

| Tool | Description |
|---|---|
| `tool_sample_size_risk_ratio` | Cohort study sample size (Fleiss RR) |
| `tool_sample_size_odds_ratio` | Case-control sample size (Kelsey OR) |
| `tool_sample_size_diagnostic` | Diagnostic test evaluation sample size |
| `tool_sample_size_proportion` | Single proportion survey (Cochran) |
| `tool_vaccine_efficacy` | VE = 1 − RR, 95% CI, NNV |
| `tool_diagnostic_test` | Sensitivity, specificity, LR+, LR−, PPV, NPV |
| `tool_seir_simulation` | SEIR compartmental outbreak model |
| `tool_hiv_cascade` | UNAIDS 90-90-90 cascade analysis |
| `tool_muac_analysis` | MUAC malnutrition screening analysis |
| `tool_epidemic_alert` | Epidemic threshold + Z-score alert detection |

---

## Example queries

**English:**
- `"Sample size for cohort study: baseline risk 10%, expected RR=2.5, 80% power"`
- `"Vaccine efficacy: 12 cases among 3000 vaccinated, 87 among 3000 unvaccinated"`
- `"SEIR meningitis Kaya district, population 350000, 35% vaccination coverage"`
- `"HIV cascade Burkina Faso: 110000 PLHIV, 66-79-88"`

**Français:**
- `"Taille d'échantillon cohorte : risque basal 10%, RR attendu 2.5, puissance 80%"`
- `"Efficacité vaccinale MenAfriVac : 12 cas sur 3000 vaccinés, 87 sur 3000 non vaccinés"`
- `"Cascade VIH Burkina Faso : 110000 PVVIH, 66% connaissent statut, 79% sous ARV, 88% supprimés"`

---

## Groq models

| Model | Best for |
|---|---|
| `llama-3.3-70b-versatile` | Best quality, tool use |
| `mixtral-8x7b-32768` | Multilingual, fast |
| `gemma2-9b-it` | Lightweight, quick |

Get a free API key: [console.groq.com](https://console.groq.com)

---

## Use as Python library

```python
from agent.agent import EpisiaAgent

agent = EpisiaAgent(model="llama-3.3-70b-versatile")

result = agent.run(
    "Vaccine efficacy: 12 cases among 3000 vaccinated, 87 among 3000 unvaccinated"
)
print(result["answer"])
print("Tools used:", result["tools_used"])
```

---

## License
MIT · [Xcept-Health](https://github.com/Xcept-Health)
