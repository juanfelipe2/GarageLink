from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional
from datetime import datetime

from . import functionary
from app import app, db, login_manager
from app.models.forms import FunctionaryForm
from app.models.tables import Funcionario, Usuario

@app.route('/cadastro-de-funcionario', methods=['GET', 'POST'])
def register_functionary():
    # Guarda de rota, apenas usuário autenticado
    if current_user.is_authenticated:
        form = FunctionaryForm()

        if form.is_submitted():
            # Obtem informações do formulário de registro
            cpf = form.cpf.data
            nome = form.nome.data
            telefone = form.telefone.data
            celular = form.celular.data
            endereco = form.endereco.data
            tipo = form.tipo.data.lower()

            # Cria objeto Funcionario
            functionary = Funcionario(
                cpf=cpf,
                nome=nome,
                telefone=telefone,
                celular=celular,
                endereco=endereco,
                tipo=tipo
                )

            # Grava no banco de dados
            db.session.add(functionary)
            db.session.commit()

            # Redireciona para lista de funcionarios
            return redirect(url_for('list_functionary'))

        return render_template('functionary/functionary_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-funcionarios', methods=['GET'])
def list_functionary():
    if current_user.is_authenticated:
        functionaries = Funcionario.query.filter_by(excluido_funcionario = False)
        return render_template('functionary/functionary_list.html', functionaries=functionaries)
    return redirect('pagina-inicial')


@app.route('/editar-funcionario/<string:id_funcionario>', methods=['GET', 'POST'])
def edit_functionary(id_funcionario):
    if current_user.is_authenticated:
        form = FunctionaryForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem funcionario cadastrado no banco de dados
            functionary = Funcionario.query.filter_by(id_funcionario=id_funcionario).first()

            # Informações do formulário
            nome = form.nome.data
            cpf = form.cpf.data
            telefone = form.telefone.data
            celular = form.celular.data
            tipo = form.tipo.data.lower()

            # Altera informações para alteração no banco de dados
            functionary.cpf_funcionario = cpf
            functionary.nome_funcionario = nome
            functionary.telefone_funcionario = telefone
            functionary.celular_funcionario = celular
            functionary.tipo_funcionario = tipo.lower()

            # Grava no banco de dados
            db.session.add(functionary)
            db.session.commit()

            return redirect(url_for('list_functionary'))
        else:
            functionary = Funcionario.query.filter_by(id_funcionario=id_funcionario).first()
            if functionary:
                form.tipo.default = functionary.tipo_funcionario.capitalize()
                form.process()
            return render_template(
                'functionary/functionary_edit.html',
                form=form,
                functionary=functionary
                )

    return redirect('pagina-inicial')


@app.route('/excluir-funcionario/<string:id_funcionario>', methods=['GET', 'POST'])
def delete_functionary(id_funcionario):
    if current_user.is_authenticated:
        functionary = Funcionario.query.filter_by(id_funcionario=id_funcionario).first()
        functionary.excluido_funcionario = True
        
        user = Usuario.query.filter_by(funcionario_id_funcionario=functionary.id_funcionario).first()
        if user:
            user.excluido_usuario = True
            db.session.add(user)
            db.session.commit()

        db.session.add(functionary)
        db.session.commit()
        
        return redirect(url_for('list_functionary'))
    return redirect('pagina-inicial')
