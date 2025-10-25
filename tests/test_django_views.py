import os
import django
from django.test import TestCase, Client

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.django_app.taxanalyzer.settings')
django.setup()

def test_tax_form():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200