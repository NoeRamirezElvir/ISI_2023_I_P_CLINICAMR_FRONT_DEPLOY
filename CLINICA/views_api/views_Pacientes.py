from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'https://clinicamr.onrender.com/api/'
def listar_pacientes(request):
    response = requests.get(url+'pacientes/')
    if response.status_code == 200:
        data = response.json()
        pacientes = data['pacientes']
    else:
        pacientes  = []
    context = {'pacientes': pacientes}
    return render(request, 'Pacientes/buscarPaciente.html', context)


#METODO 2 EN 1, PRIMERO FUNCIONA PARA LLENAR EL SELECT DE EMPLEADOS
#CUANDO DETECTA QUE EL METODO ES POST ESTE FUNCIONA PARA PODER CREAR UN NUEVO USUARIO
def crear_paciente(request):
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
            data = rsp_TipoDocumento.json()
            TipoDocumento = data['documentos']
    else:
            TipoDocumento = []
    if request.method == 'POST':
        
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        fechaNacimiento = request.POST['fechaNacimiento']
        idTipoDocumento = int(request.POST['idTipoDocument1'])
        documento= request.POST ['documento']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST ['direccion']
        
        registro_temp={'nombre': nombre,'apellido': apellido,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'documento': documento,'telefono': telefono,'correo': correo,'direccion': direccion }
        response = requests.post(url+'pacientes/', json={'nombre': nombre,'apellido': apellido,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'documento': documento,'telefono': telefono,'correo': correo,'direccion': direccion })
        pacientedata={}
        if response.status_code == 200:
            pacientedata = response.json()
            mensaje = pacientedata['message']
            return render(request, 'Pacientes/Paciente.html', {'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'registro_temp':registro_temp})
        else:
            mensaje = pacientedata['message']
            
            return render(request, 'Pacientes/Paciente.html', {'mensaje': mensaje,  'TipoDocumento': TipoDocumento, 'registro_temp':registro_temp})
    else:
        return render(request, 'Pacientes/Paciente.html', { 'TipoDocumento': TipoDocumento})


def abrir_actualizar_pacientes(request):
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
            data = rsp_TipoDocumento.json()
            TipoDocumento = data['documentos']
    else:
            TipoDocumento = []
    if request.method == 'POST':
         resp = requests.get(url+'pacientes/busqueda/id/'+str(request.POST['id_pacientes']))
         data = resp.json()
         mensaje = data['message']
         if resp.status_code == 200:
            data = resp.json()
            pacientes = data['pacientes']
            mensaje = data['message']
         else:
            pacientes = []
         context = {'pacientes': pacientes,'TipoDocumento': TipoDocumento, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Pacientes/PacienteActualizar.html', context)   
    
def actualizar_pacientes(request, id):
    rsp_TipoDocumento = requests.get(url+'documentos/')
    if rsp_TipoDocumento.status_code == 200:
            data = rsp_TipoDocumento.json()
            TipoDocumento = data['documentos']
    else:
            TipoDocumento = []
                # FIN Metodo para llenar el SELECT de los Empleados
        #Obtener los datos para hacer la actualizacion
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        fechaNacimiento = request.POST['fechaNacimiento']
        idTipoDocumento = int(request.POST['idTipoDocument1'])
        documento= request.POST ['documento']
        telefono = request.POST['telefono']
        correo = request.POST['correo']
        direccion = request.POST ['direccion']
        


        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'pacientes/id/{idTemporal}', json={'nombre': nombre,'apellido': apellido,'fechaNacimiento': fechaNacimiento,'idTipoDocumento':idTipoDocumento,'documento': documento,'telefono': telefono,'correo': correo,'direccion': direccion })
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        pacientes = data['pacientes']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento})
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            pacientes = data['pacientes']
            mensaje = data['message']
            return render(request, 'Pacientes/PacienteActualizar.html', {'pacientes': pacientes, 'TipoDocumento':TipoDocumento})
        else:
            mensaje = data['message']
            return render(request, 'Pacientes/PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes, 'TipoDocumento':TipoDocumento})

def eliminar_pacientes(request, id):
    try:
        if request.method == 'POST':
            idTemporal = id
            response = requests.delete(url + f'pacientes/id/{idTemporal}')
            res = response.json()
            rsp_pacientes = requests.get(url + 'pacientes/') 
            if rsp_pacientes.status_code == 200:
                data = rsp_pacientes.json()
                pacientes = data['pacientes']
            else:
                pacientes = []
            mensaje = res['message']
            context = {'pacientes': pacientes, 'mensaje': mensaje}
            return render(request, 'Pacientes/buscarPaciente.html', context)     
    except:
        rsp_pacientes = requests.get(url + 'pacientes/') 
        if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            pacientes = data['pacientes']
        else:
            pacientes = []
        mensaje = 'No se puede eliminar, esta siendo utilizado en otros registros'
        context = {'pacientes': pacientes, 'error': mensaje}
        return render(request, 'Pacientes/buscarPaciente.html', context)     
            
def buscar_pacientes(request):
        valor = request.GET.get('buscador', None)
        url2 = url + 'pacientes/busqueda/'

        if valor is not None and (len(valor)>0):
            
            if valor.isdigit():
                id = int(valor)
                response = requests.get(url2 + f'id/{id}')
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pacientes = {}
                    pacientes = data['pacientes']
                    context = {'pacientes': pacientes, 'mensaje':mensaje}
                    return render(request, 'Pacientes/buscarPaciente.html', context) 
                else:
                    pacientes = []
                    mensaje = 'No se encontro paciente'
                    return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje})
        
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pacientes = {}
                    pacientes = data['pacientes']
                    context = {'pacientes': pacientes, 'mensaje':mensaje}
                    return render(request, 'Pacientes/buscarPaciente.html', context)
                else:
                    pacientes = []
                    mensaje = 'No se encontro paciente'
                    return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje})
    

        else:
            response = requests.get(url+'pacientes/')
            if response.status_code == 200:
                data = response.json()
                pacientes = data['pacientes']
                mensaje = data['message']   
                return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje})
            else:
                pacientes = []
                mensaje = 'No se encontro paciente'
            return render(request, 'Pacientes/buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje})
    
