from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from .models import Reference
from datetime import datetime, timedelta

stats = Blueprint("stats", __name__)

@stats.route("/reference_stats", methods=["GET" , "POST"])
@login_required
def reference_stats():
    references = Reference.query.filter( (Reference.fecha > datetime.now()) - timedelta(days=30) ).filter(Reference.user_id == current_user.id).order_by(Reference.fecha.desc()).all()
    return render_template("stats.html")
