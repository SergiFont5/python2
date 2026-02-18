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
'''
import logging
import jinja2
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined # para forzar errores en valores undefined en el html

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

@app.route("/registro", methods=["GET", "POST"])
def getRegistro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        password = request.form["password"]
        email = request.form["email"]
        print(f"{nombre} - {apellido} - {email} - {password}")
        return redirect(url_for("iniciarApp"))
    
    return render_template(
        "registro.html", 
        titulo_pagina="Registro"
        )

@app.errorhandler(404)
def paginaError(e):
    return render_template(
        "not_found.html"
    ), 404

## __name__ obtiene el valor "__main__" por defecto 
if __name__ == "__main__":
    app.run(debug=True)
