from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask_login import login_required, current_user

from . import stats
from .. import db
from .forms import StatsDateForm
from ..models.reference import ReferenceModel

from io import StringIO
import csv

@stats.route("/reference_stats", methods=["GET" , "POST"])
@login_required
def reference_stats():
    date_form = StatsDateForm()
    if request.method == "GET":
        return render_template("stats.html", form=date_form)
    
    if request.method == "POST":
        references = ReferenceModel.query.filter(ReferenceModel.user_id == current_user.id).filter(ReferenceModel.fecha >= date_form.start_date.data, ReferenceModel.fecha <= date_form.end_date.data)
        total_reference = references.count()
        total_estudiantes = references.filter(ReferenceModel.user_type == "estudiantes").count()
        total_docentes = references.filter(ReferenceModel.user_type == "docente-investigador").count()
        total_administrativos = references.filter(ReferenceModel.user_type == "administrativo").count()
        total_externos = references.filter(ReferenceModel.user_type == "general").count()
        exportar = (date_form.start_date.data, date_form.end_date.data)

        #Datos para crear los gráficos
        data_plot_chart = {
            "data" : [references.filter(ReferenceModel.modality == "presencial").count(), references.filter(ReferenceModel.modality == "virtual").count()],
            "labels" : ["Presencial", "Virtual"],
        }

        #Grafico de lineas por días
        data_date_query = db.session.query(ReferenceModel.fecha, db.func.count(ReferenceModel.fecha)).filter(ReferenceModel.user_id == current_user.id).filter(ReferenceModel.fecha >= date_form.start_date.data, ReferenceModel.fecha <= date_form.end_date.data).order_by(ReferenceModel.fecha.asc()).group_by(ReferenceModel.fecha).all()
        data_line_chart = { label.strftime("%d/%m/%Y") : data for (label, data) in data_date_query }

        context = {
            "form": date_form,
            "estudiantes": total_estudiantes,
            "docentes": total_docentes,
            "externos": total_externos,
            "administrativos": total_administrativos,
            "exportar": exportar,
            "graph_modalidad": data_plot_chart,
            "data_line_chart" : data_line_chart,
            "total_reference": total_reference,
        }
        return render_template("stats.html", **context)
    
@stats.route("/reference_stats/report/<string:start>/<string:end>", methods=["GET" , "POST"])
@login_required
def export_report(start,end):
    references = ReferenceModel.query.filter(ReferenceModel.user_id == current_user.id).filter(ReferenceModel.fecha >= start, ReferenceModel.fecha <= end).order_by(ReferenceModel.fecha.desc()).all()
    
    #Crear el archivo para crear el informe csv
    output = StringIO()
    csv_writer = csv.writer(output)

    #Crear el encabezado
    header = ['ID; Fecha; Actividad; Detalles; Email del usuario; Modalidad; Tipo de Usuario']
    csv_writer.writerow(header)
    
    try: 
        for ref in references:
            line = [f"{str(ref.id)}; {str(ref.fecha)}; {ref.name.replace(';',' ')}; {ref.details.replace(';',' ')}; {ref.email}; {ref.modality}; {ref.user_type}"]
            csv_writer.writerow(line)

        output.seek(0)
        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=reference_report.csv"})
    except:
        flash("No se pudo crear el archivo CSV")
    
    return redirect(url_for('stats.reference_stats'))