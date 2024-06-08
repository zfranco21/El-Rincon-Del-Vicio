// Lista de imágenes de publicidad
const adImages = [
    '/static/img/publi/euroTruck.jpg',
    '/static/img/publi/lolMobile.jpg',
    '/static/img/publi/play.jpg'
];

// Función para obtener una imagen aleatoria
function getRandomAdImage() {
    const randomIndex = Math.floor(Math.random() * adImages.length);
    return adImages[randomIndex];
}

// Cambiar la imagen de publicidad al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const adImageElement = document.getElementById('ad-image');
    if (adImageElement) {
        adImageElement.src = getRandomAdImage();
    } else {
        console.error('El elemento con id "ad-image" no se encontró en el DOM.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const adImageElement = document.getElementById('ad-image1');
    if (adImageElement) {
        adImageElement.src = getRandomAdImage();
    } else {
        console.error('El elemento con id "ad-image" no se encontró en el DOM.');
    }
});