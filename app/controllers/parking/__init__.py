from flask import Blueprint

parking = Blueprint("parking", __name__)

from . import controllers