"""ISI_ClINICA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from CLINICA.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', presentacion),
    path('CLINICA/templates/presentacion/usuariologin.html',usuariologin),
    path('CLINICA/templates/home.html',home),
    path('CLINICA/templates/presentacion/iniciomenu.html',iniciomenu),
    path('CLINICA/templates/usuario/usuario.html',usuario),
    path('CLINICA/templates/usuario/inicio.html',inicio),
    path('CLINICA/templates/usuario/listar.html',listar),
    path('CLINICA/templates/usuario/registro.html',registro),
    path('CLINICA/templates/empleado/empleado.html',empleado),
    path('CLINICA/templates/cargo.html',cargo),
    path('CLINICA/templates/especialidad.html',especialidad),
    path('CLINICA/templates/documento.html',documento),
    path('CLINICA/templates/empleado/buscarEmpleado.html',buscarEmpleado),
    path('CLINICA/templates/buscarCargo.html',buscarCargo),
    path('CLINICA/templates/buscarDocumento.html',buscarDocumento),
    path('CLINICA/templates/BuscarEspecialidad.html',BuscarEspecialidad),
]
