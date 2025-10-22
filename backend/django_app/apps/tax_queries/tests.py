from django.test import TestCase
from unittest.mock import patch

class TaxQueryTest(TestCase):
    def test_form_render(self):
        """
        Test that the tax form page renders successfully.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Income")
        self.assertContains(response, "Year")

    @patch('apps.tax_queries.views.requests.post')
    def test_post_tax_form(self, mock_post):
        """
        Test submitting the tax form.
        The Flask API call is mocked to avoid external dependency.
        """
        # Mock the Flask API response
        mock_post.return_value.json.return_value = {'predicted_tax': 1234}

        response = self.client.post('/', {'income': 50000, 'year': 2025})
        self.assertEqual(response.status_code, 200)
        # Verify that the predicted tax appears in the rendered result
        self.assertContains(response, "1234")
