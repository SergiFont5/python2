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
'''

from flask import Flask, render_template

app = Flask(__name__)

# Rutes: 127.0.0.1:5000/inici
@app.route("/")
@app.route("/home")
def iniciarApp():
    return render_template("home.html")

@app.route("/info")
def darInfo():
    return "info"

@app.route("/contacto")
def getContactos():
    return render_template("contactos.html")

if __name__ == "__main__":
    app.run(debug=True)
