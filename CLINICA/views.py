from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
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
def registro(request):
    return render(request,'usuario/registro.html')
def listar(request):
    return render(request,'usuario/listar.html')
def inicio(request):
    return render(request,'usuario/inicio.html',{})
def empleado(request):
    return render(request,'empleado/empleado.html')
def cargo(request):
    return render(request,'cargo.html')
def especialidad(request):
    return render(request,'especialidad.html')
def documento(request):
    return render(request,'documento.html')
def buscarEmpleado(request):
    return render(request,'empleado/buscarEmpleado.html')
def buscarCargo(request):
    return render(request,'buscarCargo.html')
def buscarDocumento(request):
    return render(request,'buscarDocumento.html')
def BuscarEspecialidad(request):
    return render(request,'BuscarEspecialidad.html')



#Empleados
