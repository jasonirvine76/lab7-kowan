import requests
import json
from django.shortcuts import render
from django.conf import settings

def calculate(request):
    result = None
    calculation_type = None

    if request.method == 'POST':
        side_length = float(request.POST.get('side_length', 0))
        calculation_type = request.POST.get('calculation_type')

        try:
            if calculation_type == 'square_area':
                faasd_url = "http://35.168.17.66:8080/function/luas-persegi"
                response = requests.post(faasd_url, json={'side': side_length})
                response_data = response.json()  
                result = response_data.get('luas_persegi')

            elif calculation_type == 'cube_surface_area':
                faasd_surface_url = "http://52.91.99.232:8080/function/cube"
                surface_response = requests.post(faasd_surface_url, json={'side': side_length})
                surface_data = surface_response.json()
                result = surface_data.get('luas_permukaan_kubus')

        except requests.exceptions.RequestException as e:
            print(f"Error calling faasd service: {e}")
            result = "Error connecting to the calculation service."

    return render(request, 'calculate.html', {'result': result, 'calculation_type': calculation_type})
