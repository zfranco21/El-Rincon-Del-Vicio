from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/static')

# Configuración de la base de datos MySQL en Railwayp
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pnxBFMWIFsWIMuULWAbEIpITJeKKRcDaT'
app.config['MYSQL_PORT'] = 10343
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil')
def perfil():
    # Aquí va la lógica del perfil
    return render_template('perfil.html')

@app.route('/juegos')
def juegos():
    # Aquí va la lógica para manejar la ruta /juegos
    return render_template('juegos.html')

@app.route('/noticias')
def noticias():
    # Aquí va la lógica para manejar la ruta /noticias
    return render_template('noticias.html')

@app.route('/ayuda')
def ayuda():
    # Aquí va la lógica para manejar la ruta /ayuda
    return render_template('ayuda.html')

@app.route('/register')
def register():
    # Aquí va la lógica para manejar la ruta /register
    return render_template('register.html')

@app.route('/login')
def login():
    # Aquí va la lógica para manejar la ruta /login
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
