from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user
from wtforms.validators import Optional
import json

from . import parking
from app import db, login_manager, cross_origin
from app.models.forms import Parking, ServiceParking
from app.models.tables import Estacionamento, Veiculo, Cliente, Vaga, Servico, ServicoEstacionamento, UsuarioEstacionamento, and_

@parking.route('/registrar-entrada-estacionamento', methods=['GET', 'POST'])
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
            valor_total = float(form_parking.valor_total.data)
            situacao = 'pendente'
            servicos = json.loads(form_parking.servicos.data)

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
                                Vaga.veiculo_placa_veiculo == None
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
        else:
            if not form_parking.placa_veiculo.data:
                form_parking.placa_veiculo.choices = Veiculo.list_of_vehicle_no_parked()
                form_parking.process()
            
            if not form_parking.id_vaga.data:
                form_parking.id_vaga.choices = Vaga.list_of_spaces()
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
            registry = {}
            registry['id'] = service.id_servico
            registry['nome'] = service.nome_servico
            registry['descricao'] = service.descricao_servico
            registry['preco'] = service.preco_servico
            registry['tipo'] = service.tipo_servico

            return jsonify(registry), 200
    return jsonify([{'error': 'Código inválido.'}]), 403

@parking.route('/lista-entradas-estacionamento', methods=['GET'])
def list_parking():
    if current_user.is_authenticated:
        parkings = db.session.query(Estacionamento).filter(and_(Estacionamento.saida_estacionamento == None, Estacionamento.excluido_estacionamento == False))
        return render_template('parking/parking_list.html', parkings=parkings)
    return redirect('pagina-inicial')


# @parking.route('/editar-registro-estacionamento/<string:id_estacionamento>', methods=['GET', 'POST'])
# def edit_parking(id_estacionamento):
#     if current_user.is_authenticated:
#         form_parking = Parking()
#         form_service = ServiceParking()

#         if form_parking.is_submitted():
#             placa_veiculo = form_parking.placa_veiculo.data
#             id_vaga = form_parking.id_vaga.data
#             entrada = form_parking.entrada.data
#             saida = form_parking.saida.data
#             observacao = form_parking.observacao.data
#             valor_total = form_parking.valor_total.data
#             servicos = json.loads(form_parking.servicos.data)

#             parking = Estacionamento.query.filter_by(id_estacionamento=id_estacionamento).first()

#             parking.veiculo_placa_veiculo
#             parking.vaga_id_vaga
#             parking.observacao_estacionamento
#             parking.valor_total_estacionamento
#             parking.situacao_estacionamento

#             parking = Estacionamento(
#                 placa_veiculo=placa_veiculo,
#                 id_vaga=id_vaga,
#                 entrada=entrada,
#                 saida=saida,
#                 observacao=observacao,
#                 valor_total=valor_total,
#                 situacao=situacao
#                 )

#             # Grava no banco de dados
#             db.session.add(parking)
#             db.session.commit()
#             db.session.refresh(parking)

#             user = UsuarioEstacionamento(
#                 id_estacionamento=parking.id_estacionamento,
#                 login_usuario=current_user.login_usuario
#                 )

#             db.session.add(user)
#             db.session.commit()

#             space = db.session\
#                     .query(Vaga)\
#                     .filter(
#                         and_(
#                                 Vaga.id_vaga == int(id_vaga), 
#                                 Vaga.excluido_vaga == False,
#                                 Vaga.veiculo_placa_veiculo != None
#                             )\
#                         )\
#                     .first()
            
#             if space:
#                 space.veiculo_placa_veiculo = placa_veiculo
#                 space.situacao_vaga = 'ocupada'
#                 db.session.add(space)
#                 db.session.commit()

#             for servico in servicos:
#                 service = ServicoEstacionamento(
#                     id_estacionamento=parking.id_estacionamento,
#                     id_servico=servico['id'],
#                     nome=servico['nome'],
#                     preco=servico['preco']
#                 )
#                 db.session.add(service)
#                 db.session.commit()

#             # Redireciona para lista de registros estacionamento
#             return redirect(url_for('parking.list_parking'))

#         #carrega combo box com a lista de funcionários
#         elif not form_parking.placa_veiculo.data:
#             form_parking.placa_veiculo.choices = Veiculo.list_of_vehicles()
#             form_parking.process()

#         return render_template('parking/parking_register.html', form_parking=form_parking, form_service=form_service)

#     return redirect('pagina-inicial')

@parking.route('/excluir-registro-estacionamento/<string:id_estacionamento>', methods=['GET', 'POST'])
def delete_vehicle(id_estacionamento):
    if current_user.is_authenticated:

        parking = Estacionamento.query.filter_by(id_estacionamento=id_estacionamento).first()
        if parking:
            parking.excluido_estacionamento = True
            db.session.add(parking)
            db.session.commit()

        space = Vaga.query.filter_by(id_vaga=parking.vaga_id_vaga).first()
        if space:
            space.veiculo_placa_veiculo = None
            space.situacao_vaga = 'livre'
            db.session.add(space)
            db.session.commit()
            
        servico = ServicoEstacionamento.query.filter_by(estacionamento_id_estacionamento=id_estacionamento).first()
        if servico:
            servico.excluido_servico = True
            db.session.add(servico)
            db.session.commit()

        usuario = UsuarioEstacionamento.query.filter_by(estacionamento_id_estacionamento=id_estacionamento).first()
        if usuario:
            usuario.excluido_usuario = True
            db.session.add(usuario)
            db.session.commit()

        return redirect(url_for('parking.list_parking'))
    redirect('pagina-inicial')
