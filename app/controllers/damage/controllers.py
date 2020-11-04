from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional

from . import damage
from app import app, db, login_manager
from app.models.forms import DamageForm
from app.models.tables import Avaria, Veiculo

@damage.route('/cadastro-de-avarias', methods=['GET', 'POST'])
def register_damage():
    if current_user.is_authenticated:
        form = DamageForm()

        if form.is_submitted():
            descricao_avaria = form.descricao_avaria.data
            observacao_avaria = form.observacao_avaria.data
            placa_veiculo = form.placa_veiculo.data

            avaria = Avaria(
                descricao=descricao_avaria,
                observacao=observacao_avaria,
                placa_veiculo=placa_veiculo
                )

            # Grava no banco de dados
            db.session.add(avaria)
            db.session.commit()

            # Redireciona para lista de veiculos
            return redirect(url_for('damage.list_damage'))

        # carrega combo box com a lista de veiculos
        elif not form.placa_veiculo.data:
            form.placa_veiculo.choices = Veiculo.list_of_vehicles()
            form.process()

        return render_template('damage/damage_register.html', form=form)

    return redirect('pagina-inicial')


@damage.route('/lista-de-avarias', methods=['GET'])
def list_damage():
    if current_user.is_authenticated:
        avarias = Avaria.query.filter_by(excluido_avaria=False)
        return render_template('damage/damage_list.html', avarias=avarias)
    return redirect('pagina-inicial')


@damage.route('/editar-avaria/<string:id_avaria>', methods=['GET', 'POST'])
def edit_damage(id_avaria):
    if current_user.is_authenticated:
        form = DamageForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            avaria = Avaria.query.filter_by(id_avaria=id_avaria).first()

            # Informações do formulário
            descricao_avaria = form.descricao_avaria.data
            observacao_avaria = form.observacao_avaria.data

            # Altera informações para alteração no banco de dados
            avaria.descricao_avaria = descricao_avaria
            avaria.observacao_avaria = observacao_avaria

            # Grava no banco de dados
            db.session.add(avaria)
            db.session.commit()

            return redirect(url_for('damage.list_damage'))

        elif not form.id_avaria.data:
            avaria = Avaria.query.filter_by(id_avaria=id_avaria).first()

            if avaria:
                form.placa_veiculo.choices = Veiculo.list_of_vehicles()
                form.placa_veiculo.default = avaria.placa_veiculo_placa
                form.process()

            return render_template(
                'damage/damage_edit.html',
                form=form,
                avaria=avaria
                )

    return redirect('pagina-inicial')


@damage.route('/excluir-avaria/<string:id_avaria>', methods=['GET', 'POST'])
def delete_damage(id_avaria):
    if current_user.is_authenticated:
        avaria = Avaria.query.filter_by(id_avaria=id_avaria).first()
        avaria.excluido_avaria = True
        db.session.add(avaria)
        db.session.commit()
        return redirect(url_for('damage.list_damage'))
    redirect('pagina-inicial')
