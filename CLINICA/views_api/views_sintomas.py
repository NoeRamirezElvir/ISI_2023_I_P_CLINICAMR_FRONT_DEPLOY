from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes


url = 'https://clinicamr.onrender.com/api/'
def listar_sintomas(request):
    response = requests.get(url+'sintomas/')
    if response.status_code == 200:
        data = response.json()
        sintomas = data['sintomas']
    else:
        sintomas = []
    context = {'sintomas': sintomas}
    return render(request, 'sintomas/buscar_sintomas.html', context)

def crear_sintomas(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        registro_temp={'nombre': nombre, 'descripcion': descripcion}
        response = requests.post(url+'sintomas/', json={'nombre': nombre, 'descripcion': descripcion})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'sintomas/sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'sintomas/sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp})
    else:
        return render(request, 'sintomas/sintomas.html',{'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
def abrir_actualizar_sintomas(request):
    if request.method == 'POST':
         resp = requests.get(url+'sintomas/busqueda/id/'+str(request.POST['id_sintoma']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            sintomas = data['sintomas']
            mensaje = data['message']
         else:
            sintomas = []
         context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'sintomas/actualizar_sintomas.html', context)
    
def actualizar_sintomas(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']

        response = requests.put(url+f'sintomas/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
        rsp =  response.json()

        res = requests.get(url+f'sintomas/busqueda/id/{idTemporal}')
        data = res.json()
        sintomas = data['sintomas']
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':sintomas })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':sintomas})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'sintomas/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            sintomas = data['sintomas']
            mensaje = data['message']
            return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas})
        else:
            mensaje = data['message']
            return render(request, 'sintomas/actualizar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'sintomas':sintomas})

def eliminar_sintomas(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'sintomas/id/{idTemporal}')
            res = response.json()
            rsp_cargos = requests.get(url + 'sintomas/') 
            if rsp_cargos.status_code == 200:
                data = rsp_cargos.json()
                sintomas = data['sintomas']
            else:
                sintomas = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje}
            return render(request, 'sintomas/buscar_sintomas.html', context)     
    except:
        rsp_cargos = requests.get(url + 'sintomas/') 
        if rsp_cargos.status_code == 200:
            data = rsp_cargos.json()
            sintomas = data['sintomas']
        else:
            sintomas = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'error': mensaje}
        return render(request, 'sintomas/buscar_sintomas.html', context)     
        
def buscar_sintomas(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'sintomas/busqueda/'
        if valor is not None and (len(valor)>0):           
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    sintomas = {}
                    sintomas = data['sintomas']
                    context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
                    return render(request, 'sintomas/buscar_sintomas.html', context)
                else:
                    sintomas = []
                    mensaje = 'No se encontraron sintomas'
                    return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
           
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    sintomas = {}
                    sintomas = data['sintomas']
                    context = {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje':mensaje}
                    return render(request, 'sintomas/buscar_sintomas.html', context)
                else:
                    sintomas = []
                    mensaje = 'No se encontraron sintomas'
                    return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
           
        else:
            response = requests.get(url+'sintomas/')
            if response.status_code == 200:
                data = response.json()
                sintomas = data['sintomas']
                mensaje = data['message']   
                return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
            else:
                sintomas = []
                mensaje = 'No se encontraron sintomas'
            return render(request, 'sintomas/buscar_sintomas.html', {'reportes_lista':DatosReportes.cargar_lista_sintoma(),'reportes_usuarios':DatosReportes.cargar_usuario(),'sintomas': sintomas, 'mensaje': mensaje})
    