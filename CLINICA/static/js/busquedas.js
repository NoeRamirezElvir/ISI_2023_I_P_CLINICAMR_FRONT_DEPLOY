
  function filtrarMedicamentos() {
    const input = document.getElementById("buscarMedicamento");
    const valor = input.value.toLowerCase(); // Convertir el valor a minúsculas
  
    const select = document.getElementById("idMedicamento");
    select.innerHTML = '<option value="0" selected>Seleccione una opción</option>'; // Vaciar el select
    var medicamentosb = document.getElementById("medicamentosb").value;
    medicamentosb = medicamentosb.replace(/'/g, '"');
    var medicamentos = JSON.parse(medicamentosb);
  
    // Recorrer la lista de medicamentos y agregar las opciones que coincidan con el texto ingresado
    for (const item of medicamentos) {
      const nombre = item.nombre.toLowerCase();
      if (nombre.includes(valor)) {
        const option = document.createElement("option");
        option.value = `${item.id} - ${item.nombre} - ${item.precioVenta} - ${item.idImpuesto.nombre} - 1`;
        option.textContent = `${item.id}) ${item.nombre} Stock Minimo ${item.stockMinimo} Stock Actual ${item.stockActual}`;
        select.appendChild(option);
      }
    }
  
    // Si no hay opciones, mostrar un mensaje
    if (select.options.length === 1) {
      const option = document.createElement("option");
      option.disabled = true;
      option.textContent = "No se encontraron medicamentos";
      select.appendChild(option);
    }
  }
  
  
  function filtrarTratamientos() {
    const input = document.getElementById("buscarTratamiento");
    const valor = input.value.toLowerCase(); // Convertir el valor a minúsculas
  
    const select = document.getElementById("idTratamiento");
    select.innerHTML = '<option value="0" selected>Seleccione una opción</option>'; // Vaciar el select
    var tratamientosb = document.getElementById("tratamientosb").value;
    tratamientosb = tratamientosb.replace(/'/g, '"');
    var tratamientos = JSON.parse(tratamientosb);
  
    // Recorrer la lista de tratamientos y agregar las opciones que coincidan con el texto ingresado
    for (const item of tratamientos) {
      const nombrePaciente = item.idPaciente.nombre.toLowerCase();
      const documento = item.idPaciente.documento;
      const nombreTratamiento = item.idTipo.nombre.toLowerCase();
      if (nombrePaciente.includes(valor) || documento.includes(valor) || nombreTratamiento.includes(valor)) {
        const option = document.createElement("option");
        option.value = `${item.id} - ${item.idTipo.nombre} - ${item.idTipo.precio} - ${item.idTipo.impuesto}`;
        option.textContent = `${item.id} ${item.idTipo.nombre}: ${item.idPaciente.nombre} ${item.idPaciente.documento}`;
        select.appendChild(option);
      }
    }
  
    // Si no hay opciones, mostrar un mensaje
    if (select.options.length === 1) {
      const option = document.createElement("option");
      option.disabled = true;
      option.textContent = "No se encontraron tratamientos";
      select.appendChild(option);
    }
  }
  
  function filtrarExamenes() {
    const input = document.getElementById("buscarExamen");
    const valor = input.value.toLowerCase(); // Convertir el valor a minúsculas
  
    const select = document.getElementById("idExamen");
    select.innerHTML = '<option value="0" selected>Seleccione una opción</option>'; // Vaciar el select
    var examenesb = document.getElementById("examenesb").value;
    examenesb = examenesb.replace(/'/g, '"');
    var examenes = JSON.parse(examenesb);
  
    // Recorrer la lista de tratamientos y agregar las opciones que coincidan con el texto ingresado
    for (const item of examenes) {
        const nombrePaciente = item.idMuestra.idPaciente.nombre.toLowerCase();
        const documento = item.idMuestra.idPaciente.documento;
        const nombreExamen = item.idTipo.nombre.toLowerCase();
      if (nombrePaciente.includes(valor) || documento.includes(valor) || nombreExamen.includes(valor)) {
        const option = document.createElement("option");
        option.value = `${item.id} - ${item.idTipo.nombre} - ${item.idTipo.precio} - ${item.idTipo.impuesto}`;
        option.textContent = `${item.id} ${item.idTipo.nombre}: ${item.idMuestra.idPaciente.nombre} ${item.idMuestra.idPaciente.documento}`;
        select.appendChild(option);
      }
    }
  
    // Si no hay opciones, mostrar un mensaje
    if (select.options.length === 1) {
      const option = document.createElement("option");
      option.disabled = true;
      option.textContent = "No se encontraron examenes";
      select.appendChild(option);
    }
  }
  
  function filtrarConsultas() {
    const input = document.getElementById("buscarConsulta");
    const valor = input.value.toLowerCase(); // Convertir el valor a minúsculas
  
    const select = document.getElementById("selectConsulta");
    select.innerHTML = '<option value="0" data-precio="00.00" data-impuesto="00.00" selected>Seleccione una opción</option>'; // Vaciar el select
    var consultasb = document.getElementById("consultasb").value;
    consultasb = consultasb.replace(/'/g, '"');
    var consultas = JSON.parse(consultasb);

    // Recorrer la lista de consultas y agregar las opciones que coincidan con el texto ingresado
    for (const consulta of consultas) {
      const nombre = consulta.idTipo.nombre.toLowerCase();
      const documento = consulta.idCita.idPaciente.documento.toLowerCase();
      if (nombre.includes(valor) || documento.includes(valor)) {
        const option = document.createElement("option");
        option.value = consulta.id;
        option.textContent = `${consulta.id} - ${consulta.idTipo.nombre} : ${consulta.idCita.idPaciente.documento}`;
        option.dataset.precio = consulta.idTipo.precio;
        option.dataset.impuesto = consulta.idTipo.impuesto;

        select.appendChild(option);
      }
    }
  
    // Si no hay opciones, mostrar un mensaje
    if (select.options.length === 1) {
      const option = document.createElement("option");
      option.disabled = true;
      option.textContent = "No se encontraron consultas";
      select.appendChild(option);
    }
  }
  
  function filtrarPacientes() {
    const input = document.getElementById("buscarPacientes");
    const valor = input.value.toLowerCase(); // Convertir el valor a minúsculas
  
    const select = document.getElementById("selectPaciente");
    select.innerHTML = '<option value="0" selected>Consumidor Final</option>'; // Vaciar el select y agregar la opción por defecto
    var pacientesb = document.getElementById("pacientesb").value;
    guardarCliente();
    pacientesb = pacientesb.replace(/'/g, '"');
    var pacientes = JSON.parse(pacientesb);

    // Recorrer la lista de pacientes y agregar las opciones que coincidan con el texto ingresado
    for (const item of pacientes) {
      const nombre = item.nombre.toLowerCase();
      const apellido = item.apellido.toLowerCase();
      const documento = item.documento;
      if (nombre.includes(valor) || apellido.includes(valor) || documento.includes(valor)) {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = `${item.id} - ${item.nombre} ${item.apellido} ${item.documento}`;

        select.appendChild(option);
      }
    }
  
    // Si no hay opciones, mostrar un mensaje
    if (select.options.length === 1) {
      const option = document.createElement("option");
      option.disabled = true;
      option.textContent = "No se encontraron pacientes";
      select.appendChild(option);
    }
  }
  
  function guardarCliente(){
    var inputPaciente = document.getElementById("idPaciente");
    var select = document.getElementById("selectPaciente");
    var opcionSeleccionada = select.options[select.selectedIndex];

    inputPaciente.value = opcionSeleccionada.value;
  }