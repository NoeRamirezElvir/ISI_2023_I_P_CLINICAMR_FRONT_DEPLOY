
//Fecha Actual
  const fechaInput = document.getElementById('fechaRegistro');
  const fechaHidden = document.getElementById('fechaActual');
  const fechaActualUTC = new Date();
  const fechaActualLocal = new Date(fechaActualUTC.getTime() - fechaActualUTC.getTimezoneOffset() * 60000); // Convertir UTC a local
  const year = fechaActualLocal.getFullYear().toString(); // Get year
  const month = (fechaActualLocal.getMonth() + 1).toString().padStart(2, '0'); // Month needs to be zero-padded
  const day = fechaActualLocal.getDate().toString().padStart(2, '0'); // Day needs to be zero-padded
  const hours = fechaActualLocal.getHours().toString().padStart(2, '0'); // Hours needs to be zero-padded
  const minutes = fechaActualLocal.getMinutes().toString().padStart(2, '0'); // Minutes needs to be zero-padded
  const seconds = fechaActualLocal.getSeconds().toString().padStart(2, '0'); // Seconds needs to be zero-padded
  const fechaFormateada = `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
  fechaInput.value = fechaFormateada;
  fechaHidden.value = fechaFormateada;
  

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
      inputEfectivo.setAttribute("required","required");
      efectivoTemp = inputEfectivo.value;
      cambioTemp = cambio.value;
      inputEfectivo.value = '';
      if(efectivoTemp !== inputEfectivo.value){
        inputEfectivo.value = efectivoTemp;
        var to = parseFloat(total.value);
        var et = parseFloat(efectivoTemp);

        var t = isNaN(to) ? "" : to.toFixed(2);
        var e = isNaN(et) ? "" : et.toFixed(2);
        var valor = e-t;
        if (valor > 0) {
          cambio.value = valor;
        }else{
          cambio.value = '';
        }
      }
      inputEfectivo.oninput = function(){
        inputEfectivo.value = inputEfectivo.value.replace(/[^\d.]|\.(?=.*\.)/g, '');
        var to = parseFloat(total.value);
        var et = parseFloat(inputEfectivo.value);

        var t = isNaN(to) ? "" : to.toFixed(2);
        var e = isNaN(et) ? "" : et.toFixed(2);
        var valor = e-t;
        if (valor > 0) {
          cambio.value = valor;
        }else{
          cambio.value = '';
        }
      }
      inputTarjeta.setAttribute("disabled", "disabled");
      inputTarjeta.value = ''
      inputTarjeta.removeAttribute("required");
      numeroTarjeta.setAttribute("disabled", "disabled");
      numeroTarjeta.value = '';
      numeroTarjeta.removeAttribute("required");
    } else if (dato === "tarjeta"){
      inputTarjeta.removeAttribute("disabled");
      inputTarjeta.setAttribute("required","required");
      inputTarjeta.value = total.value
      inputTarjeta.setAttribute("readonly", "readonly");
      numeroTarjeta.removeAttribute("disabled");
      numeroTarjeta.setAttribute("required", "required");
      inputEfectivo.setAttribute("disabled", "disabled");
      inputEfectivo.removeAttribute("required");
      inputEfectivo.value = '';
      cambio.value = '';
    } else if (dato === "mixto"){
      inputEfectivo.removeAttribute("disabled");
      inputEfectivo.setAttribute("required","required");
      inputTarjeta.removeAttribute("disabled");
      inputTarjeta.setAttribute("required","required");
      cambio.value = '';
      efectivoTemp = inputEfectivo.value;
      numTargetaTemp = numeroTarjeta.value;
      tarjetaTemp = inputTarjeta.value;

      inputEfectivo.value = '';
      inputTarjeta.value = '';
      if(inputEfectivo.value !== efectivoTemp) {
        inputEfectivo.value = efectivoTemp
        var to = parseFloat(total.value);
        var et = parseFloat(efectivoTemp);

        var t = isNaN(to) ? "" : to.toFixed(2);
        var e = isNaN(et) ? "" : et.toFixed(2);
        var valor = t-e;
        if (valor > 0) {
          inputTarjeta.value = valor;
        }else{
          inputTarjeta.value = '';
        }
      }
      inputEfectivo.oninput = function(){
        inputEfectivo.value = inputEfectivo.value.replace(/[^\d.]|\.(?=.*\.)/g, '');
        var to = parseFloat(total.value);
        var et = parseFloat(inputEfectivo.value);

        var t = isNaN(to) ? "" : to.toFixed(2);
        var e = isNaN(et) ? "" : et.toFixed(2);
        var valor = t-e;
        if (valor > 0) {
          inputTarjeta.value = valor;
        }else{
          inputTarjeta.value = '';
        }
      }
      inputTarjeta.setAttribute("readonly", "readonly");
      numeroTarjeta.removeAttribute("disabled");
      numeroTarjeta.setAttribute("required","required");
      
    } else {
      inputEfectivo.setAttribute("disabled", "disabled");
      inputTarjeta.setAttribute("disabled", "disabled");
      numeroTarjeta.setAttribute("disabled", "disabled");
      inputEfectivo.removeAttribute("required");
      inputTarjeta.removeAttribute("required");
      numeroTarjeta.removeAttribute("required");
      inputEfectivo.value = '';
      inputTarjeta.value = '';
      numeroTarjeta.value = '';
    }
  }


