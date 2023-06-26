from datetime import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes


url = 'https://clinicamr.onrender.com/api/'
def listar_traslados(request):
    response = requests.get(url+'traslados/')
    if response.status_code == 200:
        data = response.json()
        traslados = data['traslados']
    else:
        traslados = []
    context = {'traslados': traslados}
    return render(request, 'Traslados/buscar_traslado.html', context)

def crear_traslados(request):
    autorizacion_list = list_autorizacion()
    pacientes_list = list_pacientes()
    empleado_list = list_empleado()

    if request.method == 'POST':
        idAutorizacionPaciente = int(request.POST['idAutorizacionPaciente'])
        idPaciente = int(request.POST['idPaciente'])
        idEmpleado = int(request.POST['idEmpleado'])
        nombre = request.POST['nombre']
        direccion = request.POST ['direccion']
        telefono = request.POST['telefono']
        
        registro_temp = {'idAutorizacionPaciente': idAutorizacionPaciente, 
                         'idPaciente': idPaciente, 
                         'idEmpleado': idEmpleado, 
                         'nombre':nombre, 
                         'direccion':direccion,
                         'telefono':telefono}
        response = requests.post(url+'traslados/', json={'idAutorizacionPaciente': idAutorizacionPaciente, 
                                                      'idPaciente': idPaciente, 
                                                      'idEmpleado': idEmpleado, 
                                                      'nombre':nombre, 
                                                      'direccion':direccion,
                                                      'telefono':telefono})
        data = response.json()
        if response.status_code == 200:
            mensaje = data['message']
            return render(request, 'Traslados/traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 
                                                               'registro_temp':registro_temp,
                                                               'autorizacion_list':autorizacion_list, 
                                                               'pacientes_list':pacientes_list, 
                                                               'empleado_list':empleado_list})
        else:
            mensaje = data['message']
            return render(request, 'Traslados/traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'registro_temp':registro_temp, 'autorizacion_list':autorizacion_list, 'pacientes_list':pacientes_list, 'empleado_list':empleado_list})
    else:
        return render(request, 'Traslados/traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'autorizacion_list':autorizacion_list, 
                                                          'pacientes_list':pacientes_list, 
                                                          'empleado_list':empleado_list})
    

    
def abrir_actualizar_traslados(request):
    autorizacion_list = list_autorizacion()
    pacientes_list = list_pacientes()
    empleado_list = list_empleado()
 
    if request.method == 'POST':
         
         resp = requests.get(url+'traslados/busqueda/id/'+str(request.POST['id_traslados']))
         data = resp.json()
         mensaje = data['message']
         
         if resp.status_code == 200:
            traslados = data['traslados']
            mensaje = data['message']
         else:
            traslados = []
         context = {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje':mensaje,
                                            'autorizacion_list':autorizacion_list,
                                            'pacientes_list':pacientes_list,
                                            'empleado_list':empleado_list                                          
                                            }
         mensaje = data['message']
         return render(request, 'Traslados/actualizar_traslado.html', context)
    
def actualizar_traslados(request, id):
    autorizacion_list = list_autorizacion()
    pacientes_list = list_pacientes()
    empleado_list = list_empleado()
 
    if request.method == 'POST':
        idTemporal = id
        idAutorizacionPaciente = int(request.POST['idAutorizacionPaciente'])
        idPaciente = int(request.POST['idPaciente'])
        idEmpleado = int(request.POST['idEmpleado'])
        nombre = request.POST['nombre']
        direccion = request.POST ['direccion']
        telefono = request.POST['telefono']

        response = requests.put(url+f'traslados/id/{idTemporal}', json={'idAutorizacionPaciente': idAutorizacionPaciente, 
                                                                        'idPaciente': idPaciente, 
                                                                        'idEmpleado': idEmpleado, 
                                                                        'nombre':nombre, 
                                                                        'direccion':direccion,
                                                                        'telefono':telefono})

        rsp =  response.json()
        res = requests.get(url+f'traslados/busqueda/id/{idTemporal}')
        data = res.json()
        traslados = data['traslados']
        
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Traslados/actualizar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'traslados':traslados,
                                                                                             'autorizacion_list':autorizacion_list,
                                                                                             'pacientes_list':pacientes_list,
                                                                                             'empleado_list':empleado_list                                          
                                                                                                })
        else:                                                   
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Traslados/actualizar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'traslados':traslados,
                                                                                             'autorizacion_list':autorizacion_list,
                                                                                             'pacientes_list':pacientes_list,
                                                                                             'empleado_list':empleado_list })
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'traslados/busqueda/id/{idTemporal}')
        data = response.json()
        if response.status_code == 200:
            traslados = data['traslados']
            mensaje = data['message']
            return render(request, 'Traslados/actualizar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados':traslados,
                                                                                             'autorizacion_list':autorizacion_list,
                                                                                             'pacientes_list':pacientes_list,
                                                                                             'empleado_list':empleado_list})
        else:
            mensaje = data['message']
            return render(request, 'Traslados/actualizar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'traslados':traslados,
                                                                                             'autorizacion_list':autorizacion_list,
                                                                                             'pacientes_list':pacientes_list,
                                                                                             'empleado_list':empleado_list })

def eliminar_traslados(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'traslados/id/{idTemporal}')
            res = response.json()
            rsp_traslados = requests.get(url + 'traslados/') 
            if rsp_traslados.status_code == 200:
                data = rsp_traslados.json()
                traslados = data['traslados']
            else:
                traslados = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje': mensaje}
            return render(request, 'Traslados/buscar_traslado.html', context)     
    except:
        rsp_traslados = requests.get(url + 'traslados/') 
        if rsp_traslados.status_code == 200:
            data = rsp_traslados.json()
            traslados = data['traslados']
        else:
            traslados = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'error': mensaje}
        return render(request, 'Traslados/buscar_traslado.html', context)     
     
def buscar_traslados(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'traslados/busqueda/'
        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    traslados = {}
                    traslados = data['traslados']
                    context = {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje':mensaje}
                    return render(request, 'Traslados/buscar_traslado.html', context)
                
            else:        
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    traslados = {}
                    traslados = data['traslados']
                    context = {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje':mensaje}
                    return render(request, 'Traslados/buscar_traslado.html', context)
                else:
                    traslados = []
                    mensaje = 'No se encontraron muestras'
                    return render(request, 'Traslados/buscar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje': mensaje})

        else:
            response = requests.get(url+'traslados/')
            if response.status_code == 200:
                data = response.json()
                traslados = data['traslados']
                mensaje = data['message']   
                return render(request, 'Traslados/buscar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje': mensaje})
            
            else:
                traslados = []
                mensaje = 'No se encontraron traslados'
            return render(request, 'Traslados/buscar_traslado.html', {'reportes_lista':DatosReportes.cargar_lista_traslados(),'reportes_usuarios':DatosReportes.cargar_usuario(),'traslados': traslados, 'mensaje': mensaje})


def list_autorizacion():
    rsp_autorizar = requests.get(url+'autorizar/')
    if rsp_autorizar.status_code == 200:
        data = rsp_autorizar.json()
        autorizar_list = data['autorizar']
        return autorizar_list
    else:
        autorizacion_list = []
        return autorizacion_list

def list_pacientes():
    rsp_pacientes= requests.get(url+'pacientes/')
    if rsp_pacientes.status_code == 200:
        data = rsp_pacientes.json()
        pacientes_list = data['pacientes']
        return pacientes_list
    else:
        pacientes_list = []
        return pacientes_list
    
def list_empleado():
    rsp_empleados= requests.get(url+'empleados/')
    if rsp_empleados.status_code == 200:
        data = rsp_empleados.json()
        empleados_list = data['empleados']
        return empleados_list
    else:
        empleados_list = []
        return empleados_list