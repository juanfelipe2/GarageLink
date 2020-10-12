from flask import Blueprint

vehicle = Blueprint("vehicle", __name__)

from . import controllers