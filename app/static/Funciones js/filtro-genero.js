function filtrarJuegos(genero) {
    fetch(`/filtrar_juegos?genero=${genero}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('lista-juegos').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}
