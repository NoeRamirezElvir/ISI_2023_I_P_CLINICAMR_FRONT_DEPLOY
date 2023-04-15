  //Fecha Actual
  const fechaInput = document.getElementById('fechaRegistro');
  const fechaHidden = document.getElementById('fechaActual');
  const fechaActualUTC = new Date();
  const fechaActualLocal = new Date(fechaActualUTC.getTime() - fechaActualUTC.getTimezoneOffset() * 60000); // Convertir UTC a local
  const fechaFormateada = fechaActualLocal.toISOString().slice(0, 19).replace('T', ' '); // Formato local sin segundos ni milisegundos
  fechaInput.value = fechaFormateada;
  fechaHidden.value = fechaFormateada

  function activarInput() {
  var select = document.getElementById("idMetodo");
  var total = document.getElementById("total");
  var inputEfectivo = document.getElementById("montoEfectivo");
  var inputTarjeta = document.getElementById("montoTarjeta");
  var numeroTarjeta = document.getElementById("numeroTarjeta");
  var cambio = document.getElementById("cambio");
  var opcionSeleccionada = select.options[select.selectedIndex];
  var dato = opcionSeleccionada.getAttribute("data-nombre");
  
    if (dato === "efectivo") {
      inputEfectivo.removeAttribute("disabled");
      inputTarjeta.value = "00.00";
      inputEfectivo.oninput = function(){
        inputEfectivo.value = inputEfectivo.value.replace(/[^\d.]|\.(?=.*\.)/g, '');
        var to = parseFloat(total.value);
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
      inputTarjeta.setAttribute("disabled", "disabled");
      numeroTarjeta.setAttribute("disabled", "disabled");
    } else if (dato === "tarjeta"){
      inputTarjeta.removeAttribute("disabled");
      inputTarjeta.value = total.value
      inputEfectivo.value = "00.00"
      inputTarjeta.setAttribute("readonly", "readonly");
      numeroTarjeta.removeAttribute("disabled");
      inputEfectivo.setAttribute("disabled", "disabled");
    } else if (dato === "mixto"){
      inputEfectivo.removeAttribute("disabled");
      inputTarjeta.removeAttribute("disabled");
      inputEfectivo.oninput = function(){
        inputEfectivo.value = inputEfectivo.value.replace(/[^\d.]|\.(?=.*\.)/g, '');
        var to = parseFloat(total.value);
        var et = parseFloat(inputEfectivo.value);

        var t = isNaN(to) ? "00.00" : to.toFixed(2);
        var e = isNaN(et) ? "00.00" : et.toFixed(2);
        var valor = t-e;
        if (valor <= 0) {
          inputTarjeta.value = "00.00";
        }else{
          inputTarjeta.value = valor;
        } 
        
      }
      inputTarjeta.setAttribute("readonly", "readonly");
      numeroTarjeta.removeAttribute("disabled");
    } else {
      inputEfectivo.setAttribute("disabled", "disabled");
      inputTarjeta.setAttribute("disabled", "disabled");
      numeroTarjeta.setAttribute("disabled", "disabled");
      input.value = "00.00";
      inputEfectivo.value = "00.00";
      inputTarjeta.value = "00.00";
      numeroTarjeta.value = "XXXX XXXX XXXX XXXX";
    }
  }


