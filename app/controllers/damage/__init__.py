from flask import Blueprint

damage = Blueprint("damage", __name__)

from . import controllers