from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
def usuariologin(request):
    return render(request,'more/usuariologin.html')
def home(request):
    return render(request,'more/home.html')
def iniciomenu(request):
    return render(request,'more/iniciomenu.html')
#Usuarios
def usuario(request):
    return render(request,'more/usuario/usuario.html')
def usuarioregistro(request):
    return render(request,'more/usuario/registro.html')
def usuariolistar(request):
    return render(request,'more/usuario/listar.html')
def usuarioinicio(request):
    return render(request,'more/usuario/inicio.html')
#Empleados
