from flask import Flask, render_template, request, redirect, url_for, redirect, url_for
from forms import SignupForm, LoginForm
from flask_login import current_user, login_user, logout_user, LoginManager
from models import User, users, get_user
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL en Railwayp
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pnxBFMWIFsWIMuULWAbEIpITJeKKRcDaT'
app.config['MYSQL_PORT'] = 10343
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

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


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index', authenticated=True))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('signup_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login_form.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
