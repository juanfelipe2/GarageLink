from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user
from wtforms.validators import Optional

from . import vehicle
from app import app, db, login_manager
from app.models.forms import VehicleForm
from app.models.tables import Veiculo, Cliente

@app.route('/cadastro-de-veiculos', methods=['GET', 'POST'])
def register_vehicle():
    if current_user.is_authenticated:
        form = VehicleForm()

        if form.is_submitted():
            placa = form.placa.data
            marca = form.marca.data
            modelo = form.modelo.data
            cor = form.cor.data
            anoFabricacao = form.anoFabricacao.data
            anoModelo = form.anoModelo.data
            id_cliente = form.id_cliente.data

            veiculo = Veiculo(
                placa=placa,
                marca=marca,
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

        #carrega combo box com a lista de funcionários
        elif not form.id_cliente.data:
            form.id_cliente.choices = Cliente.list_of_clients()
            form.process()

        return render_template('vehicles/vehicle_register.html', form=form)

    return redirect('pagina-inicial')


@app.route('/lista-de-veiculos', methods=['GET'])
def list_vehicle():
    if current_user.is_authenticated:
        veiculos = Veiculo.query.filter_by(excluido_veiculo = False)
        return render_template('vehicles/vehicle_list.html', veiculos=veiculos)
    return redirect('pagina-inicial')


@app.route('/editar-veiculo/<string:placa>', methods=['GET', 'POST'])
def edit_vehicle(placa):
    if current_user.is_authenticated:
        form = VehicleForm()

        print(form.validate_on_submit())
        if form.is_submitted():
            # Obtem cliente cadastrado no banco de dados
            veiculo = Veiculo.query.filter_by(placa_veiculo=placa).first()

            # Informações do formulário
            placa = form.placa.data
            marca = form.marca.data
            modelo = form.modelo.data
            cor = form.cor.data
            anoFabricacao = form.anoFabricacao.data
            anoModelo = form.anoModelo.data
            id_cliente = form.id_cliente.data

            # Altera informações para alteração no banco de dados
            veiculo.placa_veiculo = placa
            veiculo.marca_veiculo = marca
            veiculo.modelo_veiculo = modelo
            veiculo.cor_veiculo = cor
            veiculo.ano_fabricacao_veiculo = anoFabricacao
            veiculo.ano_modelo_veiculo = anoModelo
            veiculo.cliente_id_cliente = id_cliente

            # Grava no banco de dados
            db.session.add(veiculo)
            db.session.commit()

            return redirect(url_for('list_vehicle'))
        
        #carrega combo box com a lista de funcionários
        elif not form.id_cliente.data:
            veiculo = Veiculo.query.filter_by(placa_veiculo=placa).first()
            
            form.id_cliente.choices = Cliente.list_of_clients()
            form.id_cliente.default = veiculo.cliente_id_cliente
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
        veiculo = Veiculo.query.filter_by(placa_veiculo=placa).first()
        veiculo.excluido_veiculo = True
        db.session.add(veiculo)
        db.session.commit()
        return redirect(url_for('list_vehicle'))
    redirect('pagina-inicial')

@app.route('/busca-placa/<string:placa>', methods=['GET', 'POST'])
def search_plate(placa):
    vehicle = Veiculo.query.filter_by(placa_veiculo=placa.upper()).first()
    if vehicle:
        result = {}
        result['placa'] = vehicle.placa_veiculo
        return jsonify(result), 200
    else:
        result = {}
        result['error'] = 'Placa não encontrada.'
        result['code'] = 403
        return jsonify(result), 403