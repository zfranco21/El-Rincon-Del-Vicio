from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, name, email, password, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

users = []

def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None

class Comentario:
    def __init__(self, id_comentario, id_usuario, id_juego, texto_comentario, fecha_hora=None, usuario=None, juego=None):
        self.id_comentario = id_comentario
        self.id_usuario = id_usuario
        self.id_juego = id_juego
        self.texto_comentario = texto_comentario
        self.fecha_hora = fecha_hora if fecha_hora else datetime.utcnow()
        self.usuario = usuario
        self.juego = juego

    def __repr__(self):
        return '<Comentario {}>'.format(self.texto_comentario)
