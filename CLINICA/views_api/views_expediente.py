from django.http import HttpResponse
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes



url = 'https://clinicamr.onrender.com/api/'
def listar_expediente(request):
    response = requests.get(url+'expediente/')
    if response.status_code == 200:
        data = response.json()
        expediente = data['expedientes']
    else:
        expediente = []
    context = {'expediente': expediente}
    return render(request, 'expediente/buscar_expediente.html', context)

def crear_expediente(request):
    paciente_list = list_pacientes()
    if request.method == 'POST':
        idPaciente = int(request.POST['idPaciente'])
        observacion = (request.POST['observacion'])
        activo = int(request.POST['activo'])

        registro_temp={'idPaciente': idPaciente, 'observacion': observacion, 'activo': activo}
        response = requests.post(url+'expediente/', json={'idPaciente': idPaciente, 'observacion': observacion, 'activo': activo})
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'expediente/expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp, 'paciente_list':paciente_list})
        else:
            mensaje = data['message']
            return render(request, 'expediente/expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje, 'registro_temp':registro_temp, 'paciente_list':paciente_list})
    else:
        return render(request, 'expediente/expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'paciente_list':paciente_list})
    
def abrir_actualizar_expediente(request):
    paciente_list = list_pacientes()
    if request.method == 'POST':
         resp = requests.get(url+'expediente/busqueda/id/'+str(request.POST['id_expediente']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            expediente = data['expedientes']
            mensaje = data['message']
         else:
            expediente = []
         context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje':mensaje,'paciente_list':paciente_list}
         mensaje = data['message']
         return render(request, 'expediente/actualizar_expediente.html', context)

def abrir_detalle_expediente(request):
    if request.method == 'POST':
         resp = requests.get(url+'expediente/busqueda/id/'+str(request.POST['id_expediente']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            expediente = data['expedientes']
            mensaje = data['message']
         else:
            expediente = []
         context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'expediente/ver_detalle_expediente.html', context)
    
def actualizar_expediente(request, id):
    paciente_list = list_pacientes()
    if request.method == 'POST':
        idTemporal = id
        idPaciente = int(request.POST['idPaciente'])
        observacion = (request.POST['observacion'])
        activo = int(request.POST['activo'])
        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'expediente/id/{idTemporal}', json={'idPaciente': idPaciente, 'observacion': observacion, 'activo': activo})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'expediente/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        expediente = data['expedientes']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'expediente/actualizar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'expediente':expediente, 'paciente_list':paciente_list })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'expediente/actualizar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'expediente':expediente, 'paciente_list':paciente_list})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'expediente/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            expediente = data['expedientes']
            mensaje = data['message']
            return render(request, 'expediente/actualizar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'paciente_list':paciente_list})
        else:
            mensaje = data['message']
            return render(request, 'expediente/actualizar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'mensaje': mensaje,'expediente':expediente, 'paciente_list':paciente_list})

def eliminar_expediente(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'expediente/id/{idTemporal}')
            res = response.json()
            rsp_expediente = requests.get(url + 'expediente/') 
            if rsp_expediente.status_code == 200:
                data = rsp_expediente.json()
                expediente = data['expedientes']
            else:
                expediente = []
            mensaje = res['message']
            context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje': mensaje}
            return render(request, 'expediente/buscar_expediente.html', context)     
    except:
        rsp_expediente = requests.get(url + 'expediente/') 
        if rsp_expediente.status_code == 200:
            data = rsp_expediente.json()
            expediente = data['expedientes']
        else:
            expediente = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'error': mensaje}
        return render(request, 'expediente/buscar_expediente.html', context)     
 
def buscar_expediente(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'expediente/busqueda/'

        if valor is not None and (len(valor)>0):
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['expedientes']:
                    data = response.json()
                    mensaje = data['message']
                    expediente = {}
                    expediente = data['expedientes']
                    context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje':mensaje}
                    return render(request, 'expediente/buscar_expediente.html', context)
                else:
                    response = requests.get(url2+'documento/'+valor)
                    if response.status_code == 200:
                        data = response.json()
                        mensaje = data['message']
                        expediente = {}
                        expediente = data['expedientes']
                        context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje':mensaje}
                        return render(request, 'expediente/buscar_expediente.html', context)
                    else:
                        expediente = []
                        mensaje = 'No se encontraron documentos'
                        return render(request, 'expediente/buscar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje': mensaje})
            else:
                response = requests.get(url2+'documento/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    expediente = {}
                    expediente = data['expedientes']
                    context = {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje':mensaje}
                    return render(request, 'expediente/buscar_expediente.html', context)
                else:
                    expediente = []
                    mensaje = 'No se encontraron documentos'
                    return render(request, 'expediente/buscar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje': mensaje})
        else:
            response = requests.get(url+'expediente/')
            if response.status_code == 200:
                data = response.json()
                expediente = data['expedientes']
                mensaje = data['message']   
                return render(request, 'expediente/buscar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje': mensaje})
            else:
                expediente = []
                mensaje = 'No se encontraron documentos'
            return render(request, 'expediente/buscar_expediente.html', {'reportes_lista':DatosReportes.cargar_lista_expediente(),'reportes_usuarios':DatosReportes.cargar_usuario(),'expediente': expediente, 'mensaje': mensaje})
    
def list_pacientes():
    rsp_paciente = requests.get(url+'pacientes/')
    if rsp_paciente.status_code == 200:
        data = rsp_paciente.json()
        pacientes_list = data['pacientes']
        return pacientes_list
    else:
        pacientes_list = []
        return pacientes_list