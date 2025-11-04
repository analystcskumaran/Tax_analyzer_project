# Tax Analyzer Project (Final Version)

A DevOps-enabled tax analyzer using Django, Flask, Streamlit, and ML for predictions and visualizations.

## Features
- Django: User forms for tax input.
- Flask: ML API for predictions.
- Streamlit: Multi-page dashboard with extensive visualizations.
- ML: Random Forest for tax predictions.
- DevOps: Git, pytest, GitHub Actions CI/CD, Heroku deployment.

## Setup (Local)
# 1. Clone repo
git clone https://github.com/analystcskumaran/Tax_analyzer_project.git
cd Tax_analyzer_project

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\Activate  # (PowerShell on Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Flask backend
cd backend
python flask_api.py

# 5. Open new terminal → run Streamlit frontend
cd ../frontend/streamlit_app
venv\Scripts\Activate
streamlit run app.py

## DevOps for 4 Developers
- Roles: Dev1 (Django), Dev2 (Flask/ML), Dev3 (Streamlit), Dev4 (DevOps).
- Workflow: Git branches, PRs, CI tests, Heroku deploy.
- Run tests: `pytest`.
- Deploy: Push to Heroku after CI.

## Team Guidelines
- Commit often, review PRs.
- Use .env for secrets.
