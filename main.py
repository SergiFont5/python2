# 
'''
Instalación de dependencias utilizando el entorno virtual venv.
El entorno formará parte del proyecto.

Creación del entorno virtual:
    python -m venv venv

Comando para elegir un interprete:
    Ctrl + shift + p 

Para utilizarlo/activarlo:
    venv\Scripts\activate
Para desactivar:
    deactivate

Añadir flask como dependencia con el entorno activo:
    pip install flask

Archivo de configuración de dependencias:
    pip freeze > requirements.txt
Realizar todo el rato que se añadan dependencias nuevas


Descargar dependencias del proyecto a partir de requirements.txt:
Primero hay que crear el entorno virtual. Luego:
    pip install -r requirements.txt

Base de dades utilitzada:
PostgreSQL (postgres)
Dependència per utilitzar-la des de Python: psycopg2-binary
Dependència per utilitzar posgres amb funcions des de Flask: flask_sqlalchemy
'''

from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import hashlib, binascii, os, jinja2, logging

from werkzeug.utils import *
from strings_configuracion import StringsConfiguracion
from extensions import db

from models.usuario import Usuario

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined # para forzar errores en valores undefined en el html

# BD =========================
app.config.from_object(StringsConfiguracion)
db.init_app(app)
# ============================

# SESSIONS =====================
login_manager = LoginManager(app)
# En un navegador, podem escriure qualsevol url manualment (barra de dalt).
# Pot ser que hi hagi rutes protegides (ex.: només per usuaris amb la sessió iniciada).
# Si escrivissin una d'aquestes rutes sense la sessió iniciada, redirigim a la pàgina de login.

login_manager.login_view = "getRegistro" # nos lleva a esta ruta cuando se inicia la sesion.

@login_manager.user_loader
def cargar_usuario(id_usuario):
    print("Sesion iniciado con usuario " + id_usuario)

    return db.session.get(Usuario, int(id_usuario))
# ==============================

datos_posts = [
    {
        "autor": "Nombre1",
        "titulo": "Título del post 1",
        "contenido": "Contenido del post 1",
        "data_post": "11 de febrero de 2026 - 16:49"
    },
    {
        "autor": "Nombre2",
        "titulo": "Título del post 2",
        "contenido": "Contenido del post 2",
        "data_post": "11 de febrero de 2026 - 16:50"
    }
]

# Rutes: 127.0.0.1:5000/inici
@app.route("/")
@app.route("/home")
def iniciarApp():
    return render_template(
        "home.html", 
        titulo_pagina="Página inicial", 
        primer_parrafo="Hola buenos días",
        datos=datos_posts
        )

@app.route("/info")
def darInfo():
    return "info"

@app.route("/contacto")
def getContactos():
    return render_template(
        "contactos.html",
        titulo_pagina="Página contacto"
        )

def get_hash_password(password_str: str) -> str:

    # Hay una manera de encontrar passwords de usuarios con las rainbow tables
    # Rainbow tables: consiste en generar muchas passwords, y para cada una aplicarle
    # las diferentes funciones de hash que hay. Cada resultado de estos hash, se guardan
    # en una tabla (Rainbow table). Los passwords suelen ser comunes estadísticamente.
    # Si alguien externo obtiene acceso a la base de datos donde se guardan los hash de los passwords,
    # puede comprobar con la Rainbow table si el hash se encuentra en la BD, obteniendo contraseñas
    # de esta manera.
    # La estructura de dichas tablas hace su búsqueda muy rápida y eficiente.

    salt = os.urandom(16) # forma un salt de 16 bytes.
    # se hace un hash concatenando los bytes con el password
    hash_en_bytes = hashlib.sha256(salt + password_str.encode("utf-8")).digest()
    salt_y_hash_en_bytes = salt + hash_en_bytes # se concatena
    salt_y_hash_en_str = binascii.hexlify(salt_y_hash_en_bytes).decode("utf-8") #se pasan a string
    print(salt_y_hash_en_str)
    return salt_y_hash_en_str

# verificar password
def verificar_password(hash_db_str:str, password_a_comprovar:str) -> bool:
    hash_bd_bytes = binascii.unhexlify(hash_db_str.encode("utf-8"))
    salt_bd = hash_bd_bytes[:16]
    hash_bd = hash_bd_bytes[16:]

    # Apliquem el salt al password que ha escrit l'usuari (pel login).
    salt_password_a_comprovar = salt_bd + password_a_comprovar.encode("utf-8")
    hash_password_a_comprovar = hashlib.sha256(salt_password_a_comprovar).digest()

    return hash_bd == hash_password_a_comprovar

@app.route("/registro", methods=["GET", "POST"])
def getRegistro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        password = request.form["password"]
        email = request.form["email"]
        print(f"{nombre} - {apellido} - {email} - {password}")

        hash_password = get_hash_password(password)

        # guardar usuario en base de datos.
        email_existente = Usuario.query.filter_by(email=email).first()
        print(email)
        if email_existente:
            print("Error: este mail ya está en uso.")
            return render_template("registro.html", titulo_pagina="Registro")
        
        usuario_existente = Usuario.query.filter_by(nombre_usuario=nombre).first()
        if usuario_existente:
            print("Error: el nombre de usuario ya está en uso")
            return render_template("registro.html", titulo_pagina="Registro")
        
        # si el usuario no existe
        usuario = Usuario(
            nombre_usuario=nombre,
            email=email,
            hash_password=password
        )
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for("iniciarApp"))
    
    return render_template(
        "registro.html", 
        titulo_pagina="Registro"
        )

## login
@app.route("/login", methods=["GET", "POST"])
def pagina_login():

    if request.method == "POST":
        email_rebut = request.form["email"]
        password_rebut = request.form["password"]

        print(email_rebut)

        usuari = Usuario.query.filter_by(email=email_rebut).first()

        if usuari and verificar_password(usuari.hash_password, password_rebut):

        # Fem login.
            login_user(usuari)
            return redirect(url_for("iniciarApp"))

    else:
        return render_template("login.html", titol_pagina="Login")

@app.route("/gestion_usuarios")
@login_required
def gestion_usuarios():
    usuarios_bd = Usuario.query.all()
    return render_template("gestion_usuarios.html", titulo_pagina="Gestion usuarios", usuarios=usuarios_bd)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("iniciarApp"))

@app.errorhandler(404)
def paginaError(e):
    return render_template(
        "not_found.html", titulo_pagina="error"
    ), 404

## __name__ obtiene el valor "__main__" por defecto 
if __name__ == "__main__":
    # DB =========================
    with app.app_context():
        # Crear las tablas de la BD si no existen.
        db.create_all()
    # ============================
    app.run(debug=True)
