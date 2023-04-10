  //Fecha Actual
  const fechaInput = document.getElementById('fechaRegistro');
  const fechaHidden = document.getElementById('fechaActual');
  const fechaActualUTC = new Date();
  const fechaActualLocal = new Date(fechaActualUTC.getTime() - fechaActualUTC.getTimezoneOffset() * 60000); // Convertir UTC a local
  const fechaFormateada = fechaActualLocal.toISOString().slice(0, 16); // Formato local sin segundos ni milisegundos
  fechaInput.value = fechaFormateada;
  fechaHidden.value = fechaFormateada
