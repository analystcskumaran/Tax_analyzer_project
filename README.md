# Tax Analyzer Project (Final Version)

A DevOps-enabled tax analyzer using Django, Flask, Streamlit, and ML for predictions and visualizations.

## Features
- Django: User forms for tax input.
- Flask: ML API for predictions.
- Streamlit: Multi-page dashboard with extensive visualizations.
- ML: Random Forest for tax predictions.
- DevOps: Git, pytest, GitHub Actions CI/CD, Heroku deployment.

## Setup (Local)
1. Clone repo and activate venv: `python -m venv venv && source venv/bin/activate`.
2. Install deps: `pip install -r requirements.txt`.
3. Place dataset in `data/raw/tax_data.csv`.
4. Run scripts: `python scripts/data_pipeline.py` then `python models/train_model.py`.
5. Migrate Django: `cd backend/django_app && python manage.py migrate`.
6. Run components:
   - Flask: `python backend/flask_api/app.py` (http://localhost:5000).
   - Django: `cd backend/django_app && python manage.py runserver` (http://localhost:8000).
   - Streamlit: `streamlit run frontend/streamlit_app/app.py` (http://localhost:8501).

## DevOps for 4 Developers
- Roles: Dev1 (Django), Dev2 (Flask/ML), Dev3 (Streamlit), Dev4 (DevOps).
- Workflow: Git branches, PRs, CI tests, Heroku deploy.
- Run tests: `pytest`.
- Deploy: Push to Heroku after CI.

## Team Guidelines
- Commit often, review PRs.
- Use .env for secrets.
