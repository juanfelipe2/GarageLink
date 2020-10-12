from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from wtforms.validators import Optional

from . import vehicle
from app import app, db, login_manager
from app.models.forms import VehicleRegisterForm
from app.models.tables import Veiculo

@app.route('/cadastro-de-veiculos', methods=['GET', 'POST'])
def register_vehicle():
    if current_user.is_authenticated:
        form = VehicleRegisterForm()

        if form.validate_on_submit():
            placa = form.placa.data
            modelo = form.modelo.data
            cor = form.cor.data
            anoFabricacao = form.anoFabricacao.data
            anoModelo = form.anoModelo.data
            id_cliente = form.id_cliente.data

            veiculo = Veiculo(
                placa=placa,
                modelo=modelo,
                cor=cor,
                anoFabricacao=anoFabricacao,
                anoModelo=anoModelo,
                id_cliente=id_cliente
                )

            # Grava no banco de dados
            db.session.add(veiculo)
            db.session.commit()

            # Redireciona para lista de veiculos
            return redirect(url_for('list_vehicle'))

        return render_template('vehicles/vehicle_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-veiculos', methods=['GET'])
def list_vehicle():
    if current_user.is_authenticated:
        veiculos = Veiculo.query.all()
        path = request.path
        return render_template('vehicles/vehicle_list.html', veiculos=veiculos)
    return redirect('pagina-inicial')


@app.route('/editar-veiculo/<string:placa>', methods=['GET', 'POST'])
def edit_vehicle(placa):
    if current_user.is_authenticated:
        form = VehicleRegisterForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            veiculo_banco = Veiculo.query.filter_by(placa=placa).first()

            # Informações do formulário
            placa = form.placa.data
            modelo = form.modelo.data
            cor = form.cor.data
            anoFabricacao = form.anoFabricacao.data
            anoModelo = form.anoModelo.data
            id_cliente = form.id_cliente.data

            # Monta objeto Veiculo
            veiculo_model = Veiculo(
                placa=placa,
                modelo=modelo,
                cor=cor,
                anoFabricacao=anoFabricacao,
                anoModelo=anoModelo,
                id_cliente=id_cliente
                )

            # Altera informações para alteração no banco de dados
            veiculo_banco.placa = veiculo_model.placa
            veiculo_banco.modelo = veiculo_model.modelo
            veiculo_banco.cor = veiculo_model.cor
            veiculo_banco.anoFabricacao = veiculo_model.anoFabricacao
            veiculo_banco.anoModelo = veiculo_model.anoModelo
            veiculo_banco.id_cliente = veiculo_model.id_cliente

            # Grava no banco de dados
            db.session.add(veiculo_banco)
            db.session.commit()

            return redirect(url_for('list_vehicle'))
        else:
            veiculo = Veiculo.query.filter_by(placa=placa).first()
            if veiculo:
                form.tipo.default = veiculo.tipo.capitalize()
                form.process()
            return render_template(
                'vehicles/vehicle_edit.html',
                form=form,
                veiculo=veiculo
                )

    return redirect('pagina-inicial')


@app.route('/excluir-veiculo/<string:placa>', methods=['GET', 'POST'])
def delete_vehicle(placa):
    if current_user.is_authenticated:
        veiculo = Veiculo.query.filter_by(placa=placa).first()
        db.session.delete(veiculo)
        db.session.commit()
        return redirect(url_for('list_vehicle'))
    redirect('pagina-inicial')
