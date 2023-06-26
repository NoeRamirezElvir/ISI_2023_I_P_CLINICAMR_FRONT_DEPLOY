from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes


url = 'https://clinicamr.onrender.com/api/'
def listar_TipoMuestra(request):
    response = requests.get(url+'tmuestra/')
    if response.status_code == 200:
        data = response.json()
        tmuestra = data['tmuestra']
        if not tmuestra:
            tmuestra = []
    else:
        tmuestra = []
    context = {'tmuestra': tmuestra}
    return render(request, 'TipoMuestra/TMuestra.html ', context)


def crear_TipoMuestra(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        metodoConservacion = request.POST['metodoConservacion']
        
        registro_temp={'nombre': nombre, 'metodoConservacion': metodoConservacion}
        response = requests.post(url+'tmuestra/', json={'nombre': nombre, 'metodoConservacion': metodoConservacion})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'TipoMuestra/TMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'registro_temp':registro_temp})
        else:
            mensaje = data['message']
            return render(request, 'TipoMuestra/TMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,  'registro_temp':registro_temp})
    else:
        return render(request, 'TipoMuestra/TMuestra.html',{'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
def abrir_actualizar_TipoMuestra(request):
    if request.method == 'POST':
         resp = requests.get(url+'tmuestra/busqueda/id/'+str(request.POST['id_tmuestra']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            tmuestra = data['tmuestra']
            mensaje = data['message']
         else:
            tmuestra = []
         context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'TipoMuestra/TMuestraActualizar.html', context)
    
def actualizar_TipoMuestra(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        metodoConservacion = request.POST['metodoConservacion']
        
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'tmuestra/id/{idTemporal}', json={'nombre': nombre, 'metodoConservacion': metodoConservacion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'tmuestra/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        tmuestra = data['tmuestra']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':tmuestra })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':tmuestra})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'tmuestra/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            tmuestra = data['tmuestra']
            mensaje = data['message']
            return render(request, 'TipoMuestra/TMuestraActualizar.html ', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra})
        else:
            mensaje = data['message']
            return render(request, 'TipoMuestra/TMuestraActualizar.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'tmuestra':tmuestra})

def eliminar_TipoMuestra(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'tmuestra/id/{idTemporal}')
            res = response.json()
            rsp_tmuestra = requests.get(url + 'tmuestra/') 
            if rsp_tmuestra.status_code == 200:
                data = rsp_tmuestra.json()
                tmuestra = data['tmuestra']
            else:
                tmuestra = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje}
            return render(request, 'TipoMuestra/BuscarTMuestra.html', context)     
    except:
        rsp_tmuestra = requests.get(url + 'tmuestra/') 
        if rsp_tmuestra.status_code == 200:
            data = rsp_tmuestra.json()
            tmuestra = data['tmuestra']
        else:
            tmuestra = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'error': mensaje}
        return render(request, 'TipoMuestra/BuscarTMuestra.html', context)     
    
def buscar_TipoMuestra(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'tmuestra/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tmuestra = {}
                    tmuestra = data['tmuestra']
                    context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', context) 
    
                else:
                    tmuestra = []
                    mensaje = 'No se encontraron Tipos de Muestra'
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
    
                      
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    tmuestra = {}
                    tmuestra = data['tmuestra']
                    context = {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje':mensaje}
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', context)
                else:
                    tmuestra = []
                    mensaje = 'No se encontraron Tipos de Muestra'
                    return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
    
        else:
            response = requests.get(url+'tmuestra/')
            if response.status_code == 200:
                data = response.json()
                tmuestra = data['tmuestra']
                mensaje = data['message']   
                return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
            else:
                tmuestra = []
                mensaje = 'No se encontraron Tipos de Muestra'
            return render(request, 'TipoMuestra/BuscarTMuestra.html', {'reportes_lista':DatosReportes.cargar_lista_tipo_muestra(),'reportes_usuarios':DatosReportes.cargar_usuario(),'tmuestra': tmuestra, 'mensaje': mensaje})
    