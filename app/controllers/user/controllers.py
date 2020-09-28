from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user

from . import user
from app import app, db, login_manager
from app.models.forms import UserLoginForm, UserRegisterForm
from app.models.tables import Usuario

@login_manager.user_loader
def get_user(login):
    return Usuario.query.filter_by(login=login).first()

@app.route('/register', methods=['GET','POST'])
def register():
    form = UserRegisterForm()

    if form.validate_on_submit():
        #Obtem informações do formulário de registro
        nome = form.nome.data
        email = form.email.data
        login = form.login.data
        senha = form.senha.data
        tipo =  form.tipo.data.lower()

        #Cria objeto Usuario
        usuario = Usuario(login=login, senha=senha, nome=nome, email=email, tipo=tipo)

        #Grava no banco de dados
        db.session.add(usuario)
        db.session.commit()

        return redirect('index')
    return render_template('register_login.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        login = form.login.data
        senha = form.senha.data
        usuario = Usuario.query.filter_by(login=login).first()

        if usuario and usuario.verify_password(senha):
            login_user(usuario)
            return redirect('index')
    return render_template('user_login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('login')


