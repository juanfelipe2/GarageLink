from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional
from datetime import datetime

from . import service
from app import app, db, login_manager
from app.models.forms import ServiceForm
from app.models.tables import Servico

@app.route('/cadastro-de-servico', methods=['GET', 'POST'])
def register_service():
    # Guarda de rota, apenas usuário autenticado
    if current_user.is_authenticated:
        form = ServiceForm()

        if form.is_submitted():
            # Obtem informações do formulário de registro
            nome = form.nome.data
            descricao = form.descricao.data
            preco = form.preco.data
            tipo = form.tipo.data.lower()
            situacao = form.situacao.data.lower()

            # Cria objeto Servico
            service = Servico(
                nome=nome,
                descricao=descricao,
                preco=preco,
                tipo=tipo,
                situacao=situacao
                )

            # Grava no banco de dados
            db.session.add(service)
            db.session.commit()

            # Redireciona para lista de serviços
            return redirect(url_for('list_service'))

        return render_template('service/service_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-servicos', methods=['GET'])
def list_service():
    if current_user.is_authenticated:
        services = Servico.query.filter_by(excluido_servico = False)
        return render_template('service/service_list.html', services=services)
    return redirect('pagina-inicial')


@app.route('/editar-servico/<string:id_servico>', methods=['GET', 'POST'])
def edit_service(id_servico):
    if current_user.is_authenticated:
        form = ServiceForm()

        if form.is_submitted():
            # Obtem serviço cadastrado no banco de dados
            service = Servico.query.filter_by(id_servico=id_servico).first()

            # Informações do formulário
            nome = form.nome.data
            descricao = form.descricao.data
            preco = form.preco.data
            tipo = form.tipo.data
            situacao = form.situacao.data

            # Altera informações para alteração no banco de dados
            service.nome_servico = nome
            service.descricao_servico = descricao
            service.preco_servico = preco
            service.tipo_servico = tipo.lower()
            service.situacao_servico = situacao.lower()

            # Grava no banco de dados
            db.session.add(service)
            db.session.commit()

            return redirect(url_for('list_service'))
        else:
            service = Servico.query.filter_by(id_servico=id_servico).first()
            if service:
                form.tipo.default = service.tipo_servico.capitalize()
                form.situacao.default = service.situacao_servico.capitalize()
                form.process()
            return render_template(
                'service/service_edit.html',
                form=form,
                service=service
                )

    return redirect('pagina-inicial')


@app.route('/excluir-servico/<string:id_servico>', methods=['GET', 'POST'])
def delete_service(id_servico):
    if current_user.is_authenticated:
        service = Servico.query.filter_by(id_servico=id_servico).first()
        service.excluido_servico = True
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('list_service'))
    return redirect('pagina-inicial')
