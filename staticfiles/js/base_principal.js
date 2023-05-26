var opciones = document.querySelectorAll('.opcion > a');

opciones.forEach(function(opcion) {
  opcion.addEventListener('click', function(evento) {
    evento.preventDefault();
    var subopcion = this.nextElementSibling;
    if (subopcion.classList.contains('subopcion')) {
      subopcion.classList.toggle('mostrar');
    }
  });
});
const cuadroDialogo = document.getElementById('alert-alert-info');
if (cuadroDialogo) {
  setTimeout(function() {
    cuadroDialogo.style.display = 'none';
  }, 5000);
}