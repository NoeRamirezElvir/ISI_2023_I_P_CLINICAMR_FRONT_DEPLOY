from django.http import HttpResponse
import json
from django.shortcuts import render
import requests


url = 'http://localhost:8080/api/'
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
def crear_pacientes(request):
    rsp_pacientes = requests.get(url+'pacientes/')
    if rsp_pacientes.status_code == 200:
            data = rsp_pacientes.json()
            pacientes = data['pacientes']
    else:
            pacientes = []
    if request.method == 'POST':
        idTipoDocumento = int(request.POST['idTipoDocumento'])
        
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        FechaNacimiento = request.POST['FechaNacimiento']
        Tel = request.POST['Tel']
        Correo = request.POST['Correo']
        Direccion = request.Post ['Direccion']
        Documento= request.Post ['Documento']

        response = requests.post(url+'pacientes/', json={'idTipoDocumento':idTipoDocumento, 'nombre': nombre,'apellido': apellido,'FechaNacimiento': FechaNacimiento,'Tel': Tel,'Correo': Correo,'Direccion': Direccion,'Documento': Documento, })
        data={}
        if response.status_code == 200:
            data = response.json()
            mensaje = data['message']
            return render(request, 'Pacientes/Paciente.html')
        else:
            mensaje = data['pacientes']
            print(mensaje)
            return render(request, 'Pacientes/Paciente.html')
    else:
        return render(request, 'Pacientes/Paciente.html')
def abrir_actualizar_pacientes(request):
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
         context = {'pacientes': pacientes, 'mensaje':mensaje}
         mensaje = data['message']
         return render(request, 'Pacientes/PacienteActualizar.html', context)   
    
def actualizar_pacientes(request, id):
    if request.method == 'POST':
        idTemporal = id
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        


        #LLamar la consulta put, con la url especifica
        response = requests.put(url+f'pacientes/id/{idTemporal}', json={'nombre': nombre, 'descripcion': descripcion})
        #obtener la respuesta en la variable rsp
        rsp =  response.json()
        #Ya que se necesita llenar de nuevo el formulario se busca el cargo relacionado con el id
        res = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
        data = res.json()#se guarda en otra variable
        pacientes = data['pacientes']
        #Se valida el mensaje que viene de la consulta a la API, este viene con el KEY - MESSAGE
        if rsp['message'] == "La actualización fue exitosa.":
            mensaje = rsp['message']+'- Actualizado Correctamente'
            return render(request, 'PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes })
        else:
            mensaje = rsp['message']                            #Se necesitan enviar tanto los datos del usuario, el empleado y el mensaje de la consulta
            return render(request, 'PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes})
    else:
        #Y aqui no se que hice la verdad
        response = requests.get(url+f'pacientes/busqueda/id/{idTemporal}')
        if response.status_code == 200:
            data = response.json()
            usuario = data['pacientes']
            mensaje = data['message']
            return render(request, 'cargoactualizar.html', {'pacientes': pacientes})
        else:
            mensaje = data['message']
            return render(request, 'PacienteActualizar.html', {'mensaje': mensaje,'pacientes':pacientes})

def eliminar_pacientes(request, id):
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
        return render(request, 'buscarPaciente.html', context)     
    
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
                    print(context)
                    return render(request, 'buscarPaciente.html', context)       
            else:
                response = requests.get(url2+'nombre/'+valor)
                if response.status_code == 200:
                    data = response.json()
                    mensaje = data['message']
                    pacientes = {}
                    pacientes = data['pacientes']
                    context = {'pacientes': pacientes, 'mensaje':mensaje}
                    return render(request, 'buscarPaciente.html', context)
        else:
            response = requests.get(url+'pacientes/')
            if response.status_code == 200:
                data = response.json()
                pacientes = data['pacientes']
                mensaje = data['message']   
                return render(request, 'buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje})
            else:
                usuarios = []
                mensaje = 'No se encontro paciente'
            return render(request, 'buscarPaciente.html', {'pacientes': pacientes, 'mensaje': mensaje})
    
