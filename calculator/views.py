# myapp/views.py

import requests
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
                # Panggil layanan untuk menghitung luas persegi
                faasd_url = settings.SQUARE_AREA_URL
                response = requests.post(faasd_url, json={'side': side_length})
                response_data = response.json()
                result = response_data.get('result')

            elif calculation_type == 'cube_volume':
                # Langkah pertama: panggil layanan untuk menghitung luas persegi
                faasd_square_url = settings.SQUARE_AREA_URL
                square_response = requests.post(faasd_square_url, json={'side': side_length})
                square_data = square_response.json()
                square_area = square_data.get('result')

                # Langkah kedua: hitung volume kubus menggunakan luas persegi
                faasd_volume_url = settings.CUBE_VOLUME_URL
                volume_response = requests.post(faasd_volume_url, json={'luas_sisi_kubus': square_area})
                volume_data = volume_response.json()
                result = volume_data.get('luas_permukaan_kubus')

        except requests.exceptions.RequestException as e:
            print(f"Error calling faasd service: {e}")
            result = "Error connecting to the calculation service."

    return render(request, 'calculate.html', {'result': result, 'calculation_type': calculation_type})
