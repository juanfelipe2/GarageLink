from app import db
from flask_login import UserMixin
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

class Funcionario(db.Model, UserMixin):
    __tableName__ = "funcionario"

    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_funcionario = db.Column(db.String)
    cpf_funcionario = db.Column(db.String)
    telefone_funcionario = db.Column(db.String)
    celular_funcionario = db.Column(db.String)
    endereco_funcionario = db.Column(db.String)
    tipo_funcionario = db.Column(db.String)
    excluido_funcionario = db.Column(db.Boolean)

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


class Cliente(db.Model, UserMixin):
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

    def is_deleted(self):
        return self.excluido_cliente


class Veiculo(db.Model, UserMixin):
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
