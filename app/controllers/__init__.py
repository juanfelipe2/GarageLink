# módulo para registrar blueprints

from flask import render_template
from app import app
from app.controllers.user import user as user_blueprint
from app.controllers.index import index as index_blueprint
from app.controllers.client import client as client_blueprint
from app.controllers.vehicle import vehicle as vehicle_blueprint

app.register_blueprint(index_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(client_blueprint)
app.register_blueprint(vehicle_blueprint)

@app.errorhandler(404)
def resource_not_found(e):
    return render_template('not-found-page.html')
