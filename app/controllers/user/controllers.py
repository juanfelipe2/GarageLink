from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from wtforms.validators import Optional

from . import user
from app import app, db, login_manager
from app.models.forms import UserLoginForm, UserForm
from app.models.tables import Usuario, Funcionario

@login_manager.user_loader
def get_user(login):
    return Usuario.query.filter_by(login_usuario=login).first()

@app.route('/cadastro-de-usuario', methods=['GET','POST'])
def register():
    #Guarda de rota, apenas usuário autenticado e que for gerente pode registrar
    if current_user.is_authenticated and current_user.is_manager():
        form = UserForm()
        
        if form.is_submitted():
            #Obtem informações do formulário de registro
            nome = form.nome.data
            email = form.email.data.lower()
            login = form.login.data.lower()
            senha = form.senha.data
            tipo =  form.tipo.data.lower()
            situacao =  form.situacao.data.lower()
            id_funcionario = form.id_funcionario.data

            #Cria objeto Usuario
            usuario = Usuario(login=login, senha=senha, nome=nome, email=email, tipo=tipo, situacao=situacao, id_funcionario=id_funcionario)

            #Grava no banco de dados
            db.session.add(usuario)
            db.session.commit()

            #Redireciona para lista de usuários
            return redirect(url_for('list'))
        
        #carrega combo box com a lista de funcionários
        elif not form.id_funcionario.data:
            form.id_funcionario.choices = Funcionario.list_of_functionaries()
            form.process()

        return render_template('user_register.html', form=form)
    
    return redirect('pagina-inicial')


@app.route('/login', methods=['GET','POST'])
def login():
    if not current_user.is_authenticated:
        form = UserLoginForm()

        if form.validate_on_submit():
            login = form.login.data.lower()
            senha = form.senha.data
            usuario = Usuario.query.filter_by(login_usuario=login).first()

            if not usuario.is_deleted() and usuario.is_active() and usuario and usuario.verify_password(senha):
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
    if current_user.is_authenticated and current_user.is_manager():
        users = Usuario.query.filter_by(excluido_usuario=False)
        path = request.path
        return render_template('user_list.html', users=users)

    return redirect('pagina-inicial')

@app.route('/editar-usuario/<string:login>', methods=['GET','POST'])
def edit(login):
    if current_user.is_authenticated and current_user.is_manager():
        form = UserForm()

        if form.is_submitted():
            #Obtem usuário cadastrado no banco de dados
            usuario = Usuario.query.filter_by(login_usuario=login).first()
            
            #Informações do formulário
            nome = form.nome.data
            email = form.email.data.lower()
            senha = form.senha.data
            tipo =  form.tipo.data.lower()
            situacao =  form.situacao.data.lower()

            #Altera informações para alteração no banco de dados
            usuario.nome_usuario = nome
            usuario.email_usuario = email
            if senha:
                usuario.set_password(senha)
            usuario.tipo_usuario = tipo
            usuario.situacao_usuario = situacao

            #Grava no banco de dados
            db.session.add(usuario)
            db.session.commit()

            return redirect(url_for('list'))
        else:
            usuario = Usuario.query.filter_by(login_usuario=login).first()

            if usuario: 
                #carrega campos de seleção
                funcionario = Funcionario.query.filter_by(id_funcionario=usuario.funcionario_id_funcionario).first()
                form.id_funcionario.choices = [(funcionario.id_funcionario, funcionario.nome_funcionario)]
                form.tipo.default = usuario.tipo_usuario.capitalize()
                form.situacao.default = usuario.situacao_usuario.capitalize()
                form.process()
            return render_template('edit_user.html', form=form, usuario=usuario)
    
    return redirect('pagina-inicial')

@app.route('/excluir-usuario/<string:login>', methods=['GET','POST'])
def delete(login):
    if current_user.is_authenticated and current_user.is_manager():
        usuario = Usuario.query.filter_by(login_usuario=login).first()
        usuario.excluido_usuario = True
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('list'))

    return redirect('pagina-inicial')