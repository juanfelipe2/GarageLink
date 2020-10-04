#módulo para registrar blueprints

from flask import render_template

from app import app

from app.controllers.index import index as index_blueprint
app.register_blueprint(index_blueprint)

from app.controllers.user import user as user_blueprint
app.register_blueprint(user_blueprint)

@app.errorhandler(404)
def resource_not_found(e):
    return render_template('not-found-page.html')