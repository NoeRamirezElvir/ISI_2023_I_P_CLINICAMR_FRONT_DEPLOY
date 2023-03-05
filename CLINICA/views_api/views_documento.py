from django.http import HttpResponse
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/documentos/'
def listar_documentos(request):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        documentos = data['documentos']
    else:
        documentos = []
    context = {'documentos': documentos}
    return render(request, 'buscarDocumento.html', context)