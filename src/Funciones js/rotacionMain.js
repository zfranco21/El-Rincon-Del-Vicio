//Franco: Crear una funcionalidad para rotar elementos de la pagina de inicio.
//elementos a rotar: Video, titulos del juego,Descripcion y url para ver el trailer.
//rotacion cada 5 segundos.


//constante incio que guarda los cambios que deben hacerse en un array
const inicio = [
    { 
        video: "https://www.youtube.com/embed/7b74IRV0vBg?si=xxuEC6DF0almOnto",
        sliderTitulo: "Street Fighter 3",
        sliderTexto: "Street Fighter Alpha 3 es un juego de lucha lanzado en 1998 de jugabilidad rápida y frenética, con una amplia selección de personajes. Es de los mejores juegos de lucha de la era de los 32 bits.",
        trailer: "https://www.youtube.com/watch?v=7b74IRV0vBg&t=1055s",
    },
    { 
        video: "https://www.youtube.com/embed/UZNOI3VTWBk?si=wTx2pRakdWUBYKWg",
        sliderTitulo: "Metal Gear Solid",
        sliderTexto: "Metal Gear Solid es un videojuego de acción-aventura y sigilo desarrollado por Konami. Lanzado originalmente para la PlayStation en 1998, es uno de los títulos más influyentes de su generación.",
        trailer: "https://www.youtube.com/watch?v=UZNOI3VTWBk&t=1s",
    },
    { 
        video: "https://www.youtube.com/embed/A4OuWAvDLBo?si=J9Pyzu9ov1D7mPx7",
        sliderTitulo: "Medal Of Honor",
        sliderTexto: "Esta saga se centra en ofrecer al jugador videojuegos de disparos de corte bélico que habitualmente están ambientados durante la Segunda Guerra Mundial.",
        trailer: "https://www.youtube.com/watch?v=A4OuWAvDLBo",
    }
];

//le decimos que arranque desde el elemento 0, osea el primero.
let currentIndex = 0;

//Creamos la funcion que va a interactuar con los ID de cada elemento en el html.
//le pasamos las id de los elementos que queremos cambiar
//accedemos con .src o .textContent al contenido especifico que necesitamos
//luego le decimos que cambie el contenido ID por lo que esta en nuestra variable inicio
//y por ultimo currentIndex nos ayuda a pasar los videos 1 x 1 y cuando llegue al ultimo vuelva al primero.
function cambiar() {
    document.getElementById("videoFrame").src = inicio[currentIndex].video;
    document.getElementById("sliderTitulo").textContent = inicio[currentIndex].sliderTitulo;
    document.getElementById("sliderTexto").textContent = inicio[currentIndex].sliderTexto;
    document.getElementById("trailer").href = inicio[currentIndex].trailer;
    currentIndex = (currentIndex + 1) % inicio.length;
}

//use setInterval que es un metodo de bucle cada cierto tiempo
//como tenemos un array, va a ir pasando de un elemento a otro cada 7 segundos, y luego se reinicia el bucle.
setInterval(cambiar, 7000);
window.onload = cambiar;
//Window.onload = cambiar; : Esto le dice al navegador que cuando cargue toda la pagina empiece la funcion cambiar.
