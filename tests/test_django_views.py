import os
import django
from django.test import Client

# ✅ Correct Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxanalyzer.settings')
django.setup()

def test_tax_form():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200
