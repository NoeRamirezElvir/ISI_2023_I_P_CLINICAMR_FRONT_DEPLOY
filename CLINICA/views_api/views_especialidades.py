from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_especialidades(request):
    response = requests.get(url+'especialidades/')
    if response.status_code == 200:
        data = response.json()
        especialidades = data['especialidades']
        if not especialidades:
            especialidades = []
    else:
        especialidades = []
    context = {'especialidades': especialidades}
    return render(request, 'BuscarEspecialidad.html', context)