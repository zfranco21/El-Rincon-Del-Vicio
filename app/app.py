from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from flask_mysqldb import MySQL
import os
import MySQLdb.cursors
import math
from datetime import datetime
from forms import SignupForm, LoginForm
from models import User

app = Flask(__name__)

# Configuración de la base de datos MySQL en Railway
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_PORT'] = 59963
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LZDxAybpKOralbJsehIgVKxJyPLmYsXl'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Inicialización de mysqldb
mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil')
@login_required
def perfil():
    user_id = current_user.id
    form = SignupForm()
    return render_template('perfil.html', user_id=user_id, form=form)

@app.route('/juegos')
def juegos():
    page = request.args.get('page', 1, type=int)
    per_page = 9
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(*) FROM Juegos')
    total_products = cursor.fetchone()['COUNT(*)']
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_juego, nombre, url_imagen, genero, lanzamiento FROM Juegos LIMIT %s OFFSET %s', (per_page, offset))
    products = cursor.fetchall()
    cursor.close()

    total_pages = math.ceil(total_products / per_page)

    return render_template('juegos.html', products=products, page=page, total_pages=total_pages)

@app.route('/juegos-indivi/<int:juegos_indivi_id>', methods=['GET', 'POST'])
def juegos_indivi(juegos_indivi_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_juego, nombre, url_imagen, genero, lanzamiento, url_descarga FROM Juegos WHERE id_juego = %s', (juegos_indivi_id,))
    juegos_indivi = cursor.fetchone()
    cursor.close()
    
    if not juegos_indivi:
        return "Juego no encontrado", 404

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Por favor, inicia sesión para comentar.')
            return redirect(url_for('login'))
        
        texto_comentario = request.form['texto_comentario']
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        id_usuario = current_user.id

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Comentarios (id_usuario, id_juego, texto_comentario, fecha_hora) VALUES (%s, %s, %s, %s)', 
                       (id_usuario, juegos_indivi_id, texto_comentario, fecha_hora))
        mysql.connection.commit()
        cursor.close()

        flash('Comentario agregado!')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT c.id_comentario, c.texto_comentario, c.fecha_hora, u.nombre FROM Comentarios c JOIN Usuarios u ON c.id_usuario = u.id_usuario WHERE c.id_juego = %s ORDER BY c.fecha_hora DESC', (juegos_indivi_id,))
    comentarios = cursor.fetchall()
    cursor.close()

    return render_template('juegos-indivi.html', juegos_indivi=juegos_indivi, comentarios=comentarios)

@app.route('/filtrar_juegos', methods=['GET'])
def filtrar_juegos():
    genero = request.args.get('genero')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_juego, nombre, url_imagen, genero, lanzamiento FROM Juegos WHERE genero = %s', (genero,))
    products = cursor.fetchall()
    cursor.close()
    
    return render_template('juegos_filtrados.html', products=products)

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index', authenticated=True))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario FROM Usuarios WHERE correo_electronico = %s", (email,))
        existing_user = cur.fetchone()
        cur.close()
        if existing_user:
            flash('Ya existe una cuenta con este correo electrónico. Por favor, inicia sesión.', 'error')
            return redirect(url_for('login'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Usuarios (nombre, correo_electronico, contrasena_hash) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            user_id = cur.lastrowid
            cur.close()
            user = User(user_id, name, email, password)
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template('signup_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE correo_electronico = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        if user_data and user_data['contrasena_hash'] == password:
            user = User(user_data['id_usuario'], user_data['nombre'], user_data['correo_electronico'], user_data['contrasena_hash'])
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login_form.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        # Obtiene el valor de is_admin de la base de datos
        is_admin = user_data['is_admin']
        return User(user_data['id_usuario'], user_data['nombre'], user_data['correo_electronico'], user_data['contrasena_hash'], is_admin)
    return None

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@login_required
def eliminar_usuario(user_id):
    if current_user.is_admin or current_user.id == user_id:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (user_id,))
            mysql.connection.commit()
        flash('Usuario eliminado correctamente', 'success')
        return redirect(url_for('index'))
    else:
        abort(403)

@app.route('/subir_juego', methods=['POST'])
@login_required
def subir_juego():
    if not current_user.is_admin:
        flash('No tienes permisos para realizar esta acción.', 'error')
        return redirect(url_for('perfil'))
    
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    url_descarga = request.form['url_descarga']
    genero = request.form['genero']
    lanzamiento = request.form['lanzamiento']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO Juegos (nombre, descripcion, url_descarga, genero, lanzamiento) VALUES (%s, %s, %s, %s, %s)', 
                   (nombre, descripcion, url_descarga, genero, lanzamiento))
    mysql.connection.commit()
    cursor.close()

    flash('Juego subido con éxito!', 'success')
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
