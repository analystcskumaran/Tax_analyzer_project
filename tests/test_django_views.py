from django.test import Client

def test_tax_form():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200