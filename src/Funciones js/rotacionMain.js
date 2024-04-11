//Franco: Crear una funcionalidad para rotar elementos de la pagina de inicio
//rotacion cada 5 segundos

const inicio = [{ 
    urlImagen: "https://www.youtube.com/embed/7b74IRV0vBg?si=xxuEC6DF0almOnto",
    sliderTitulo: "Street Fighter 3",
    sliderTexto: "Street Fighter Alpha 3 es un juego de lucha lanzado en 1998 conocido por su jugabilidad rápida y frenética, así como por su amplia selección de personajes. Es uno de los mejores juegos de lucha de la era de los 32 bits.",
},
{ 
    urlImagen: "https://www.youtube.com/embed/7b74IRV0vBg?si=xxuEC6DF0almOnto",
    sliderTitulo: "Resident Evil 2",
    sliderTexto: "Street Fighter Alpha 3 es un juego de lucha lanzado en 1998 conocido por su jugabilidad rápida y frenética, así como por su amplia selección de personajes. Es uno de los mejores juegos de lucha de la era de los 32 bits.",
}];

let currentIndex = 0;

function cambiar() {
    document.body.style.backgroundImage = "url('" + inicio[currentIndex].urlImagen + "')";
    document.getElementById("sliderTitulo").textContent = inicio[currentIndex].sliderTitulo;
    document.getElementById("sliderTexto").textContent = inicio[currentIndex].sliderTexto;
    currentIndex = (currentIndex + 1) % inicio.length;
}

setInterval(cambiar, 5000);
window.onload = cambiar;
