# módulo para registrar blueprints

from flask import render_template
from app import app
from app.controllers.user import user as user_blueprint
from app.controllers.base import base as base_blueprint
from app.controllers.index import index as index_blueprint
from app.controllers.client import client as client_blueprint
from app.controllers.vehicle import vehicle as vehicle_blueprint
from app.controllers.vacancy import vacancy as vacancy_blueprint
from app.controllers.damage import damage as damage_blueprint
from app.controllers.service import service as service_blueprint
from app.controllers.functionary import functionary as functionary_blueprint
from app.controllers.monthly_payment import monthly_payment as monthly_payment_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(base_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(client_blueprint)
app.register_blueprint(vehicle_blueprint)
app.register_blueprint(vacancy_blueprint)
app.register_blueprint(damage_blueprint)
app.register_blueprint(service_blueprint)
app.register_blueprint(functionary_blueprint)
app.register_blueprint(monthly_payment_blueprint)

@app.errorhandler(404)
def resource_not_found(e):
    return render_template('not-found/not-found-page.html')
