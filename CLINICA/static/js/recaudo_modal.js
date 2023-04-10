// Obtener cada ventana modal
var ventanaModal1 = document.getElementById("miVentanaModal1");
var ventanaModal2 = document.getElementById("miVentanaModal2");
var ventanaModal3 = document.getElementById("miVentanaModal3");

// Obtener cada botón que abre su respectiva ventana modal
var botonAbrir1 = document.getElementById("miBotonAbrir1");
var botonAbrir2 = document.getElementById("miBotonAbrir2");
var botonAbrir3 = document.getElementById("miBotonAbrir3");

// Obtener el botón para cerrar cada ventana modal
var botonCerrar1 = document.getElementsByClassName("cerrar")[0];
var botonCerrar2 = document.getElementsByClassName("cerrar")[1];
var botonCerrar3 = document.getElementsByClassName("cerrar")[2];

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
}
