from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos MySQL en Railway
# Configuración de la base de datos MySQL en Railway
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pnxBFMWIFsWIMuULWAbEIpITJeKKRcDaT'
app.config['MYSQL_PORT'] = 10343
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Utiliza cursores tipo diccionario para facilitar el acceso a los datos

mysql = MySQL(app)

# Resto del código de la aplicación...


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
            return redirect(url_for('home'))

        except Exception as e:
            # Maneja el error en caso de que falle el registro
            return 'Error al registrar usuario: {}'.format(str(e))

    # Renderiza el formulario de registro
    return render_template('register.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['password']

        try:
            # Establece la conexión a la base de datos MySQL
            conexion = mysql.connection

            # Crea un cursor para ejecutar consultas SQL
            cursor = conexion.cursor()

            # Ejecuta una consulta SQL SELECT para buscar el usuario por correo electrónico
            consulta = "SELECT * FROM usuarios WHERE correo_electronico = %s"
            cursor.execute(consulta, (email,))
            usuario = cursor.fetchone()

            # Cierra el cursor
            cursor.close()

            if usuario:
                # Verifica si la contraseña ingresada coincide con la contraseña almacenada en la base de datos
                if check_password_hash(usuario['contrasena_hash'], contrasena):
                    # Inicia sesión y redirige al usuario a la página de inicio después del inicio de sesión exitoso
                    session['email'] = email
                    return redirect(url_for('home'))
                else:
                    # Mensaje de error si la contraseña es incorrecta
                    return 'Contraseña incorrecta'

            else:
                # Mensaje de error si el usuario no existe
                return 'Usuario no encontrado'

        except Exception as e:
            # Maneja el error en caso de que falle el inicio de sesión
            return 'Error al iniciar sesión: {}'.format(str(e))

    # Renderiza el formulario de inicio de sesión
    return render_template('login.html')

# Ruta para la página de inicio (requiere inicio de sesión)
@app.route('/home')
def home():
    if 'email' in session:
        return 'Bienvenido, {}'.format(session['email'])
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/perfil')
def perfil():
    if 'nombre_usuario' in session:
        return render_template('perfil.html', nombre=session['nombre_usuario'])
    else:
        return redirect(url_for('login'))
    
# Nueva ruta para obtener el nombre de usuario
@app.route('/get_username')
def get_username():
    if 'email' in session:
        try:
            # Establece la conexión a la base de datos MySQL
            conexion = mysql.connection

            # Crea un cursor para ejecutar consultas SQL
            cursor = conexion.cursor()

            # Ejecuta una consulta SQL SELECT para buscar el usuario por correo electrónico
            consulta = "SELECT nombre FROM usuarios WHERE correo_electronico = %s"
            cursor.execute(consulta, (session['email'],))
            usuario = cursor.fetchone()

            # Cierra el cursor
            cursor.close()

            if usuario:
                return jsonify({'logged_in': True, 'nombre_usuario': usuario['nombre']})
            else:
                return jsonify({'logged_in': False})

        except Exception as e:
            return jsonify({'error': 'Error al obtener el nombre de usuario: {}'.format(str(e))})

    else:
        return jsonify({'logged_in': False})
    

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.run(debug=True)