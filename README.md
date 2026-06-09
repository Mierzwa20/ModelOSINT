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
- **Weight (W)**: Multiplier (1 to 4) used to determine the value of data to an attacker.

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

### Classic setup - usage without database

1. Change into the `app` directory: `cd app`
2. Ensure Python is installed on your system: `python3 --version` or `python --version`
3. Create a Python virtual environment: `python3 -m venv .venv`
4. Activate Python virtual environment: `source .venv/bin/activate`
5. Install Flask: `pip install -r requirements.txt`
6. Set environmental variables: `export FLASK_SECRET_KEY=Tw0j_b4rdz0_t4jny_i_dlu9i_klucz_s3syjny_123!@#`
7. Run the application: `python app.py`
8. Open your browser and navigate to `http://127.0.0.1:5555/`

### Docker - full setup with database

1. Ensure Docker is installed on your system: `docker --version`
2. Make sure your current working directory is the root of this repository
3. Set environmental variables in `.env` file:

```bash
POSTGRES_USER=testUser
POSTGRES_PASSWORD=testPasswd
FLASK_SECRET_KEY=Tw0j_b4rdz0_t4jny_i_dlu9i_klucz_s3syjny_123!@#
SURVEY_APP_PASSWORD=ToHasloJestTylkoDlaUsera!
```

4. Run the application: `docker compose up`
5. Open your browser and navigate to `http://127.0.0.1:5555/`

### Getting Results

1. `docker compose exec db-app psql -U {env_user} -d db-app`
2. `{env_passwd}`
3. Average score by education profile

```SQL
SELECT
    s.education_profile AS education_profile,
    ua.category AS category,
    ROUND(AVG(ua.points_earned), 2) AS average_risk_points,
    COUNT(DISTINCT s.id) AS submission_count
FROM user_answers ua
JOIN submissions s ON ua.submission_id = s.id
GROUP BY s.education_profile, ua.category
ORDER BY s.education_profile, average_risk_points DESC;
```

4. Average score by age group

```SQL
SELECT
    age_group AS age_group,
    ROUND(AVG(total_score), 2) AS average_total_score,
    COUNT(*) AS sample_count
FROM submissions
GROUP BY age_group
ORDER BY average_total_score DESC;
```

## CI/CD Pipeline Trigger

In this project, CI/CD is implemented using **GitHub Actions**. The pipeline is triggered by creating a new tag for release, following the naming convention `v*`.

**Create new releases ONLY when code is fully tested!**
