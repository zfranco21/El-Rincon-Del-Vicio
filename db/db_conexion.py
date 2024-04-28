from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Elrincondelvicio.'
app.config['MYSQL_DB'] = 'elrincondelvicio'

mysql = MySQL(app)


#Este archivo llamado db_conxion.py realiza la conexion con mi base de datos MySql y nos permite trabajar sobre las tablas y los datos que le inserté.