from django.http import HttpResponse
import json
from django.shortcuts import render
import requests

from ..views_api.datos_reporte import DatosReportes


url = 'https://clinicamr.onrender.com/api/'
def listar_cargos(request):
    response = requests.get(url+'cargos/')
    if response.status_code == 200:
        data = response.json()
        cargos = data['cargos']
    else:
        cargos = []
    context = {'cargos': cargos}
    return render(request, 'cargos/buscarCargo.html', context)

def crear_cargo(request):
    reportes_lista = DatosReportes.cargar_lista_cargos()
    reportes_usuarios = DatosReportes.cargar_usuario()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        activo = int(request.POST['payment_method'])

        registro_temp={'nombre': nombre, 'descripcion': descripcion, 'activo': activo}
        response = requests.post(url+'cargos/', json={'nombre': nombre, 'descripcion': descripcion, 'activo': activo})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'cargos/cargo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
        else:
            mensaje = data['message']
            return render(request, 'cargos/cargo.html', {'mensaje': mensaje, 'registro_temp':registro_temp,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
    else:
        return render(request, 'cargos/cargo.html',{'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
    
def abrir_actualizar_cargos(request):
    reportes_lista = DatosReportes.cargar_lista_cargos()
    reportes_usuarios = DatosReportes.cargar_usuario()
    if request.method == 'POST':
         resp = requests.get(url+'cargos/busqueda/id/'+str(request.POST['id_cargo']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            cargos = data['cargos']
            mensaje = data['message']
         else:
            cargos = []
         context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios}
         mensaje = data['message']
         return render(request, 'cargos/cargoactualizar.html', context)
    
def actualizar_cargo(request, id):
    reportes_lista = DatosReportes.cargar_lista_cargos()
    reportes_usuarios = DatosReportes.cargar_usuario()
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        activo = int(request.POST['payment_method'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'cargos/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion, 'activo': activo})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'cargos/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        cargos = data['cargos']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'cargos/cargoactualizar.html', {'mensaje': mensaje,'cargos':cargos ,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'cargos/cargoactualizar.html', {'mensaje': mensaje,'cargos':cargos,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'cargos/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            cargos = data['cargos']
            mensaje = data['message']
            return render(request, 'cargos/cargoactualizar.html', {'cargos': cargos,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
        else:
            mensaje = data['message']
            return render(request, 'cargos/cargoactualizar.html', {'mensaje': mensaje,'cargos':cargos,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})

def eliminar_cargo(request, id):
    reportes_lista = DatosReportes.cargar_lista_cargos()
    reportes_usuarios = DatosReportes.cargar_usuario()
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'cargos/id/{idTemporal}')
            res = response.json()
            rsp_cargos = requests.get(url + 'cargos/') 
            if rsp_cargos.status_code == 200:
                data = rsp_cargos.json()
                cargos = data['cargos']
            else:
                cargos = []
            mensaje = res['message']
            context = {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios}
            return render(request, 'cargos/buscarCargo.html', context)
    except:
        rsp_cargos = requests.get(url + 'cargos/') 
        if rsp_cargos.status_code == 200:
            data = rsp_cargos.json()
            cargos = data['cargos']
        else:
            cargos = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'cargos': cargos, 'error': mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios}
        return render(request, 'cargos/buscarCargo.html', context)      
    
def buscar_cargos(request):
        reportes_lista = DatosReportes.cargar_lista_cargos()
        reportes_usuarios = DatosReportes.cargar_usuario()
        valor = request.GET.get('buscador', None)
        url2 = url + 'cargos/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    cargos = {}
                    cargos = data['cargos']
                    context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios}
                    return render(request, 'cargos/buscarCargo.html', context)     
                else:
                    cargos = []
                    mensaje = 'No se encontraron cargos'
                    return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})  
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    cargos = {}
                    cargos = data['cargos']
                    context = {'cargos': cargos, 'mensaje':mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios}
                    return render(request, 'cargos/buscarCargo.html', context)
                else:
                    cargos = []
                    mensaje = 'No se encontraron cargos'
                    return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
        else:
            response = requests.get(url+'cargos/')
            if response.status_code == 200:
                data = response.json()
                cargos = data['cargos']
                mensaje = data['message']   
                return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
            else:
                cargos = []
                mensaje = 'No se encontraron cargos'
            return render(request, 'cargos/buscarCargo.html', {'cargos': cargos, 'mensaje': mensaje,'reportes_lista':reportes_lista,'reportes_usuarios':reportes_usuarios})
    