// Obtener cada ventana modal
var ventanaModal1 = document.getElementById("miVentanaModal1");
var ventanaModal2 = document.getElementById("miVentanaModal2");
var ventanaModal3 = document.getElementById("miVentanaModal3");
var ventanaModal4 = document.getElementById("miVentanaModal4");
var ventanaModal5 = document.getElementById("miVentanaModal5");

// Obtener cada botón que abre su respectiva ventana modal
var botonAbrir1 = document.getElementById("miBotonAbrir1");
var botonAbrir2 = document.getElementById("miBotonAbrir2");
var botonAbrir3 = document.getElementById("miBotonAbrir3");
var botonAbrir4 = document.getElementById("miBotonAbrir4");
var botonAbrir5 = document.getElementById("miBotonAbrir5");

// Obtener el botón para cerrar cada ventana modal
var botonCerrar1 = document.getElementsByClassName("cerrar")[0];
var botonCerrar2 = document.getElementsByClassName("cerrar")[1];
var botonCerrar3 = document.getElementsByClassName("cerrar")[2];
var botonCerrar4 = document.getElementsByClassName("cerrar")[3];
var botonCerrar5 = document.getElementsByClassName("cerrar")[4];

// Cuando se hace clic en cada botón, se muestra su respectiva ventana modal
botonAbrir1.onclick = function() {
  ventanaModal1.style.display = "block";
}

botonAbrir2.onclick = function() {
  ventanaModal2.style.display = "block";
}

botonAbrir3.onclick = function() {
  ventanaModal3.style.display = "block";
}

botonAbrir4.onclick = function() {
  ventanaModal4.style.display = "block";
}

botonAbrir5.onclick = function() {
  ventanaModal5.style.display = "block";
}

// Cuando se hace clic en el botón de cerrar de cada ventana modal, se oculta la ventana modal correspondiente
botonCerrar1.onclick = function() {
  ventanaModal1.style.display = "none";
}

botonCerrar2.onclick = function() {
  ventanaModal2.style.display = "none";
}

botonCerrar3.onclick = function() {
  ventanaModal3.style.display = "none";
}

botonCerrar4.onclick = function() {
  ventanaModal4.style.display = "none";
}

botonCerrar5.onclick = function() {
  ventanaModal5.style.display = "none";
}

// Cuando el usuario hace clic en cualquier parte fuera de la ventana modal, esta se cierra
window.onclick = function(event) {
  if (event.target == ventanaModal1) {
    ventanaModal1.style.display = "none";
  }

  if (event.target == ventanaModal2) {
    ventanaModal2.style.display = "none";
  }

  if (event.target == ventanaModal3) {
    ventanaModal3.style.display = "none";
  }

  if (event.target == ventanaModal4) {
    ventanaModal4.style.display = "none";
  }

  if (event.target == ventanaModal5) {
    ventanaModal5.style.display = "none";
  }
}
