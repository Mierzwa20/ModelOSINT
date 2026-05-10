# OSINT Risk Assessment Model

A Python Flask web application designed as an auditing tool to calculate an individual's vulnerability to OSINT (Open-Source Intelligence) tracking and profiling.

## Logic and Methodology

The app uses a 20-factor proprietary model divided into 5 attack vector categories:

1. Social Media
2. Digital Footprint
3. Personally Identifiable Information (PII)
4. Cyber Hygiene
5. Advanced Footprints

### Scoring System

- **Value (P)**: Each answer maps to a risk scale from `0` (Safe) to `10` (Vulnerable).
- **Weight (W)**: Multiplier (1 to 4) determining the value of data to an attacker.

### Formula

The final score is calculated using the following mathematical model:

<p align="center"><img src="https://marmag0.github.io/endpoints/random/piodo-formula.png" alt="Risk Formula"></p>

```
Risk(\%) = \left( \frac{\sum_{i=1}^{20} (P_i \cdot W_i)}{\sum_{i=1}^{20} (10 \cdot W_i)} \right) \cdot 100
```

### Interpretation

- **`0% - 25%` (Minimal):** Perfect digital hygiene.
- **`26% - 50%` (Moderate):** Average user, basic profiling possible.
- **`51% - 75%` (High):** Serious privacy threat.
- **`76% - 100%` (Critical):** Completely transparent digital life.

## Setup Instructions

1. Ensure Python is installed on your system: `python3 --version` or `python --version`
2. Create Python virtual environment: `python3 -m venv .venv`
3. Activate Python virtual environment: `source .venv/bin/activate`
4. Install Flask: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open your browser and navigate to `http://127.0.0.1:5000/`
