from flask import request

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contraseña = request.form['contraseña']

    # Aquí puedes realizar la inserción de datos en la base de datos
    # utilizando las consultas SQL adecuadas
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Usuarios (nombre, correo_electronico, contrasena_hash) VALUES (%s, %s, %s)", (nombre, correo, contraseña))
    mysql.connection.commit()
    cursor.close()

    return 'Usuario registrado correctamente'


#Contendría el código principal de tu aplicación Flask, incluyendo la definición de rutas y
#la lógica para manejar las solicitudes HTTP. El código que proporcionaste para la ruta de registro iría en este archivo.