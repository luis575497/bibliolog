from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import logout_user, login_user, login_required

from . import login_manager, bcrypt, db
from .models import User, Campus
from .forms import LoginForm, ProfileForm


login = Blueprint("login", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login.login_biblio'))

@login.route("/login", methods=["GET" , "POST"])
def login_biblio():
    login_form = LoginForm()

    if request.method == "GET":
        return render_template("login.html", form = login_form)
    
    if request.method == "POST":
        user = User.query.filter_by(email=login_form.username.data).first() 
        if user: 
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                flash("Sesión iniciada correctamente")
                login_user(user)
                return redirect(url_for('reference.index'))
            else:
                flash("Contraseña incorrecta")
                return redirect(url_for('login.login_biblio'))
        else:
            flash("El correo proporcionado no existe en la base de datos")
            return redirect(url_for('login.login_biblio'))

@login.route("/register", methods=["GET" , "POST"])
def register():
    register_form = LoginForm()


    if request.method == "POST":
        if User.query.filter_by(email=register_form.username.data).first():
            flash("Ya está registrado el correo en la base de datos")
            return redirect(url_for('login.register'))
        else:
            campus = Campus.query.filter(Campus.name == register_form.campus.data).first()
            hashed_password = bcrypt.generate_password_hash(register_form.password.data)
            new_user = User(email=register_form.username.data, 
                            password=hashed_password,
                            name=register_form.name.data,
                            campus=campus)
            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login.login_biblio'))
    
    if request.method == "GET":
        return render_template("register.html", form = register_form)
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login.login_biblio'))

# Editar el perfil del usuario    
@login.route("/user/<id>", methods=["GET" , "POST"])
@login_required
def profile(id):
    profile_form = ProfileForm()

    if request.method == "GET":
        user = User.query.get(id)
        profile_form.name.default = user.name
        profile_form.username.default = user.email
        profile_form.campus.default = user.campus
        profile_form.process()

        return render_template("profile.html", form=profile_form, user=user)
    
    if request.method == "POST":
        user = User.query.get(id)
        user.email=profile_form.username.data
        user.name=profile_form.name.data
        campus = Campus.query.filter(Campus.name == profile_form.campus.data).first()
        user.campus = campus
        
        if profile_form.password.data != "":
            hashed_password = bcrypt.generate_password_hash(profile_form.password.data)
            user.password = hashed_password
            db.session.commit()
            logout_user()
            flash("Contraseña cambiada")

        db.session.commit()
        flash("Datos del perfil de usuario actualizado")
        return redirect(url_for('reference.index',))
