from django.test import TestCase

class TaxQueryTest(TestCase):
    def test_form_render(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)