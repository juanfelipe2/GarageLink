from . import index
from flask import redirect, url_for, render_template
from flask_login import current_user

@index.route("/")
@index.route("/index")
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))