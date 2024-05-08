document.addEventListener("DOMContentLoaded", function() {
    const pregunta = document.querySelectorAll(".faq .pregunta h2");
    
    pregunta.forEach(function(pregunta) {
      pregunta.addEventListener("click", function() {
        var parent = this.parentElement;
        if (parent.classList.contains("active")) {
          parent.classList.remove("active");
        } else {

          // Oculta todas las respuestas
          var respuesta = document.querySelectorAll(".faq .pregunta");
          respuesta.forEach(function(respuesta) {
            respuesta.classList.remove("active");
          });

          // Mostrar la respuesta de la pregunta seleccionada
          parent.classList.add("active");
        }
      });
    });
  });
  