from flask import Blueprint

functionary = Blueprint("functionary", __name__)

from . import controllers