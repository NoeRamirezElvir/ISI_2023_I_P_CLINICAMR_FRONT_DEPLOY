from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.shortcuts import render
from passlib.context import CryptContext
import requests
from django.shortcuts import redirect


url = 'https://clinicamr.onrender.com/api/'
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        response = requests.post(url+'login/', json={'username': username, 'password': password})
        data = response.json()
        if data['mensaje'] == 'Inicio Exitoso':
            mensaje = data['mensaje']
            return render(request, 'inicio.html', {'mensaje': mensaje})
        else:
            mensaje = data['mensaje']
            return render(request, 'presentacion/usuariologin.html', {'mensaje': mensaje})
    else:
        return render(request, 'presentacion/usuariologin.html')
    
def registrar_login(request):
    rsp_empleado = requests.get(url+'empleados/')
    if rsp_empleado.status_code == 200:
            data = rsp_empleado.json()
            empleado = data['empleados']
    else:
            response = requests.post(url+'empleados/', json={'nombre': 'administrador','apellidos': 'administrador','fechaNacimiento': '01/01/2000','idTipoDocumentos':None, 'idEspecialidadMedico':None, 'idCargoEmpleado':None, 'documento': 'N/A','telefono': 88888888,'email': 'admin.example@email.com','direccion': 'No Aplica','activo': 1 })
            rsp_empleado = requests.get(url+'empleados/')
            data = rsp_empleado.json()
            empleado = data['empleados']
    if request.method == 'POST':
        idEmpleado = int(request.POST['idEmpleadl'])
        nombreUsuario = request.POST['username']
        password = request.POST['password']
        passwordc = request.POST['passwordc']
        activo = 1
        bloqueado = 0
        if password == passwordc: 
            response = requests.post(url+'usuarios/', json={'idEmpleado':idEmpleado, 'nombreUsuario': nombreUsuario, 'password': password,'passwordc':passwordc, 'activo': activo, 'bloqueado': bloqueado})
            userdata={}
            if response.status_code == 200:
                userdata = response.json()
                mensaje = userdata['message']
                return render(request, 'presentacion/usuariosignup.html', {'mensaje': mensaje,  'empleado': empleado})
            else:
                mensaje = userdata['usuariosr']
                
                return render(request, 'presentacion/usuariosignup.html', {'mensaje': mensaje,  'empleado': empleado})
        else:
            mensaje = 'Las contraseñas no coinciden'
            return render(request, 'presentacion/usuariosignup.html', {'mensaje': mensaje,'empleado': empleado}) 
    else:
        return render(request, 'presentacion/usuariosignup.html', { 'empleado': empleado})
