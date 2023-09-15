from flask import Blueprint, render_template, redirect, url_for, request

from .extensions import db
from . import models
from .forms import Reference

reference = Blueprint("reference", __name__)

@reference.route("/", methods=["GET" , "POST"])
def index():
    if request.method == "GET":
        form_reference = Reference()
        references = models.Reference.query.all()
        
        return render_template("index.html" , form = form_reference, references = references)

@reference.route("/reference/", methods=["GET" , "POST"])
def create_reference():
    form_reference = Reference()
    if request.method == "POST":
        new_reference =  models.Reference(
            name = form_reference.activity.data,
            details = form_reference.details.data,
            fecha = form_reference.date.data,
            user_type = form_reference.user_type.data,
            email = form_reference.email.data,
            modality = form_reference.modality.data
        )

        db.session.add(new_reference)
        db.session.commit()
        return redirect(url_for('reference.index'))

    return redirect(url_for('reference.index'))

@reference.route("/reference_update/<id>", methods=["GET" , "POST"])
def update_reference(id):  

    if request.method == "GET":
        form_reference = Reference()
        reference = models.Reference.query.get(id)
        return render_template("reference_update.html", form=form_reference, ref = reference)
    
    if request.method == "POST":
        form_reference = Reference()
        reference = models.Reference.query.get(id)
        
        #Actualizar los datos con el formulario
        reference.name = form_reference.activity.data
        reference.details = form_reference.details.data
        reference.fecha = form_reference.date.data
        reference.user_type = form_reference.user_type.data
        reference.email = form_reference.email.data
        reference.modality = form_reference.modality.data
        
        db.session.commit()
        return redirect(url_for('reference.index'))
    
@reference.route("/reference_delete/<id>", methods=["GET" , "POST"])
def delete_reference(id):
    if request.method == "GET":
        ref= models.Reference.query.get(id)
        db.session.delete(ref)
        db.session.commit()

        return redirect(url_for('reference.index'))