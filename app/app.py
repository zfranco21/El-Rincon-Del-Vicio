from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from flask_mysqldb import MySQL
from forms import SignupForm, LoginForm
from models import User
import os
import MySQLdb.cursors
import math
import MySQLdb

app = Flask(__name__)

# Configuración de la base de datos MySQL en Railway
app.config['MYSQL_HOST'] = 'roundhouse.proxy.rlwy.net' 
app.config['MYSQL_PORT'] = 16543 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aBhEAcCIorqmrzymnSjidmAuPxZQYEKf'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Inicialización de mysqldb
mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil')
@login_required
def perfil():
    # Obtén el ID del usuario actual
    user_id = current_user.id
    form = SignupForm()  # Crear una instancia del formulario SignupForm
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

@app.route('/juegos-indivi/<int:juegos_indivi_id>')
def juegos_indivi(juegos_indivi_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_juego, nombre, url_imagen, genero, lanzamiento, url_descarga FROM Juegos WHERE id_juego = %s', (juegos_indivi_id,))
    juegos_indivi = cursor.fetchone()
    cursor.close()
    if juegos_indivi:
        return render_template('juegos-indivi.html', juegos_indivi=juegos_indivi)
    else:
        return "Juego no encontrado", 404
    

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
        # Verificar si ya existe un usuario con el mismo correo electrónico
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario FROM Usuarios WHERE correo_electronico = %s", (email,))
        existing_user = cur.fetchone()
        cur.close()
        if existing_user:
            flash('Ya existe una cuenta con este correo electrónico. Por favor, inicia sesión.', 'error')
            return redirect(url_for('login'))
        else:
            # Si no existe, proceder con la inserción del nuevo usuario
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Usuarios (nombre, correo_electronico, contrasena_hash) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            # Obtener el ID del nuevo usuario insertado
            user_id = cur.lastrowid
            cur.close()
            # Crear una instancia de User con el ID insertado
            user = User(user_id, name, email, password)
            # Dejar al usuario logueado
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
        # Consulta SQL para obtener el usuario por su correo electrónico
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE correo_electronico = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        if user_data and user_data['contrasena_hash'] == password:
            # esto crea una instancia de User con los datos recuperados de la base de datos, sirve para el logueo de una cuenta ya creada
            user = User(user_data['id_usuario'], user_data['nombre'], user_data['correo_electronico'], user_data['contrasena_hash'])
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login_form.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    # Consulta SQL para obtener el usuario por su ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data['id_usuario'], user_data['nombre'], user_data['correo_electronico'], user_data['contrasena_hash'])
    return None

@app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))

UPLOAD_FOLDER = 'static/profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@login_required
def eliminar_usuario(user_id):
    if current_user.is_admin or current_user.id == user_id:
        # esto ayuda a eliminar el usuario de la base de datos
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (user_id,))
            mysql.connection.commit()
        flash('Usuario eliminado correctamente', 'success')
        return redirect(url_for('index'))
    else:
        abort(403)

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
