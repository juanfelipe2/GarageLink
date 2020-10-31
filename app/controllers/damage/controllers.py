from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional

from . import damage
from app import app, db, login_manager
from app.models.forms import DamageForm
from app.models.tables import Avaria, Veiculo

@app.route('/cadastro-de-avarias', methods=['GET', 'POST'])
def register_damage():
    if current_user.is_authenticated:
        form = DamageForm()

        if form.is_submitted():
            descricao_avaria = form.descricao_avaria.data
            observacao_avaria = form.observacao_avaria.data

            avaria = Avaria(
                descricao_avaria=descricao_avaria,
                observacao_avaria=observacao_avaria
                )

            # Grava no banco de dados
            db.session.add(avaria)
            db.session.commit()

            # Redireciona para lista de veiculos
            return redirect(url_for('damage_list'))

        # carrega combo box com a lista de funcionários
        # elif not form.id_cliente.data:
        #     form.id_cliente.choices = Veiculo.list_of_clients()
        #     form.process()

        return render_template('damage/damage_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-avarias', methods=['GET'])
def list_damage():
    if current_user.is_authenticated:
        avarias = Avaria.query.filter_by(excluido_avaria=False)
        return render_template('damage/damage_list.html', avarias=avarias)
    return redirect('pagina-inicial')


@app.route('/editar-avaria/<string:id_avaria>', methods=['GET', 'POST'])
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

            return redirect(url_for('damage_list'))

        elif not form.id_cliente.data:
            avaria = Avaria.query.filter_by(id_avaria=id_avaria).first()

            # form.id_cliente.choices = Veiculo.list_of_clients()
            # form.id_cliente.default = veiculo.cliente_id_cliente
            form.process()

            return render_template(
                'damage/damage_edit.html',
                form=form,
                avaria=avaria
                )

    return redirect('pagina-inicial')


@app.route('/excluir-avaria/<string:id_avaria>', methods=['GET', 'POST'])
def delete_damage(id_avaria):
    if current_user.is_authenticated:
        avaria = Avaria.query.filter_by(id_avaria=id_avaria).first()
        avaria.excluido_avaria = True
        db.session.add(avaria)
        db.session.commit()
        return redirect(url_for('damage_list'))
    redirect('pagina-inicial')
