web: gunicorn taxanalyzer.wsgi --bind 0.0.0.0:$PORT
api: python backend/flask_api/app.py
dashboard: streamlit run frontend/streamlit_app/app.py --server.port $PORT --server.address 0.0.0.0