from flask import Blueprint

reference = Blueprint("reference", __name__, template_folder='templates')

from .routes import *