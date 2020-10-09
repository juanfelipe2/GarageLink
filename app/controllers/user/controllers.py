from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from wtforms.validators import Optional

from . import user
from app import app, db, login_manager
from app.models.forms import UserLoginForm, UserRegisterForm
from app.models.tables import Usuario

@login_manager.user_loader
def get_user(login):
    return Usuario.query.filter_by(login=login).first()

@app.route('/cadastro-de-usuario', methods=['GET','POST'])
def register():
    #Guarda de rota, apena usuário autenticado e que for gerente pode registrar
    if current_user.is_authenticated and current_user.tipo.lower() == 'gerente':
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

            #Redireciona para lista de usuários
            return redirect(url_for('list'))

        return render_template('user_register.html', form=form)
    
    return redirect('pagina-inicial')


@app.route('/login', methods=['GET','POST'])
def login():
    if not current_user.is_authenticated:
        form = UserLoginForm()

        if form.validate_on_submit():
            login = form.login.data
            senha = form.senha.data
            usuario = Usuario.query.filter_by(login=login).first()

            if usuario and usuario.verify_password(senha):
                login_user(usuario)
                return redirect('pagina-inicial')

        return render_template('user_login.html', form=form)

    return redirect('pagina-inicial')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/lista-de-usuarios', methods=['GET'])
def list():
    if current_user.is_authenticated and current_user.tipo.lower() == 'gerente':
        users = Usuario.query.all()
        path = request.path
        return render_template('user_list.html', users=users)
    return redirect('pagina-inicial')

@app.route('/editar-usuario/<string:login>', methods=['GET','POST'])
def edit(login):
    if current_user.is_authenticated and current_user.tipo.lower() == 'gerente':
        form = UserRegisterForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            #Obtem usuário cadastrado no banco de dados
            usuario_banco = Usuario.query.filter_by(login=login).first()
            
            #Informações do formulário
            nome = form.nome.data
            email = form.email.data
            senha = form.senha.data
            tipo =  form.tipo.data.lower()

            #Monta objeto Usuario
            usuario_model = Usuario(login=login, senha=senha, nome=nome, email=email, tipo=tipo)

            #Altera informações para alteração no banco de dados
            usuario_banco.nome = usuario_model.nome
            usuario_banco.email = usuario_model.email
            usuario_banco.senha = usuario_model.senha
            usuario_banco.tipo = usuario_model.tipo

            #Grava no banco de dados
            db.session.add(usuario_banco)
            db.session.commit()

            return redirect(url_for('list'))
        else:
            usuario = Usuario.query.filter_by(login=login).first()
            if usuario:
                form.tipo.default = usuario.tipo.capitalize()
                form.process()
            return render_template('edit_user.html', form=form, usuario=usuario)
    
    return redirect('pagina-inicial')

@app.route('/excluir-usuario/<string:login>', methods=['GET','POST'])
def delete(login):
    if current_user.is_authenticated and current_user.tipo.lower() == 'gerente':
        usuario = Usuario.query.filter_by(login=login).first()
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('list'))
    redirect('pagina-inicial')