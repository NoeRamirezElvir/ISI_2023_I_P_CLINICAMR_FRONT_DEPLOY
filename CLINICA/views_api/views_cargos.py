from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/cargos/'
def listar_cargos(request):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cargos = data['cargos']
    else:
        cargos = []
    context = {'cargos': cargos}
    return render(request, 'buscarCargo.html', context)

def crear_cargo(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        activo = int(request.POST['payment_method'])
        response = requests.post(url, json={'nombre': nombre, 'descripcion': descripcion, 'activo': activo})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'cargo.html', {'mensaje': mensaje})
        else:
            mensaje = data['message']
            return render(request, 'cargo.html', {'mensaje': mensaje})
    else:
        return render(request, 'cargo.html')
    
