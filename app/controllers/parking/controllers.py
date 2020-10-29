from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user
from wtforms.validators import Optional
import json

from . import parking
from app import db, login_manager, cross_origin
from app.models.forms import Parking, ServiceParking
from app.models.tables import Estacionamento, Veiculo, Cliente, Vaga, Servico, ServicoEstacionamento, UsuarioEstacionamento, and_

@parking.route('/registrar-entrada', methods=['GET', 'POST'])
def register_parking():
    if current_user.is_authenticated:
        form_parking = Parking()
        form_service = ServiceParking()

        if form_parking.is_submitted():
            placa_veiculo = form_parking.placa_veiculo.data
            id_vaga = form_parking.id_vaga.data
            entrada = form_parking.entrada.data
            saida = form_parking.saida.data
            observacao = form_parking.observacao.data
            valor_total = form_parking.valor_total.data
            situacao = 'pendente'
            servicos = json.loads(form_parking.servicos.data)

            print(servicos)

            parking = Estacionamento(
                placa_veiculo=placa_veiculo,
                id_vaga=id_vaga,
                entrada=entrada,
                saida=saida,
                observacao=observacao,
                valor_total=valor_total,
                situacao=situacao
                )

            # Grava no banco de dados
            db.session.add(parking)
            db.session.commit()
            db.session.refresh(parking)

            user = UsuarioEstacionamento(
                id_estacionamento=parking.id_estacionamento,
                login_usuario=current_user.login_usuario
                )

            db.session.add(user)
            db.session.commit()

            space = db.session\
                    .query(Vaga)\
                    .filter(
                        and_(
                                Vaga.id_vaga == int(id_vaga), 
                                Vaga.excluido_vaga == False,
                                Vaga.veiculo_placa_veiculo != None
                            )\
                        )\
                    .first()
            
            if space:
                space.veiculo_placa_veiculo = placa_veiculo
                space.situacao_vaga = 'ocupada'
                db.session.add(space)
                db.session.commit()
            

            for servico in servicos:
                service = ServicoEstacionamento(
                    id_estacionamento=parking.id_estacionamento,
                    id_servico=servico['id'],
                    nome=servico['nome'],
                    preco=servico['preco']
                )
                db.session.add(service)
                db.session.commit()


            # Redireciona para lista de registros estacionamento
            return redirect(url_for('parking.list_parking'))

        #carrega combo box com a lista de funcionários
        elif not form_parking.placa_veiculo.data:
            form_parking.placa_veiculo.choices = Veiculo.list_of_vehicles()
            form_parking.process()

        return render_template('parking/parking_register.html', form_parking=form_parking, form_service=form_service)

    return redirect('pagina-inicial')

@parking.route('/busca-servico/<string:id_servico>', methods=['GET'])
def search_service(id_servico):
    if id_servico and current_user.is_authenticated:
        service = db.session\
                    .query(Servico)\
                    .filter(
                        and_(
                                Servico.id_servico == int(id_servico), 
                                Servico.excluido_servico == False
                            )\
                        )\
                    .first()
        if service:
            return jsonify({'id': service.id_servico,'nome': service.nome_servico,'descricao': service.descricao_servico, 'preco': service.preco_servico, 'tipo': service.tipo_servico}), 200
    return jsonify([{'error': 'Código inválido.'}]), 403

@parking.route('/lista-registros-estacionamento', methods=['GET'])
def list_parking():
    if current_user.is_authenticated:
        parkings = Estacionamento.query.filter_by(excluido_estacionamento = False)
        return render_template('parking/parking_list.html', parkings=parkings)
    return redirect('pagina-inicial')


# @app.route('/editar-veiculo/<string:placa>', methods=['GET', 'POST'])
# def edit_vehicle(placa):
#     if current_user.is_authenticated:
#         form = VehicleForm()

#         print(form.validate_on_submit())
#         if form.is_submitted():
#             # Obtem cliente cadastrado no banco de dados
#             veiculo = Veiculo.query.filter_by(placa_veiculo=placa).first()

#             # Informações do formulário
#             placa = form.placa.data
#             marca = form.marca.data
#             modelo = form.modelo.data
#             cor = form.cor.data
#             anoFabricacao = form.anoFabricacao.data
#             anoModelo = form.anoModelo.data
#             id_cliente = form.id_cliente.data

#             # Altera informações para alteração no banco de dados
#             veiculo.placa_veiculo = placa
#             veiculo.marca_veiculo = marca
#             veiculo.modelo_veiculo = modelo
#             veiculo.cor_veiculo = cor
#             veiculo.ano_fabricacao_veiculo = anoFabricacao
#             veiculo.ano_modelo_veiculo = anoModelo
#             veiculo.cliente_id_cliente = id_cliente

#             # Grava no banco de dados
#             db.session.add(veiculo)
#             db.session.commit()

#             return redirect(url_for('list_vehicle'))
        
#         #carrega combo box com a lista de funcionários
#         elif not form.id_cliente.data:
#             veiculo = Veiculo.query.filter_by(placa_veiculo=placa).first()
            
#             form.id_cliente.choices = Cliente.list_of_clients()
#             form.id_cliente.default = veiculo.cliente_id_cliente
#             form.process()

#             return render_template(
#                 'vehicles/vehicle_edit.html',
#                 form=form,
#                 veiculo=veiculo
#                 )

#     return redirect('pagina-inicial')


# @app.route('/excluir-veiculo/<string:placa>', methods=['GET', 'POST'])
# def delete_vehicle(placa):
#     if current_user.is_authenticated:
#         veiculo = Veiculo.query.filter_by(placa_veiculo=placa).first()
#         veiculo.excluido_veiculo = True
#         db.session.add(veiculo)
#         db.session.commit()
#         return redirect(url_for('list_vehicle'))
#     redirect('pagina-inicial')
