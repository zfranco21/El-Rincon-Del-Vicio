document.addEventListener('DOMContentLoaded', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_username', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                if (data.logged_in) {
                    document.getElementById('boton-registro').style.display = 'none';
                    document.getElementById('boton-perfil').style.display = 'block';
                    document.getElementById('boton-perfil').querySelector('a').textContent = data.nombre_usuario;
                    document.getElementById('boton-perfil').querySelector('a').href = '/perfil';
                } else {
                    document.getElementById('boton-registro').style.display = 'block';
                    document.getElementById('boton-perfil').style.display = 'none';
                }
            }
        }
    };
    xhr.send();
});
