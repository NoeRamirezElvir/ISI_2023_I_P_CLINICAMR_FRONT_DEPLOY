from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes


url = 'https://clinicamr.onrender.com/api/'
def listar_resultados(request):
    response = requests.get(url+'resultados/')
    if response.status_code == 200:
        data = response.json()
        resultados = data['resultados']
    else:
        resultados = []
    context = {'resultados': resultados}
    return render(request, 'Resultados/BuscarResultados.html', context)

def crear_resultados(request):
    tratamiento_list = list_tratamiento()
    if request.method == 'POST':
        idTratamiento = int(request.POST['idTratamiento'])      
        fecha = request.POST['fecha']
        observacion = request.POST['observacion']       
        registro_temp = {'idTratamiento': idTratamiento, 'fecha': fecha, 'observacion': observacion}
        response = requests.post(url+'resultados/', json={'idTratamiento': idTratamiento, 'fecha': fecha, 'observacion': observacion})
        data = response.json()      
        if response.status_code == 200:
            mensaje = data['message']
            return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp,'tratamiento_list':tratamiento_list})
            
        else:
            mensaje = data['message']
            return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'tratamiento_list':tratamiento_list})
    else:
        return render(request, 'Resultados/Resultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tratamiento_list':tratamiento_list})
    
def abrir_actualizar_resultados(request):
    tratamiento_list = list_tratamiento()
 
    if request.method == 'POST':
         print(request.POST['id_resultados'])
         resp = requests.get(url+'resultados/busqueda/id/'+str(request.POST['id_resultados']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            resultados = data['resultados']
            mensaje = data['message']
         else:
            resultados = []
         context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje,'tratamiento_list':tratamiento_list}
         mensaje = data['message']
         return render(request, 'Resultados/ActualizarResultados.html', context)
    
def actualizar_resultados(request, id):
    tratamiento_list = list_tratamiento()
    if request.method == 'POST':
        idTemporal = id
        idTratamiento = int(request.POST['idTratamiento'])
        
        fecha = request.POST['fecha']
        observacion = request.POST['observacion']
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'resultados/id/{idTemporal}', json={'idTratamiento': idTratamiento,'fecha': fecha, 'observacion':observacion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'resultados/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        resultados = data['resultados']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':resultados,'tratamiento_list':tratamiento_list})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':resultados,'tratamiento_list':tratamiento_list})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'resultados/busqueda/id/{idTemporal}')
        data = response.json()
        if response.status_code == 200:
            resultados = data['resultados']
            mensaje = data['message']
            return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados,'tratamiento_list':tratamiento_list})
        else:
            mensaje = data['message']
            return render(request, 'Resultados/ActualizarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'resultados':resultados, 'tratamiento_list':tratamiento_list})

def eliminar_resultados(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'resultados/id/{idTemporal}')
            res = response.json()
            rsp_resultados = requests.get(url + 'resultados/') 
            if rsp_resultados.status_code == 200:
                data = rsp_resultados.json()
                resultados = data['resultados']
            else:
                resultados = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje}
            return render(request, 'Resultados/BuscarResultados.html', context)     
    except:
        rsp_resultados = requests.get(url + 'resultados/') 
        if rsp_resultados.status_code == 200:
            data = rsp_resultados.json()
            resultados = data['resultados']
        else:
            resultados = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'error': mensaje}
        return render(request, 'Resultados/BuscarResultados.html', context)     
   
def buscar_resultados(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'resultados/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['resultados']:
                    data = response.json()
                    mensaje = data['message']
                    resultados = {}
                    resultados = data['resultados']
                    context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje}
                    return render(request, 'Resultados/BuscarResultados.html', context) 
                else:
                    resultados = []
                    mensaje = 'No se encontraron resultados'
                    return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})

                
            else:        
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    resultados = {}
                    resultados = data['resultados']
                    context = {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje':mensaje}
                    return render(request, 'Resultados/BuscarResultados.html', context)
                else:
                    resultados = []
                    mensaje = 'No se encontraron resultados'
                    return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})

        else:
            response = requests.get(url+'resultados/')
            if response.status_code == 200:
                data = response.json()
                resultados = data['resultados']
                mensaje = data['message']   
                return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})
            else:
                resultados = []
                mensaje = 'No se encontraron resultados'
            return render(request, 'Resultados/BuscarResultados.html', {'reportes_lista':DatosReportes.cargar_lista_resultado(),'reportes_usuarios':DatosReportes.cargar_usuario(),'resultados': resultados, 'mensaje': mensaje})

def list_tratamiento():
    rsp_tratamientos = requests.get(url+'tratamientos/')
    if rsp_tratamientos.status_code == 200:
        data = rsp_tratamientos.json()
        tratamientos_list = data['tratamientos']
        return tratamientos_list
    else:
        tratamientos_list = []
        return tratamientos_list


    
