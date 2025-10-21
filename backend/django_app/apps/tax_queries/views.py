from django.shortcuts import render
import requests

def tax_form(request):
    if request.method == 'POST':
        income = float(request.POST['income'])
        year = int(request.POST['year'])
        response = requests.post('http://localhost:5000/predict', json={'income': income, 'year': year})
        result = response.json()
        return render(request, 'result.html', {'result': result['predicted_tax']})
    return render(request, 'tax_form.html')