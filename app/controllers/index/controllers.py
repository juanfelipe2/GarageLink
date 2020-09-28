from . import index
from flask import redirect
from flask_login import current_user

@index.route("/")
@index.route("/index")
def index():
    if current_user.is_authenticated:
        return 'Bem-vindo!'
    else:
        return redirect('login')