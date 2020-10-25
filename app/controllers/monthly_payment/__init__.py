from flask import Blueprint

monthly_payment = Blueprint("monthly_payment", __name__)

from . import controllers