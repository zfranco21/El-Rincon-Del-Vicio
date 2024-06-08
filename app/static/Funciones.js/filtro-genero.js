// Obtener botones de filtro
const btnAventura = document.getElementById('filtro-aventura');
const btnAccion = document.getElementById('filtro-accion');
const btnTerror = document.getElementById('filtro-terror');
const btnEstrategia = document.getElementById('filtro-estrategia');
const btnCasual = document.getElementById('filtro-casual');

// Evento de clic en los botones de filtro
btnAventura.addEventListener('click', () => filtrarJuegos('adventure'));
btnAccion.addEventListener('click', () => filtrarJuegos('Acción'));
btnTerror.addEventListener('click', () => filtrarJuegos('Terror'));
btnEstrategia.addEventListener('click', () => filtrarJuegos('Estrategia'));
btnCasual.addEventListener('click', () => filtrarJuegos('Casual'));

// Función para filtrar juegos por género
function filtrarJuegos(genero) {
    const juegos = document.querySelectorAll('.grid .flex-col'); // Selector de los juegos
    juegos.forEach(juego => {
        const juegoGenero = juego.querySelector('.text-white:nth-of-type(3)').textContent.split(': ')[1]; // Obtener el género del juego
        if (genero === 'Todos' || juegoGenero === genero) {
            juego.style.display = 'flex'; // Mostrar el juego si coincide con el género seleccionado o si se selecciona "Todos"
        } else {
            juego.style.display = 'none'; // Ocultar el juego si no coincide con el género seleccionado
        }
    });
}
