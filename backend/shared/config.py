import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///tax.db')
MODEL_PATH = os.getenv('MODEL_PATH', '../../models/model.pkl')
DATA_PATH = os.getenv('DATA_PATH', '../../data/processed/cleaned_tax_data.pkl')