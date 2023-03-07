from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
def listar_empleados(request):
    response = requests.get(url+'empleados/')
    if response.status_code == 200:
        data = response.json()
        empleados = data['empleados']
    else:
        empleados = []
    context = {'empleados': empleados}
    return render(request, 'empleado/buscarEmpleado.html', context)