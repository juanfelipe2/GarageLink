from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional

from . import vacancy
from app import app, db, login_manager
from app.models.forms import VacancyForm
from app.models.tables import Vaga, Veiculo

@app.route('/cadastro-de-vagas', methods=['GET', 'POST'])
def register_vacancy():
    if current_user.is_authenticated:
        form = VacancyForm()

        if form.is_submitted():
            localizacao_vaga = form.localizacao_vaga.data
            codigo_vaga = form.codigo_vaga.data
            situacao_vaga = form.situacao_vaga.data

            vaga = Vaga(
                localizacao_vaga=localizacao_vaga,
                codigo_vaga=codigo_vaga,
                situacao_vaga=situacao_vaga
                )

            # Grava no banco de dados
            db.session.add(vaga)
            db.session.commit()

            # Redireciona para lista de veiculos
            return redirect(url_for('vacancy_list'))

        # carrega combo box com a lista de funcionários
        # elif not form.id_cliente.data:
        #     form.id_cliente.choices = Cliente.list_of_clients()
        #     form.process()

        return render_template('vacancy/vacancy_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-vagas', methods=['GET'])
def list_vacancy():
    if current_user.is_authenticated:
        vagas = Vaga.query.filter_by(excluido_vaga=False)
        return render_template('vacancy/vacancy_list.html', vagas=vagas)
    return redirect('pagina-inicial')


@app.route('/editar-vaga/<string:id_vaga>', methods=['GET', 'POST'])
def edit_vacancy(id_vaga):
    if current_user.is_authenticated:
        form = VacancyForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            vaga = Vaga.query.filter_by(id_vaga=id_vaga).first()

            # Informações do formulário
            localizacao_vaga = form.localizacao_vaga.data
            codigo_vaga = form.codigo_vaga.data
            situacao_vaga = form.situacao_vaga.data

            # Altera informações para alteração no banco de dados
            vaga.localizacao_vaga = localizacao_vaga
            vaga.codigo_vaga = codigo_vaga
            vaga.situacao_vaga = situacao_vaga

            # Grava no banco de dados
            db.session.add(vaga)
            db.session.commit()

            return redirect(url_for('vacancy_list'))

        elif not form.id_cliente.data:
            vaga = Vaga.query.filter_by(id_vaga=id_vaga).first()

            # form.id_cliente.choices = Cliente.list_of_clients()
            # form.id_cliente.default = veiculo.cliente_id_cliente
            form.process()

            return render_template(
                'vacancy/vacancy_edit.html',
                form=form,
                vaga=vaga
                )

    return redirect('pagina-inicial')


@app.route('/linkar-vaga/<string:id_vaga>', methods=['GET', 'POST'])
def link_vacancy(id_vaga):
    if current_user.is_authenticated:
        form = VacancyForm()

        print(form.validate_on_submit())

        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            vaga = Vaga.query.filter_by(id_vaga=id_vaga).first()

            # Informações do formulário
            codigo_vaga = form.codigo_vaga.data
            veiculo_placa_veiculo = form.veiculo_placa_veiculo.data

            # Altera informações para alteração no banco de dados
            vaga.codigo_vaga = codigo_vaga
            vaga.veiculo_placa_veiculo = veiculo_placa_veiculo

            # Grava no banco de dados
            db.session.add(vaga)
            db.session.commit()

            return redirect(url_for('vacancy_list'))
        elif not form.veiculo_placa_veiculo.data:
            vaga = Vaga.query.filter_by(id_vaga=id_vaga).first()

            form.veiculo_placa_veiculo.choices = Veiculo.list_of_vehicles()
            form.veiculo_placa_veiculo.default = vaga.veiculo_placa_veiculo
            form.process()

            return render_template(
                'vacancy/vacancy_link.html',
                form=form,
                vaga=vaga
                )

    return redirect('pagina-inicial')


@app.route('/excluir-vaga/<string:id_vaga>', methods=['GET', 'POST'])
def delete_vacancy(id_vaga):
    if current_user.is_authenticated:
        vaga = Vaga.query.filter_by(id_vaga=id_vaga).first()
        vaga.excluido_vaga = True
        db.session.add(vaga)
        db.session.commit()
        return redirect(url_for('vacancy_list'))
    redirect('pagina-inicial')
