from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional
from datetime import datetime

from . import client
from app import app, db, login_manager
from app.models.forms import ClientForm
from app.models.tables import Cliente

@app.route('/cadastro-de-clientes', methods=['GET', 'POST'])
def register_client():
    # Guarda de rota, apena cliente autenticado
    if current_user.is_authenticated:
        form = ClientForm()

        if form.is_submitted():
            # Obtem informações do formulário de registro
            cpf = form.cpf.data
            nome = form.nome.data
            dataNascimento = form.dataNascimento.data
            dataCadastro = datetime.today().strftime('%Y-%m-%d')
            telefone = form.telefone.data
            celular = form.celular.data
            email = form.email.data
            situacao = 'Em dia'
            tipo = 'Único'

            # Cria objeto Cliente
            cliente = Cliente(
                cpf=cpf,
                nome=nome,
                dataNascimento=dataNascimento,
                dataCadastro=dataCadastro,
                telefone=telefone,
                celular=celular,
                email=email,
                situacao=situacao,
                tipo=tipo
                )

            # Grava no banco de dados
            db.session.add(cliente)
            db.session.commit()

            # Redireciona para lista de clientes
            return redirect(url_for('list_client'))

        return render_template('clients/client_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-clientes', methods=['GET'])
def list_client():
    if current_user.is_authenticated:
        clients = Cliente.query.filter_by(excluido_cliente = False)
        return render_template('clients/client_list.html', clients=clients)
    return redirect('pagina-inicial')


@app.route('/editar-cliente/<string:id_cliente>', methods=['GET', 'POST'])
def edit_client(id_cliente):
    if current_user.is_authenticated:
        form = ClientForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            cliente = Cliente.query.filter_by(id_cliente=id_cliente).first()

            # Informações do formulário
            cpf = form.cpf.data
            nome = form.nome.data
            dataNascimento = form.dataNascimento.data
            telefone = form.telefone.data
            celular = form.celular.data
            email = form.email.data
            situacao = 'Em dia'
            tipo = 'Único'

            # Altera informações para alteração no banco de dados
            cliente.cpf_cliente = cpf
            cliente.nome_cliente = nome
            cliente.data_nascimento_cliente = dataNascimento
            cliente.telefone_cliente = telefone
            cliente.celular_cliente = celular
            cliente.email_cliente = email
            cliente.situacao_cliente = situacao.lower()
            cliente.tipo_cliente = tipo.lower()

            # Grava no banco de dados
            db.session.add(cliente)
            db.session.commit()

            return redirect(url_for('list_client'))
        else:
            cliente = Cliente.query.filter_by(id_cliente=id_cliente).first()
            if cliente:
                form.situacao.default = cliente.situacao_cliente.capitalize()
                form.tipo.default = cliente.tipo_cliente.capitalize()
                form.process()
            return render_template(
                'clients/client_edit.html',
                form=form,
                cliente=cliente
                )

    return redirect('pagina-inicial')


@app.route('/excluir-cliente/<string:id_cliente>', methods=['GET', 'POST'])
def delete_client(id_cliente):
    if current_user.is_authenticated:
        cliente = Cliente.query.filter_by(id_cliente=id_cliente).first()
        cliente.excluido_cliente = True
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('list_client'))
    return redirect('pagina-inicial')
