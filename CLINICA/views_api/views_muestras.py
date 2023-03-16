from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_muestras(request):
    response = requests.get(url+'muestras/')
    if response.status_code == 200:
        data = response.json()
        muestras= data['muestras']
    else:
        muestras = []
    context = {'muestras': muestras}
    return render(request, 'Muestras/Muestra.html', context)

