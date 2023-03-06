from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.shortcuts import render
from passlib.context import CryptContext
import requests
from django.shortcuts import redirect


url = 'http://localhost:8080/api/'
def buscar_login(request):
    nombre = requests.POST['username']
    rsp_usuario = requests.get(url+f'usuarios/busqueda/nombre/{nombre}') 
    if rsp_usuario.status_code == 200:
        data = rsp_usuario.json()
        usuarios = data['usuariosr']
        print(usuarios)
    else:
        usuarios = []
    context = {'usuariosr': usuarios}
    return render(request, 'presentacion/usuariologin.html', context)