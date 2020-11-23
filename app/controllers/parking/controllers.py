from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user
from wtforms.validators import Optional
import json

from . import parking
from app import db, login_manager
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
            valor_liquido = valor_total
            situacao = 'pendente'
            servicos = json.loads(form_parking.servicos.data)

            parking = Estacionamento(
                placa_veiculo=placa_veiculo,
                id_vaga=id_vaga,
                entrada=entrada,
                saida=saida,
                observacao=observacao,
                valor_liquido=valor_liquido,
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
            return redirect(url_for('parking.list_parking', tipo_listagem='entradas'))

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
                                Servico.situacao_servico == 'ativo',
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

@parking.route('/todos-servicos', methods=['GET'])
def all_services():
    # if current_user.is_authenticated:
    services = db.session\
                .query(Servico)\
                .filter(
                    and_(
                            Servico.situacao_servico == 'ativo',
                            Servico.excluido_servico == False
                        )\
                    )
    registry = [
        {
            'id': 0,
            'nome': ""
        }
    ]
    
    for service in services:
        registry.append(
            {
                'id': service.id_servico,
                'nome': service.nome_servico
            }
        )

    return jsonify(registry), 200
    # return jsonify([{'error': 'Código inválido.'}]), 403

@parking.route('/lista-registros-estacionamento/<string:tipo_listagem>', methods=['GET'])
def list_parking(tipo_listagem):
    if current_user.is_authenticated:
        if tipo_listagem == 'entradas':
            parkings = db.session.query(Estacionamento).filter(and_(Estacionamento.saida_estacionamento == None, Estacionamento.excluido_estacionamento == False))
        elif tipo_listagem == 'saidas':
            parkings = db.session.query(Estacionamento).filter(and_(Estacionamento.saida_estacionamento != None, Estacionamento.excluido_estacionamento == False))
        return render_template('parking/parking_list.html', parkings=parkings)
    return redirect('pagina-inicial')


@parking.route('/registro-estacionamento/<string:id_estacionamento>', methods=['GET', 'POST'])
def edit_parking(id_estacionamento):
    if current_user.is_authenticated:
        form_parking = Parking()

        if form_parking.is_submitted():
            placa_veiculo = form_parking.placa_veiculo.data
            id_vaga = form_parking.id_vaga.data
            observacao = form_parking.observacao.data
            valor_total = float(form_parking.valor_total.data)
            servicos = json.loads(form_parking.servicos.data)

            parking = Estacionamento.query.filter_by(id_estacionamento=id_estacionamento).first()
            id_vaga_origem = parking.vaga_id_vaga

            parking.veiculo_placa_veiculo = placa_veiculo
            parking.vaga_id_vaga = id_vaga
            parking.observacao_estacionamento = observacao
            parking.valor_liquido_estacionamento = valor_total
            parking.valor_total_estacionamento = valor_total

            # Grava no banco de dados
            db.session.add(parking)
            db.session.commit()

            space_origin = Vaga.query.filter_by(id_vaga=id_vaga).first()

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
            
            if space_origin:
                space_origin.veiculo_placa_veiculo = None
                space_origin.situacao_vaga = 'livre'
                db.session.add(space_origin)
                db.session.commit()

            for servico in servicos:
                service = db.session\
                            .query(ServicoEstacionamento)\
                            .filter(
                                and_(
                                    ServicoEstacionamento.estacionamento_id_estacionamento == id_estacionamento,
                                    ServicoEstacionamento.servico_id_servico == servico['id_origem'],
                                    ServicoEstacionamento.excluido_servico == False
                                )
                            ).first()
                print(service)
                if service:
                    service.servico_id_servico = servico['id']
                    service.nome_servico = servico['nome']
                    service.preco_servico = servico['preco']
                    service.excluido_servico = servico['excluido'] == 'true'
                else:
                    service = ServicoEstacionamento(
                        id_estacionamento=parking.id_estacionamento,
                        id_servico=servico['id'],
                        nome=servico['nome'],
                        preco=servico['preco']
                    )
                db.session.add(service)
                db.session.commit()

            # Redireciona para lista de registros estacionamento
            return redirect(url_for('parking.list_parking', tipo_listagem='entradas'))

        else:
            parking = Estacionamento.query.filter_by(id_estacionamento=id_estacionamento).first()
            services = db.session\
                        .query(
                            Servico.id_servico,
                            ServicoEstacionamento.nome_servico, 
                            Servico.descricao_servico,
                            ServicoEstacionamento.preco_servico,
                            Servico.tipo_servico
                        )\
                        .join(
                            Servico, 
                            ServicoEstacionamento.servico_id_servico == Servico.id_servico
                        )\
                        .filter(
                            ServicoEstacionamento.estacionamento_id_estacionamento == id_estacionamento,
                            ServicoEstacionamento.excluido_servico == False
                        )

            space = Vaga.query.filter_by(id_vaga=parking.vaga_id_vaga).first()

            if not form_parking.placa_veiculo.data:
                if parking.situacao_estacionamento == 'pendente':
                    list = Veiculo.list_of_vehicle_no_parked()
                    list.sort()
                else:
                    list = [parking.veiculo_placa_veiculo]
                form_parking.placa_veiculo.choices = list
                form_parking.placa_veiculo.default = parking.veiculo_placa_veiculo
                form_parking.process()
            
            if not form_parking.id_vaga.data:
                if parking.situacao_estacionamento == 'pendente':
                    list = Vaga.list_of_spaces()
                    list.append((space.id_vaga, space.codigo_vaga + ' - ' + space.localizacao_vaga))
                else:
                    list = [(space.id_vaga, space.codigo_vaga + ' - ' + space.localizacao_vaga)]
                form_parking.id_vaga.choices = list
                form_parking.id_vaga.default = parking.vaga_id_vaga
                form_parking.process()

            return render_template(
                    'parking/parking_edit.html',
                    form_parking=form_parking,
                    parking=parking,
                    services=services,
                    saida=False,
                    read_only=False
                )

    return redirect('pagina-inicial')


@parking.route('/registro-saida-estacionamento/<string:id_estacionamento>', methods=['GET', 'POST'])
def exit_parking(id_estacionamento):
    if current_user.is_authenticated:
        form_parking = Parking()

        if form_parking.is_submitted():
            observacao = form_parking.observacao.data
            tipo_pagamento = form_parking.tipo_pagamento.data
            desconto = float(form_parking.desconto.data)
            saida = form_parking.saida.data
            valor_recebido = float(form_parking.valor_recebido.data)
            valor_liquido = float(form_parking.valor_liquido.data)
            valor_total = float(form_parking.valor_total.data)
            servicos = json.loads(form_parking.servicos.data)

            parking = Estacionamento.query.filter_by(id_estacionamento=id_estacionamento).first()

            parking.observacao_estacionamento = observacao
            parking.tipo_pagamento_estacionamento = tipo_pagamento
            parking.saida_estacionamento = saida
            parking.desconto_estacionamento = desconto
            parking.valor_recebido_estacionamento = valor_recebido
            parking.valor_liquido_estacionamento = valor_liquido
            parking.valor_total_estacionamento = valor_total
            parking.situacao_estacionamento = 'pago'

            # Grava no banco de dados
            db.session.add(parking)
            db.session.commit()

            space = Vaga.query.filter_by(id_vaga=parking.vaga_id_vaga).first()

            if space:
                space.veiculo_placa_veiculo = None
                space.situacao_vaga = 'livre'
                db.session.add(space)
                db.session.commit()

            for servico in servicos:
                service = db.session\
                            .query(ServicoEstacionamento)\
                            .filter(
                                and_(
                                    ServicoEstacionamento.estacionamento_id_estacionamento == id_estacionamento,
                                    ServicoEstacionamento.servico_id_servico == servico['id_origem'],
                                    ServicoEstacionamento.excluido_servico == False
                                )
                            ).first()
                            
                if service:
                    service.servico_id_servico = servico['id']
                    service.nome_servico = servico['nome']
                    service.preco_servico = servico['preco']
                    service.excluido_servico = servico['excluido'] == 'true'
                else:
                    service = ServicoEstacionamento(
                        id_estacionamento=parking.id_estacionamento,
                        id_servico=servico['id'],
                        nome=servico['nome'],
                        preco=servico['preco']
                    )
                db.session.add(service)
                db.session.commit()

            # Redireciona para lista de registros estacionamento
            return redirect(url_for('parking.list_parking', tipo_listagem='entradas'))

        else:
            parking = Estacionamento.query.filter_by(id_estacionamento=id_estacionamento).first()
            services = db.session\
                        .query(
                            Servico.id_servico,
                            ServicoEstacionamento.nome_servico, 
                            Servico.descricao_servico,
                            ServicoEstacionamento.preco_servico,
                            Servico.tipo_servico
                        )\
                        .join(
                            Servico, 
                            ServicoEstacionamento.servico_id_servico == Servico.id_servico
                        )\
                        .filter(
                            ServicoEstacionamento.estacionamento_id_estacionamento == id_estacionamento,
                            ServicoEstacionamento.excluido_servico == False
                        )

            space = Vaga.query.filter_by(id_vaga=parking.vaga_id_vaga).first()

            if not form_parking.placa_veiculo.data:
                list = []
                list.append(parking.veiculo_placa_veiculo)
                form_parking.placa_veiculo.choices = list
                form_parking.placa_veiculo.default = parking.veiculo_placa_veiculo
                form_parking.process()
            
            if not form_parking.id_vaga.data:
                list = []
                list.append((space.id_vaga, space.codigo_vaga + ' - ' + space.localizacao_vaga))
                form_parking.id_vaga.choices = list
                form_parking.id_vaga.default = parking.vaga_id_vaga
                form_parking.process()

            return render_template(
                    'parking/parking_edit.html',
                    form_parking=form_parking,
                    parking=parking,
                    services=services,
                    saida=True,
                    read_only=True
                )

    return redirect('pagina-inicial')


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
        
        servicos = db.session.query(ServicoEstacionamento).filter(and_(ServicoEstacionamento.estacionamento_id_estacionamento == id_estacionamento, ServicoEstacionamento.excluido_servico == False))
        for servico in servicos:
            servico.excluido_servico = True
            db.session.add(servico)
            db.session.commit()

        usuarios = db.session.query(UsuarioEstacionamento).filter(and_(UsuarioEstacionamento.estacionamento_id_estacionamento == id_estacionamento, UsuarioEstacionamento.excluido_usuario == False))
        for usuario in usuarios:
            usuario.excluido_usuario = True
            db.session.add(usuario)
            db.session.commit()

        if parking.situacao_estacionamento.lower() == 'pago':
            return redirect(url_for('parking.list_parking', tipo_listagem='saidas'))
        else:
            return redirect(url_for('parking.list_parking', tipo_listagem='entradas'))
    redirect('pagina-inicial')
