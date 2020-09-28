#módulo para registrar blueprints

from app import app

from app.controllers.index import index as index_blueprint
app.register_blueprint(index_blueprint)

from app.controllers.user import user as user_blueprint
app.register_blueprint(user_blueprint)