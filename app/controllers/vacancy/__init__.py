from flask import Blueprint

vacancy = Blueprint("vacancy", __name__)

from . import controllers