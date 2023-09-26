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

@reference.route("/", methods=["GET" , "POST"])
@login_required
def index() -> str:
    """
    Renderizado del template index

    Cuando se envía una petición POST hacia la ruta raiz ``/`` se buscan los datos sobre formulario
    del buscado y un listado de los últimos referencias en plazo de 30 díasen la base de datos y posteriormente
    se renderiza el template ``index.html``.

    Returns
    -------
    str
        Renderizado del template ``index.html`` mediante platillas Jinja2

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema

    """
    if request.method == "GET":
        form_reference = ReferenceForm()
        page = request.args.get('page', 1, type=int)
        references = models.Reference.query.filter( (models.Reference.fecha > datetime.now()) - timedelta(days=30) ).filter(models.Reference.user_id == current_user.id).order_by(models.Reference.fecha.desc()).paginate(page=page, per_page=15)
        month_ref = models.Reference.query.filter( (models.Reference.fecha > datetime.now()) - timedelta(days=30) ).filter(models.Reference.user_id == current_user.id).count()
        count_user_est = models.Reference.query.filter( (models.Reference.fecha > datetime.now()) - timedelta(days=30) ).filter(models.Reference.user_id == current_user.id).filter(models.Reference.user_type == "estudiantes").count()
        count_user_doc = models.Reference.query.filter( (models.Reference.fecha > datetime.now()) - timedelta(days=30) ).filter(models.Reference.user_id == current_user.id).filter(models.Reference.user_type == "docente-investigador").count()
        count_user_pub = models.Reference.query.filter( (models.Reference.fecha > datetime.now()) - timedelta(days=30) ).filter(models.Reference.user_id == current_user.id).filter(models.Reference.user_type == "general").count()
        
        context ={
            "form": form_reference, 
            "references": references, 
            "user": current_user,
            "month_ref": month_ref,
            "count_user_est": count_user_est,
            "count_user_doc": count_user_doc,
            "count_user_pub": count_user_pub,
            "month": calendar.month_name[ datetime.now().month]
        }
        return render_template("index.html" , **context)

@reference.route("/reference/", methods=["POST"])
@login_required
async def create_reference() -> Response:
    """
    Crear una referencia

    Cuando se envía una petición POST hacia la ruta ``/reference/`` se envían los datos necesarios para crear un objeto de tipo Reference en la base de datos.
    Y se envía un correo electrónico al email recuperado del formulario

    Returns
    -------
    Response
        Renderizado de la plantilla ``index.html`` con los datos obtenidos previamente

    Notes
    -----
    Para ejecutar esta ruta se requiere que el usuario se encuentra autenticado en el sistema
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
def update_reference(id):  
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
def delete_reference(id):
    if request.method == "GET":
        ref= models.Reference.query.get(id)
        db.session.delete(ref)
        db.session.commit()
        flash("Referencia eliminada")
        return redirect(url_for('reference.index'))
    
@reference.route("/search", methods=["GET" , "POST"])
@login_required
def search():
    query = request.form.get("query")
    if query:
        results = models.Reference.query.filter(models.Reference.user_id == current_user.id) \
            .filter(models.Reference.email.icontains(query) | models.Reference.details.icontains(query)) \
            .order_by(models.Reference.fecha.asc()).limit(100).all()
    else:
        results=[]
    return render_template("search_results.html", results=results)

