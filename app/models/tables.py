from app import db
from flask_login import UserMixin
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

class Funcionario(db.Model):
    __tableName__ = "funcionario"

    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_funcionario = db.Column(db.String)
    cpf_funcionario = db.Column(db.String)
    telefone_funcionario = db.Column(db.String)
    celular_funcionario = db.Column(db.String)
    endereco_funcionario = db.Column(db.String)
    tipo_funcionario = db.Column(db.String)
    excluido_funcionario = db.Column(db.Boolean)

    def __init__(self, cpf, nome, telefone, celular, endereco, tipo):
        self.cpf_funcionario = cpf
        self.nome_funcionario = nome
        self.telefone_funcionario = telefone
        self.celular_funcionario = celular
        self.endereco_funcionario = endereco
        self.tipo_funcionario = tipo
        self.excluido_funcionario = False


    def list_of_functionaries():
        #filtra os funcionários que não possuem login cadastrado
        functionaries = db.session\
                          .query(
                                Funcionario.id_funcionario, 
                                Funcionario.nome_funcionario
                            )\
                            .outerjoin(
                                Usuario, 
                                and_(
                                    Usuario.funcionario_id_funcionario == Funcionario.id_funcionario, 
                                    Usuario.excluido_usuario == False
                                )
                            )\
                            .filter(
                                and_(
                                    Usuario.login_usuario == None, 
                                    Funcionario.excluido_funcionario == False
                                )
                            )
       
       #inicia lista com um valor em branco
        list = [(0, '')]

        for func in functionaries:
            list.append((func.id_funcionario, func.nome_funcionario))
        
        return list

    def is_deleted(self):
        return self.excluido_funcionario

class Usuario(db.Model, UserMixin):
    __tableName__ = "usuario"
    
    login_usuario = db.Column(db.String, primary_key=True)
    senha_usuario = db.Column(db.String)
    nome_usuario = db.Column(db.String)
    email_usuario = db.Column(db.String, unique=True)
    tipo_usuario = db.Column(db.String)
    situacao_usuario = db.Column(db.String)
    excluido_usuario = db.Column(db.Boolean)
    funcionario_id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id_funcionario'))
    
    def __init__(self, login, senha, nome, email, tipo, situacao, id_funcionario):
        self.login_usuario = login
        self.senha_usuario = generate_password_hash(senha)
        self.nome_usuario = nome
        self.email_usuario = email
        self.tipo_usuario = tipo
        self.situacao_usuario = situacao
        self.funcionario_id_funcionario = id_funcionario
        self.excluido_usuario = False

    def get_id(self):
        return self.login_usuario
    
    def set_password(self, pwd):
        self.senha_usuario =  generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.senha_usuario, pwd)
    
    def is_deleted(self):
        return self.excluido_usuario

    def is_manager(self):
        return self.tipo_usuario.lower() == 'gerente'
    
    def is_active(self):
        return self.situacao_usuario.lower() == 'ativo'
        return check_password_hash(self.senha, pwd)


class Cliente(db.Model):
    __tableName__ = "cliente"

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf_cliente = db.Column(db.String)
    nome_cliente = db.Column(db.String)
    data_nascimento_cliente = db.Column(db.String)
    data_cadastro_cliente = db.Column(db.String)
    telefone_cliente = db.Column(db.String)
    celular_cliente = db.Column(db.String)
    email_cliente = db.Column(db.String)
    situacao_cliente = db.Column(db.String)
    tipo_cliente = db.Column(db.String)
    excluido_cliente = db.Column(db.Boolean)

    def __init__(
        self, cpf, nome, dataNascimento, dataCadastro, telefone,
        celular, email, situacao, tipo
    ):
        self.cpf_cliente = cpf
        self.nome_cliente = nome
        self.data_nascimento_cliente = dataNascimento
        self.data_cadastro_cliente = dataCadastro
        self.telefone_cliente = telefone
        self.celular_cliente = celular
        self.email_cliente = email
        self.situacao_cliente = situacao
        self.tipo_cliente = tipo
        self.excluido_cliente = False
    
    def list_of_clients():
        #retorna todos os clientes
        clients = db.session\
                            .query(
                                Cliente.id_cliente, 
                                Cliente.nome_cliente
                            )\
                            .filter(
                                Cliente.excluido_cliente == False
                            )
        
        #inicia lista com um valor em branco
        list = [(0, '')]

        for client in clients:
            list.append((client.id_cliente, client.nome_cliente))
        
        return list

    def list_of_clients_no_monthly():
        clients = db.session\
                    .query(
                        Cliente.id_cliente, 
                        Cliente.nome_cliente
                    )\
                    .outerjoin(
                        Mensalidade, 
                        and_(
                            Mensalidade.cliente_id_cliente == Cliente.id_cliente, 
                            Mensalidade.excluido_mensalidade == False
                        )
                    )\
                    .filter(
                        Cliente.excluido_cliente == False,
                        or_(
                            Mensalidade.situacao_mensalidade == None,
                            Mensalidade.situacao_mensalidade == 'pago'
                        )
                    )
        
        #inicia lista com um valor em branco
        list = [(0, '')]

        for client in clients:
            list.append((client.id_cliente, client.nome_cliente))
        
        return list

    def is_deleted(self):
        return self.excluido_cliente

class Veiculo(db.Model):
    __tableName__ = "veiculo"

    placa_veiculo = db.Column(db.String, primary_key=True)
    marca_veiculo = db.Column(db.String)
    modelo_veiculo = db.Column(db.String)
    cor_veiculo = db.Column(db.String)
    ano_fabricacao_veiculo = db.Column(db.String)
    ano_modelo_veiculo = db.Column(db.String)
    excluido_veiculo = db.Column(db.Boolean)
    cliente_id_cliente = db.Column(db.String)

    def __init__(self, placa, marca, modelo, cor, anoFabricacao, anoModelo, id_cliente):
        self.placa_veiculo = placa
        self.marca_veiculo = marca
        self.modelo_veiculo = modelo
        self.cor_veiculo = cor
        self.ano_fabricacao_veiculo = anoFabricacao
        self.ano_modelo_veiculo = anoModelo
        self.excluido_veiculo = False
        self.cliente_id_cliente = id_cliente
    
    def is_deleted(self):
        return self.excluido_veiculo

class Servico(db.Model):
    __tableName__ = "servico"

    id_servico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_servico = db.Column(db.String)
    descricao_servico = db.Column(db.String)
    situacao_servico = db.Column(db.String)
    preco_servico = db.Column(db.Float)
    tipo_servico = db.Column(db.String)
    excluido_servico = db.Column(db.Boolean)

    def __init__(self, nome, descricao, preco, tipo, situacao):
        self.nome_servico = nome
        self.descricao_servico = descricao
        self.preco_servico = preco
        self.tipo_servico = tipo
        self.situacao_servico = situacao
        self.excluido_servico = False

    def is_deleted(self):
        return self.excluido_servico

class Mensalidade(db.Model):
    __tableName__ = "mensalidade"

    id_mensalidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_mensalidade = db.Column(db.Float)
    data_vencimento_mensalidade = db.Column(db.String)
    data_pagamento_mensalidade = db.Column(db.String)
    situacao_mensalidade = db.Column(db.String)
    excluido_mensalidade = db.Column(db.Boolean)
    cliente_id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))

    def __init__(self, valor, data_vencimento, data_pagamento, situacao, id_cliente):
        self.valor_mensalidade = valor
        self.data_vencimento_mensalidade = data_vencimento
        self.data_pagamento_mensalidade = data_pagamento
        self.situacao_mensalidade = situacao
        self.cliente_id_cliente = id_cliente
        self.excluido_mensalidade = False
    
    def is_deleted(self):
        return self.excluido_mensalidade