-- Tabla de usuarios con sus atributos
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    correo_electronico VARCHAR(255) NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);    

-- Tabla de juegos con sus atributos
CREATE TABLE Juegos (
    id_juego INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    url_imagen VARCHAR(255) NOT NULL,
    descripcion TEXT,
    url_descarga VARCHAR(255) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    lanzamiento DATETIME NOT NULL
);

-- Tabla de calificaciones con sus atributos
CREATE TABLE Calificaciones (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_juego INT,
    calificacion DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_juego) REFERENCES Juegos(id_juego)
);

-- Tabla de comentarios con sus atributos
CREATE TABLE Comentarios (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_juego INT,
    texto_comentario TEXT NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_juego) REFERENCES Juegos(id_juego)
);
