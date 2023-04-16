var medicamentosSeleccionados = [];
var tratamientosSeleccionados = [];
var examenesSeleccionados = [];


var total = 0;
var subtotal = 0;
var imp = 0;
var precioTemp = 0;
var impuestoTemp = 0;
var cambio = document.getElementById("cambio");
var inputEfectivo = document.getElementById("montoEfectivo");

function actualizarVariables(total, subtotal, imp) {
  // Actualizar las variables globales del archivo JavaScript
  this.total = total;
  this.subtotal = subtotal;
  this.imp = imp;
}

function guardarMedicamento() {
  var medicamentosSeleccionado = document.getElementById("idMedicamento").value;
  var valores = medicamentosSeleccionado.split(" - ");
  var valores = medicamentosSeleccionado.split(" - ");
  var precio = parseFloat(valores[2]);
  var impuesto = parseFloat(valores[3]);
  var can = parseInt(valores[4], 10);

  if (medicamentosSeleccionado != 0 && !medicamentosSeleccionados.some(m => m.startsWith(valores[0]))) {
    medicamentosSeleccionados.push(medicamentosSeleccionado);
    subtotal += (precio) * can;
    imp += (precio * impuesto) * can;
    total += (precio + ( precio * impuesto)) * can;
    cargarTablaMedicamento();
    actualizarTotal();
  }
}


function guardarTratamiento() {
    var tratamientoSeleccionado = document.getElementById("idTratamiento").value;
    var valores = tratamientoSeleccionado.split(" - ");
    var precio = parseFloat(valores[2]);
    var impuesto = parseFloat(valores[3]);

    if (!tratamientosSeleccionados.includes(tratamientoSeleccionado) && tratamientoSeleccionado != 0) {
      tratamientosSeleccionados.push(tratamientoSeleccionado);
      subtotal += precio;
      imp += (precio * impuesto);
      total += precio + ( precio * impuesto);
      cargarTablaTratamiento();
      actualizarTotal();
    }
  }

  function guardarExamen() {
    var examenesSeleccionado = document.getElementById("idExamen").value;
    var valores = examenesSeleccionado.split(" - ");
    var precio = parseFloat(valores[2]);
    var impuesto = parseFloat(valores[3]);

    if (!examenesSeleccionados.includes(examenesSeleccionado) && examenesSeleccionado != 0) {
        examenesSeleccionados.push(examenesSeleccionado);
        subtotal += precio;
        imp += (precio * impuesto);
        total += precio + ( precio * impuesto);
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
    // Columna para el nombre del medicamento
    var valor = document.createElement("td");
    valor.innerText = medicamentosSeleccionados[i];
    fila.classList.add("td-fila-valor");

    // Columna para la cantidad
    var cantidad = document.createElement("td");
    var cantidadInput = document.createElement("input");
    cantidadInput.type = "number";
    cantidadInput.min = "1";
    cantidadInput.value = medicamentosSeleccionados[i].split(" - ")[4]; // Valor predeterminado es 1
    cantidadInput.classList.add("cantidad-input");

    cantidadInput.oninput = function(){
      cantidadInput.value = cantidadInput.value.replace(/[^\d.]|\.(?=.*\.)/g);
    }
    cantidadInput.onchange = function() {
      var filaAModificar = this.parentNode.parentNode;
      var nombreMedicamento = filaAModificar.getElementsByTagName("td")[0].innerText;
      var indice = medicamentosSeleccionados.findIndex(medicamento => medicamento.includes(nombreMedicamento));
      medicamentosSeleccionados[indice] = medicamentosSeleccionados[indice].split(" - ")[0] + " - " + medicamentosSeleccionados[indice].split(" - ")[1] + " - " + medicamentosSeleccionados[indice].split(" - ")[2] + " - " + medicamentosSeleccionados[indice].split(" - ")[3] + " - " + this.value; // Actualiza la cantidad en el array
      
      var valores = nombreMedicamento.split(" - ");
      var precio = parseFloat(valores[2]);
      var impuesto = parseFloat(valores[3]);

      var canTemp = parseInt(valores[4],10);
      var can = parseInt(this.value, 10);

      if (!isNaN(can)) {
        canTemp = canTemp - 1;
        subtotal -= ((precio))* canTemp;
        imp -= ((precio * impuesto))* canTemp;
        total -= ((precio + ( precio * impuesto)))* canTemp;
        canTemp = parseInt(valores[4],10);
  
        can = can -  1;
        subtotal += ((precio))* can;
        imp += ((precio * impuesto))* can;
        total += ((precio + ( precio * impuesto)))* can;
        can = parseInt(this.value, 10);
      }
      cargarTablaMedicamento();
      actualizarTotal();
    }

    cantidad.appendChild(cantidadInput);

    // Columna para el botón de eliminar
    var botonEliminar = document.createElement("button");
    botonEliminar.innerText = "Eliminar";
    botonEliminar.classList.add("eliminar-btn");

    botonEliminar.onclick = function() {
        var filaAEliminar = this.parentNode.parentNode;
        var valorAEliminar = filaAEliminar.getElementsByTagName("td")[0].innerText;
        var indice = medicamentosSeleccionados.indexOf(valorAEliminar);
        var medicamentoEliminar = medicamentosSeleccionados.splice(indice, 1)[0];
        var precioEliminado = parseFloat(medicamentoEliminar.split(" - ")[2]);
        var impuestoEliminado = parseFloat(medicamentoEliminar.split(" - ")[3]);
        var cantidadEliminada = parseInt(filaAEliminar.getElementsByClassName("cantidad-input")[0].value);
        total -= (precioEliminado  + (precioEliminado * impuestoEliminado))*cantidadEliminada;
        imp -= ((precioEliminado * impuestoEliminado))*cantidadEliminada;
        subtotal -= (precioEliminado)*cantidadEliminada;
        cargarTablaMedicamento();
        actualizarTotal();
      }

    // Columna para las acciones
    var acciones = document.createElement("td");
    acciones.appendChild(botonEliminar);

    // Agregar todas las columnas a la fila
    fila.appendChild(valor);
    fila.appendChild(cantidad);
    fila.appendChild(acciones);

    // Agregar la fila a la tabla
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
        var impuestoEliminado = parseFloat(tratamientoEliminado.split(" - ")[3]);
        total -= precioEliminado + (precioEliminado * impuestoEliminado);
        imp -= (precioEliminado * impuestoEliminado);
        subtotal -= precioEliminado
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
        var examenEliminado = examenesSeleccionados.splice(indice, 1)[0];
        var precioEliminado = parseFloat(examenEliminado.split(" - ")[2]);
        var impuestoEliminado = parseFloat(examenEliminado.split(" - ")[3]);
        total -= precioEliminado + (precioEliminado * impuestoEliminado);
        imp -= (precioEliminado * impuestoEliminado);
        subtotal -= precioEliminado
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

  function guardarConsulta(){
    var select = document.getElementById("idConsulta");
    var opcionSeleccionada = select.options[select.selectedIndex];
    var precio = parseFloat(opcionSeleccionada.getAttribute("data-precio"));
    var impuesto = parseFloat(opcionSeleccionada.getAttribute("data-impuesto"));
    subtotal -= precioTemp;
    imp -= (precioTemp * impuestoTemp);
    total -= precioTemp + (precioTemp * impuestoTemp);

    precioTemp = precio;
    impuestoTemp = impuesto;

    subtotal += precio;
    imp += (precio * impuesto);
    total += precio + ( precio * impuesto);

    actualizarTotal();

  }


  function actualizarTotal() {
    var precioSubTotalInput = document.getElementById("subtotal");
    var precioTotalInput = document.getElementById("total");
    var impuestoTotalInput = document.getElementById("imp");
    precioTotalInput.value = isNaN(total) ? "00.00" : total.toFixed(2);
    precioSubTotalInput.value = isNaN(subtotal) ? "00.00" : subtotal.toFixed(2);
    impuestoTotalInput.value = isNaN(imp) ? "00.00" : imp.toFixed(2);
    
    var to = parseFloat(precioTotalInput.value);
    var et = parseFloat(inputEfectivo.value);

    var t = isNaN(to) ? "00.00" : to.toFixed(2);
    var e = isNaN(et) ? "00.00" : et.toFixed(2);
    var valor = e-t;
    if (valor <= 0) {
      cambio.value = "00.00";
    }else{
      cambio.value = valor;
    }
  }
  
  

//Este metodo es para poder acceder a la lista de items (detalles de la enfermedad)
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
