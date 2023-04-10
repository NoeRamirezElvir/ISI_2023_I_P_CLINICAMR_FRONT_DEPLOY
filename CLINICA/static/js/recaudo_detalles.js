var medicamentosSeleccionados = [];
var tratamientosSeleccionados = [];
var examenesSeleccionados = [];

var total = 0;


function guardarMedicamento() {
  var medicamentosSeleccionado = document.getElementById("idMedicamento").value;
  var medicamentoPrecio = parseFloat(medicamentosSeleccionado.match(/(\d+\.\d{2})$/)[1]);

  if (!medicamentosSeleccionados.includes(medicamentosSeleccionado) && medicamentosSeleccionado != 0) {
    medicamentosSeleccionados.push(medicamentosSeleccionado);
    total += medicamentoPrecio;
    cargarTablaMedicamento();
    actualizarTotal();
  }
}

function guardarTratamiento() {
    var tratamientoSeleccionado = document.getElementById("idTratamiento").value;
    var tratamientoPrecio = parseFloat(tratamientoSeleccionado.match(/(\d+\.\d{2})$/)[1]);
  
    if (!tratamientosSeleccionados.includes(tratamientoSeleccionado) && tratamientoSeleccionado != 0) {
      tratamientosSeleccionados.push(tratamientoSeleccionado);
      total += tratamientoPrecio;
      cargarTablaTratamiento();
      actualizarTotal();
    }
  }

  function guardarExamen() {
    var examenesSeleccionado = document.getElementById("idExamen").value;
    var examenPrecio = parseFloat(examenesSeleccionado.match(/(\d+\.\d{2})$/)[1]);

    if (!examenesSeleccionados.includes(examenesSeleccionado) && examenesSeleccionado != 0) {
        examenesSeleccionados.push(examenesSeleccionado);
        total += examenPrecio;
        cargarTablaExamen();
        actualizarTotal();
    }
  }

//Tabla Medicamento
function cargarTablaMedicamento() {
  var tbody = document.querySelector("#myTableMedicamento tbody");
  tbody.innerHTML = ""; // Elimina todas las filas de la tabla

  for (var i = 0; i < medicamentosSeleccionados.length; i++) {
    var fila = document.createElement("tr");
    var valor = document.createElement("td");
    valor.innerText = medicamentosSeleccionados[i];
    fila.classList.add("td-fila-valor");
    var botonEliminar = document.createElement("button");
    botonEliminar.innerText = "Eliminar";
    botonEliminar.classList.add("eliminar-btn");

    botonEliminar.onclick = function() {
        var filaAEliminar = this.parentNode.parentNode;
        var valorAEliminar = filaAEliminar.getElementsByTagName("td")[0].innerText;
        var indice = medicamentosSeleccionados.indexOf(valorAEliminar);
        var medicamentoEliminar = medicamentosSeleccionados.splice(indice, 1)[0];
        var precioEliminado = parseFloat(medicamentoEliminar.split(" - ")[2]);
        total -= precioEliminado;
        cargarTablaMedicamento();
        actualizarTotal();
      }   

    var acciones = document.createElement("td");
    acciones.appendChild(botonEliminar);
    fila.appendChild(valor);
    fila.appendChild(acciones);
    tbody.appendChild(fila);
  }
}
//Tabla Tratamiento
function cargarTablaTratamiento() {
    var tbody = document.querySelector("#myTableTratamiento tbody");
    tbody.innerHTML = ""; // Elimina todas las filas de la tabla
  
    for (var i = 0; i < tratamientosSeleccionados.length; i++) {
      var fila = document.createElement("tr");
      var valor = document.createElement("td");
      valor.innerText = tratamientosSeleccionados[i];
      fila.classList.add("td-fila-valor");
      var botonEliminar = document.createElement("button");
      botonEliminar.innerText = "Eliminar";
      botonEliminar.classList.add("eliminar-btn");

      botonEliminar.onclick = function() {
        var filaAEliminar = this.parentNode.parentNode;
        var valorAEliminar = filaAEliminar.getElementsByTagName("td")[0].innerText;
        var indice = tratamientosSeleccionados.indexOf(valorAEliminar);
        var tratamientoEliminado = tratamientosSeleccionados.splice(indice, 1)[0];
        var precioEliminado = parseFloat(tratamientoEliminado.split(" - ")[2]);
        total -= precioEliminado;
        cargarTablaTratamiento();
        actualizarTotal();
      }
    
      var acciones = document.createElement("td");
      acciones.appendChild(botonEliminar);
      fila.appendChild(valor);
      fila.appendChild(acciones);
      tbody.appendChild(fila);
    }
  }
//Tabla Examen
function cargarTablaExamen() {
    var tbody = document.querySelector("#myTableExamen tbody");
    tbody.innerHTML = ""; // Elimina todas las filas de la tabla
  
    for (var i = 0; i < examenesSeleccionados.length; i++) {
      var fila = document.createElement("tr");
      var valor = document.createElement("td");
      valor.innerText = examenesSeleccionados[i];
      fila.classList.add("td-fila-valor");
      var botonEliminar = document.createElement("button");
      botonEliminar.innerText = "Eliminar";
      botonEliminar.classList.add("eliminar-btn");
      botonEliminar.onclick = function() {
        var filaAEliminar = this.parentNode.parentNode;
        var valorAEliminar = filaAEliminar.getElementsByTagName("td")[0].innerText;
        var indice = examenesSeleccionados.indexOf(valorAEliminar);
        examenesSeleccionados.splice(indice, 1);
        cargarTablaExamen();
        actualizarTotal();
      }

      botonEliminar.onclick = function() {
        var filaAEliminar = this.parentNode.parentNode;
        var valorAEliminar = filaAEliminar.getElementsByTagName("td")[0].innerText;
        var indice = examenesSeleccionados.indexOf(valorAEliminar);
        var medicamentoEliminado = examenesSeleccionados.splice(indice, 1)[0];
        var precioEliminado = parseFloat(medicamentoEliminado.split(" - ")[2]);
        total -= precioEliminado;
        cargarTablaExamen();
        actualizarTotal();
      }
    
      var acciones = document.createElement("td");
      acciones.appendChild(botonEliminar);
      fila.appendChild(valor);
      fila.appendChild(acciones);
      tbody.appendChild(fila);
    }
  }



  function actualizarTotal() {
    var precioTotalInput = document.getElementById("precio");
    precioTotalInput.value = isNaN(total) ? "00.00" : total.toFixed(2);
  }
  
  

//Este metodo es para poder acceder a la lista de sintomas (detalles de la enfermedad)
document.getElementById("myForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Previene que el formulario se envíe automáticamente
  
  var medicamentosSeleccionadosInput = document.getElementById("medicamentosSeleccionadosInput");
  var tratamientosSeleccionadosInput = document.getElementById("tratamientosSeleccionadosInput");
  var examenesSeleccionadosInput = document.getElementById("examenesSeleccionadosInput");
  medicamentosSeleccionadosInput.value = JSON.stringify(medicamentosSeleccionados);
  tratamientosSeleccionadosInput.value = JSON.stringify(tratamientosSeleccionados);
  examenesSeleccionadosInput.value = JSON.stringify(examenesSeleccionados);
  
  this.submit(); // Envía el formulario
});
