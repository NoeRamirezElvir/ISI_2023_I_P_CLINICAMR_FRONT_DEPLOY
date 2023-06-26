import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render
import requests
from ..views_api.datos_reporte import DatosReportes

url = 'https://clinicamr.onrender.com/api/'
def listar_citas(request):
    response = requests.get(url+'citas/')
    if response.status_code == 200:
        data = response.json()
        citas = data['citas']
    else:
        citas  = []
    context = {'citas': citas}
    return render(request, 'citas/cita_buscar.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_citas(request):
    rsp_paciente = requests.get(url+'pacientes/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            pacientes_list = data['pacientes']
    else:
            pacientes_list = []
    
    
    if request.method == 'POST':
        idPaciente = int(request.POST['idPaciente'])
        fechaActual= request.POST ['fechaActual']
        fechaProgramada = request.POST['fechaProgramada']
        fechaMaxima = request.POST['fechaMaxima']
        activa = int(request.POST['activado'])


        registro_temp = {'idPaciente':idPaciente,'fechaActual': fechaActual,'fechaProgramada': fechaProgramada,'fechaMaxima': fechaMaxima,'activa': activa }
        response = requests.post(url+'citas/', json={'idPaciente':idPaciente,'fechaActual': fechaActual,'fechaProgramada': fechaProgramada,'fechaMaxima': fechaMaxima,'activa': activa })
        pacientedata={}
        pacientedata = response.json()
        if response.status_code == 200:
            mensaje = pacientedata['message']
            return render(request, 'citas/cita.html', {'mensaje': mensaje,  'paciente_list': pacientes_list, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            mensaje = pacientedata['message']
            return render(request, 'citas/cita.html', {'mensaje': mensaje,  'paciente_list': pacientes_list, 'registro_temp':registro_temp,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    else:
        return render(request, 'citas/cita.html', { 'paciente_list': pacientes_list,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})


def abrir_actualizar_citas(request):
    
    
    rsp_paciente = requests.get(url+'pacientes/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            paciente_list = data['pacientes']
    else:
            paciente_list = []
    if request.method == 'POST':
         resp = requests.get(url+'citas/busqueda/id/'+str(request.POST['id_citas']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            citas = data['citas']
            mensaje = data['message']
         else:
            citas = []
         context = {'citas': citas,'paciente_list': paciente_list, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
         mensaje = data['message']
         return render(request, 'citas/cita_actualizar.html', context)   
    
def actualizar_citas(request, id):
    
    
    rsp_paciente = requests.get(url+'pacientes/')
    if rsp_paciente.status_code == 200:
            data = rsp_paciente.json()
            paciente_list = data['pacientes']
    else:
            paciente_list = []
            
    if request.method == 'POST':
        idTemporal = id
        idPaciente = int(request.POST['idPaciente'])
        fechaActual= request.POST ['fechaActual']
        fechaProgramada = request.POST['fechaProgramada']
        fechaMaxima = request.POST['fechaMaxima']
        activa = request.POST ['activado']

        response = requests.put(url+f'citas/id/{idTemporal}',json={'idPaciente':idPaciente,'fechaActual': fechaActual,'fechaProgramada': fechaProgramada,'fechaMaxima': fechaMaxima,'activa': activa })
        rsp =  response.json()
        res = requests.get(url+f'citas/busqueda/id/{idTemporal}')
        data = res.json()
        citas = data['citas']
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'citas/cita_actualizar.html', {'mensaje': mensaje,'citas':citas, 'paciente_list':paciente_list,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'citas/cita_actualizar.html', {'mensaje': mensaje,'citas':citas, 'paciente_list':paciente_list,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    else:
        idTemporal = id
        response = requests.get(url+f'citas/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            citas = data['citas']
            mensaje = data['message']
            return render(request, 'citas/cita_actualizar.html', {'citas': citas, 'paciente_list':paciente_list,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
        else:
            mensaje = data['message']
            return render(request, 'citas/cita_actualizar.html', {'mensaje': mensaje,'citas':citas, 'paciente_list':paciente_list,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})

def eliminar_citas(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'citas/id/{idTemporal}')
            res = response.json()
            rsp_pacientes = requests.get(url + 'citas/') 
            if rsp_pacientes.status_code == 200:
                data = rsp_pacientes.json()
                citas = data['citas']
            else:
                citas = []
            mensaje = res['message']
            
            
            context = {'citas': citas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
            return render(request, 'citas/cita_buscar.html', context)     
    except:
        rsp_pacientes = requests.get(url + 'citas/') 
        if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            citas = data['citas']
        else:
            citas = []
        
        
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'citas': citas, 'error': mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
        return render(request, 'citas/cita_buscar.html', context) 

def buscar_citas(request):
        
        
        valor = request.GET.get('buscador', None)
        url2 = url + 'citas/busqueda/'

        if valor is not None and (len(valor)>0):      
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                data = response.json()
                if data['citas']:
                    data = response.json()
                    mensaje = data['message']
                    citas = {}
                    citas = data['citas']
                    context = {'citas': citas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'citas/cita_buscar.html', context)
                
                else:
                    response = requests.get(url2+f'documento/{valor}')
                    data = response.json()
                    if data['citas']:
                        mensaje = data['message']
                        citas = {}
                        citas = data['citas']
                        context = {'citas': citas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                        return render(request, 'citas/cita_buscar.html', context)
                    else:
                        citas = []
                        mensaje = 'No se encontrarón citas'
                        context = {'citas': citas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                        return render(request, 'citas/cita_buscar.html', context)  
            else:
                response = requests.get(url2+f'documento/{valor}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    citas = {}
                    citas = data['citas']
                    context = {'citas': citas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'citas/cita_buscar.html', context)
                else:
                    citas = []
                    mensaje = 'No se encontrarón citas'
                    context = {'citas': citas, 'mensaje':mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()}
                    return render(request, 'citas/cita_buscar.html', context)  
        else:
            response = requests.get(url+'citas/')
            if response.status_code == 200:
                data = response.json()
                citas = data['citas']
                mensaje = data['message']   
                return render(request, 'citas/cita_buscar.html', {'citas': citas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
            else:
                citas = []
                mensaje = 'No se encontrarón citas'
            return render(request, 'citas/cita_buscar.html', {'citas': citas, 'mensaje': mensaje,'reportes_lista':DatosReportes.cargar_lista_citas(),'reportes_usuarios':DatosReportes.cargar_usuario()})
    
def abrir_calendario(request):
    response = requests.get(url+'citas/')
    if response.status_code == 200:
        data = response.json()
        citas = data['citas']
    else:
        citas  = []
    return render(request, 'citas/cita_calendario.html', {'citas': citas})