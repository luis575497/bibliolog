
from flask import render_template

def page_not_found(e):
    context = {
        "error": e,
        "titulo": "Oooooops! La página que intentas solicitar no está en el servidor",
        "mensaje":"Lo sentimos pero la página que busca no existe, ha sido eliminada, el nombre ha cambiado o no está disponible temporalmente",
        "number": "404"
    }
    return render_template("error.html", **context)
