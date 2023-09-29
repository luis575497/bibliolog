from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from flask_mailing import Message
from werkzeug.wrappers import Response

from datetime import datetime, timedelta
import calendar

from ..extensions import db, mail
from ..models import models
from ..forms.referenceform import ReferenceForm

reference = Blueprint("reference", __name__)

@reference.route("/reference/", methods=["POST"])
@login_required
async def create_reference() -> Response:
    """
    Crear una referencia
    Cuando se envía una petición POST hacia la ruta ``/reference/`` se envían los datos necesarios para crear un objeto de tipo Reference en la base de datos.
    Y se envía un correo electrónico al email recuperado del formulario
    """
    form_reference = ReferenceForm()

    if request.method == "POST" and form_reference.validate():
        bibliotecario = current_user.id
        new_reference =  models.Reference(
            name = form_reference.activity.data,
            details = form_reference.details.data,
            fecha = form_reference.date.data,
            user_type = form_reference.user_type.data,
            email = form_reference.email.data,
            modality = form_reference.modality.data,
            user_id= bibliotecario,
            )
        
        # Enviar mensaje al usuario sobre la referencia realizada
        msg = Message(
              subject="Evaluación de Atención en la Biblioteca Ucuenca",
              sender="biblioteca@ucuenca.edu.ec",
              recipients=[form_reference.email.data],
              body =f""" <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h1>Evalúa nuestra atención en la Biblioteca de la Universidad de Cuenca</h1>
                        <p>Estimado/a usuario/a,</p>
                        <p>Fuiste atendido/a por: <strong>{current_user.name}</strong></p>
                        <p>Recibiste la siguiente referencia: <em> {form_reference.details.data} </em></p>
                        <p>Queremos conocer tu opinión sobre la atención que recibiste en nuestra biblioteca. Por favor, tómate un momento para completar la evaluación haciendo clic en el enlace a continuación:</p>
                        <a href="https://forms.gle/XbNLiYKX3sWdWfYF6" style="display: inline-block; padding: 12px 20px; background-color: #3498db; color: #fff; text-decoration: none; border-radius: 5px;">Evaluar la atención</a>
                        <p>Tu opinión es importante para nosotros y nos ayudará a mejorar nuestros servicios. ¡Gracias por tu colaboración!</p>
                        <p>Atentamente,</p>
                        <p>Equipo de la Biblioteca de la Universidad de Cuenca</p>
                    """,
                subtype="html")
        
        await mail.send_message(msg)
        db.session.add(new_reference)
        db.session.commit()
        flash("Referencia creada correctamente, enviado correo electrónico al usuario")
        return redirect(url_for('reference.index'))

    return redirect(url_for('reference.index'))

@reference.route("/reference/<id>/update", methods=["GET" , "POST"])
@login_required
def update_reference(id: int) -> Response:
    """
    Actualizar una referencia
    Cuando se envía una petición GET hacia la ruta ``/reference/<id>/update`` se obtienen los datos necesarios para renderizar el archivo ``reference_update.html`` con los datos de la re
    referencia enviados. Cuando se realiza un petición POST hacia esta ruta se obtienen los datos del formulario y se actualiza los datos de la referencia en la base de datos. 
    """  
    form_reference = ReferenceForm()
    
    if request.method == "GET":
        form_reference = ReferenceForm()
        reference = models.Reference.query.get(id)
        form_reference.modality.default = reference.modality
        form_reference.user_type.default = reference.user_type
        form_reference.activity.default = reference.name        
        form_reference.details.default = reference.details
        form_reference.process()
        return render_template("reference_update.html", form=form_reference, ref = reference)
    
    if request.method == "POST" and form_reference.validate_on_submit():        
        reference = models.Reference.query.get(id)

        #Actualizar los datos con el formulario
        reference.name = form_reference.activity.data
        reference.details = form_reference.details.data
        reference.fecha = form_reference.date.data
        reference.user_type = form_reference.user_type.data
        reference.email = form_reference.email.data
        reference.modality = form_reference.modality.data
        db.session.commit()

        flash("Referencia actualizada correctamente")

        return redirect(url_for('reference.index'))

    
@reference.route("/reference/<id>/delete", methods=["GET" , "POST"])
@login_required
def delete_reference(id: int) -> Response:
    """
    Eliminar una referencia
    Cuando se envía una petición GET hacia la ruta ``/reference/<id>/delete`` se elimina la referencia usando el identificador de este en la base de datos. 
    """  
    if request.method == "GET":
        ref= models.Reference.query.get(id)
        db.session.delete(ref)
        db.session.commit()
        flash("Referencia eliminada")
        return redirect(url_for('reference.index'))
    
@reference.route("/search", methods=["GET" , "POST"])
@login_required
def search() -> str:
    """
    Buscar referencias
    Cuando se envía una petición GET hacia la ruta ``/search`` se buscan en la base de datos todos las referencias que coincidan
    con la consulta en los campos de email y details de las referencias en la base de datos. 
    """ 
    query = request.form.get("query")
    if query:
        results = models.Reference.query.filter(models.Reference.user_id == current_user.id) \
            .filter(models.Reference.email.icontains(query) | models.Reference.details.icontains(query)) \
            .order_by(models.Reference.fecha.asc()).limit(100).all()
    else:
        results=[]
    return render_template("search_results.html", results=results)

