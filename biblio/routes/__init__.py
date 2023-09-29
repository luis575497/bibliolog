from flask import render_template, request
from flask_login import current_user, login_required

from datetime import datetime, timedelta
import calendar

from ..extensions import db, mail
from ..models import models
from ..forms.referenceform import ReferenceForm
from .reference import reference

@reference.route("/", methods=["GET" , "POST"])
@login_required
def index() -> str:
    """
    Renderizado del template index
    Cuando se envía una petición POST hacia la ruta raiz ``/`` se buscan los datos sobre formulario
    del buscado y un listado de los últimos referencias en plazo de 30 díasen la base de datos y posteriormente
    se renderiza el template ``index.html``.

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