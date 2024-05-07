from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')

# Configuración de la base de datos MySQL en Railway
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pnxBFMWIFsWIMuULWAbEIpITJeKKRcDaT'
app.config['MYSQL_PORT'] = 10343
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Utiliza cursores tipo diccionario para facilitar el acceso a los datos

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register(): 
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['password']

        # Verifica la seguridad de la contraseña (puedes agregar más criterios según sea necesario)
        if len(contrasena) < 8:
            return 'La contraseña debe tener al menos 8 caracteres.'

        # Genera un hash de la contraseña antes de almacenarla en la base de datos
        hashed_password = generate_password_hash(contrasena)

        try:
            # Establece la conexión a la base de datos MySQL
            conexion = mysql.connection

            # Crea un cursor para ejecutar consultas SQL
            cursor = conexion.cursor()

            # Ejecuta una consulta SQL INSERT para insertar los datos en la base de datos
            consulta = "INSERT INTO usuarios (nombre, correo_electronico, contrasena_hash) VALUES (%s, %s, %s)"
            valores = (nombre, email, hashed_password)
            cursor.execute(consulta, valores)

            # Hace commit para confirmar los cambios en la base de datos
            conexion.commit()

            # Cierra el cursor
            cursor.close()

            # Redirige al usuario a la página de inicio de sesión después de completar el registro
            return redirect(url_for('login'))

        except Exception as e:
            # Maneja el error en caso de que falle el registro
            return 'Error al registrar usuario: {}'.format(str(e))

    # Renderiza el formulario de registro
    return render_template('register.html')

def obtener_perfil(username):
    # Aquí puedes agregar la lógica para obtener el perfil del usuario
    # Puedes acceder a la variable 'username' para identificar qué perfil se está solicitando
    # Por ahora, simplemente devolveremos un perfil de ejemplo
    perfil = {
        'username': username,
        'nombre': 'Usuario de ejemplo',
        'email': 'ejemplo@example.com',
        'bio': 'Esta es una breve biografía del usuario de ejemplo',
        # Agrega más detalles del perfil según sea necesario
    }
    # Devolver el perfil como una respuesta JSON
    return jsonify(perfil)

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
