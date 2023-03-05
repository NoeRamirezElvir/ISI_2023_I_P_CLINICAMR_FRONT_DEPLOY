from django.http import HttpResponse
import json
from django.shortcuts import render
import requests



def presentacion(request):
    return render(request,'presentacion/presentacion.html')
def usuariologin(request):
    return render(request,'presentacion/usuariologin.html')
def home(request):
    return render(request,'base_principal.html')
def iniciomenu(request):
    return render(request,'presentacion/iniciomenu.html')
#Usuarios
def usuario(request):
    return render(request,'usuario/usuario.html')

def crear_usuario(request):#
    return render(request,'usuario/registro.html')
def abrir_actualizar_usuario(request):#
    return render(request,'usuario/actualizar.html')
def actualizar_usuario(request,id):#
    return render(request,'usuario/actualizar.html')
def eliminar_usuario(request,id):#
    return render(request,'usuario/listar.html')
def buscar_usuarios(request):#
    return render(request,'usuario/listar.html')

def inicio(request):
    return render(request,'usuario/inicio.html',)
def empleado(request):
    return render(request,'empleado/empleado.html')

def crear_cargo(request):#
    return render(request,'cargo.html')

def especialidad(request):
    return render(request,'especialidad.html')
def documento(request):
    return render(request,'documento.html')
def buscarEmpleado(request):
    return render(request,'empleado/buscarEmpleado.html')



#Empleados
