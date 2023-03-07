from django.http import HttpResponse
import json
from django.shortcuts import render
import requests



def presentacion(request):
    return render(request,'presentacion/presentacion.html')
def usuariologin(request):
    return render(request,'presentacion/usuariologin.html')

def usuariosignup(request):##############
    return render(request,'presentacion/usuariosignup.html')
def abrir_actualizar_cargos(request):#
    return render(request,'cargoactualizar.html')
def actualizar_cargo(request,id):#
    return render(request,'cargoactualizar.html')
def buscar_cargos(request):#
    return render(request,'buscarCargo.html')
#
def abrir_actualizar_documentos(request):#
    return render(request,'documentoactualizar.html')
def actualizar_documento(request,id):#
    return render(request,'documentoactualizar.html')
def buscar_documentos(request):#
    return render(request,'buscarDocumento.html')
def crear_documento(request):#
    return render(request,'documento.html')



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
