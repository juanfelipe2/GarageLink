from . import base
from flask import redirect, url_for, render_template, abort, request
from flask_login import current_user
from app import app, db
from app.models.tables import Usuario

@base.route("/alterar-senha", methods=['GET','POST'])
def change_password():
    if current_user.is_authenticated:
        pagina_atual = request.args.get('pagina_atual')

        if request.method == 'POST':
            usuario = Usuario.query.filter_by(login_usuario=current_user.login_usuario).first()
            senha = request.form['senha_atual']
            nova_senha = request.form['nova_senha']
            confirmar_senha = request.form['confirmar_senha']
            
            if usuario.verify_password(senha) and nova_senha == confirmar_senha:
                usuario.set_password(nova_senha)
                db.session.add(usuario)
                db.session.commit()
                return redirect(pagina_atual)

            return redirect(pagina_atual)

        return redirect('pagina-inicial')

    return redirect('login')
