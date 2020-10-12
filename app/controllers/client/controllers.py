from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional

from . import client
from app import app, db, login_manager
from app.models.forms import ClientRegisterForm
from app.models.tables import Cliente

@app.route('/cadastro-de-clientes', methods=['GET', 'POST'])
def register_client():
    # Guarda de rota, apena cliente autenticado
    if current_user.is_authenticated:
        form = ClientRegisterForm()

        if form.validate_on_submit():
            # Obtem informações do formulário de registro
            id_cliente = form.id_cliente.data
            cpf = form.cpf.data
            nome = form.nome.data
            dataNascimento = form.dataNascimento.data
            dataCadastro = form.dataCadastro.data
            celular = form.celular.data
            email = form.email.data
            situacao = form.situacao.data
            tipo = form.tipo.data.lower()

            # Cria objeto Cliente
            cliente = Cliente(
                id_cliente=id_cliente,
                cpf=cpf,
                nome=nome,
                dataNascimento=dataNascimento,
                dataCadastro=dataCadastro,
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
        clients = Cliente.query.all()
        path = request.path
        return render_template('clients/client_list.html', clients=clients)
    return redirect('pagina-inicial')


@app.route('/editar-cliente/<string:id_cliente>', methods=['GET', 'POST'])
def edit_client(id_cliente):
    if current_user.is_authenticated:
        form = ClientRegisterForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            cliente_banco = Cliente.query.filter_by(id_cliente=id_cliente).first()

            # Informações do formulário
            id_cliente = form.id_cliente.data
            cpf = form.cpf.data
            nome = form.nome.data
            dataNascimento = form.dataNascimento.data
            dataCadastro = form.dataCadastro.data
            celular = form.celular.data
            email = form.email.data
            situacao = form.situacao.data.lower()
            tipo = form.tipo.data.lower()

            # Monta objeto Cliente
            cliente_model = Cliente(
                id_cliente=id_cliente,
                cpf=cpf,
                nome=nome,
                dataNascimento=dataNascimento,
                dataCadastro=dataCadastro,
                celular=celular,
                email=email,
                situacao=situacao,
                tipo=tipo
                )

            # Altera informações para alteração no banco de dados
            cliente_banco.id_cliente = cliente_model.id_cliente
            cliente_banco.cpf = cliente_model.cpf
            cliente_banco.nome = cliente_model.nome
            cliente_banco.dataNascimento = cliente_model.dataNascimento
            cliente_banco.dataCadastro = cliente_model.dataCadastro
            cliente_banco.celular = cliente_model.celular
            cliente_banco.email = cliente_model.email
            cliente_banco.situacao = cliente_model.situacao
            cliente_banco.tipo = cliente_model.tipo

            # Grava no banco de dados
            db.session.add(cliente_banco)
            db.session.commit()

            return redirect(url_for('list_client'))
        else:
            cliente = Cliente.query.filter_by(id_cliente=id_cliente).first()
            if cliente:
                form.tipo.default = cliente.tipo.capitalize()
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
        db.session.delete(cliente)
        db.session.commit()
        return redirect(url_for('list_client'))
    redirect('pagina-inicial')
