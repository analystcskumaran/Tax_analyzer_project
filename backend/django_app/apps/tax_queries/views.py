from django.shortcuts import render
import requests

def tax_form(request):
    if request.method == 'POST':
        income = float(request.POST['income'])
        year = int(request.POST['year'])

        try:
            response = requests.post(
                'http://localhost:5000/predict',
                json={'income': income, 'year': year},
                timeout=5  # optional timeout in seconds
            )
            response.raise_for_status()  # raise error for non-200 status
            result = response.json()
            predicted_tax = result.get('predicted_tax', 'N/A')

            return render(request, 'result.html', {'result': predicted_tax})

        except requests.exceptions.ConnectionError:
            error_message = "The prediction service is not running. Please start the Flask backend on port 5000."
        except requests.exceptions.Timeout:
            error_message = "The request to the Flask API timed out."
        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred while contacting the Flask API: {e}"
        except Exception as e:
            error_message = f"Unexpected error: {e}"

        return render(request, 'result.html', {'error': error_message})

    return render(request, 'tax_form.html')
