from app import db
from flask_login import UserMixin
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

class Funcionario(db.Model, UserMixin):
    __tableName__ = "funcionario"

    id_funcionario = db.Column(db.Integer, primary_key=True)
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

    id_cliente = db.Column(db.String, primary_key=True)
    cpf = db.Column(db.String)
    nome = db.Column(db.String)
    dataNascimento = db.Column(db.String)
    dataCadastro = db.Column(db.String)
    celular = db.Column(db.String)
    email = db.Column(db.String)
    situacao = db.Column(db.String)
    tipo = db.Column(db.String)

    def __init__(
        self, id_cliente, cpf, nome, dataNascimento, dataCadastro, celular,
        email, situacao, tipo
    ):
        self.id_cliente = id_cliente
        self.cpf = cpf
        self.nome = nome
        self.dataNascimento = dataNascimento
        self.dataCadastro = dataCadastro
        self.celular = celular
        self.email = email
        self.situacao = situacao
        self.tipo = tipo

    def get_id(self):
        return self.id_cliente


class Veiculo(db.Model, UserMixin):
    __tableName__ = "veiculo"

    placa = db.Column(db.String, primary_key=True)
    modelo = db.Column(db.String)
    cor = db.Column(db.String)
    anoFabricacao = db.Column(db.String)
    anoModelo = db.Column(db.String)
    id_cliente = db.Column(db.String)

    def __init__(self, placa, modelo, cor, anoFabricacao, anoModelo, id_cliente):
        self.placa = placa
        self.modelo = modelo
        self.cor = cor
        self.anoFabricacao = anoFabricacao
        self.anoModelo = anoModelo
        self.id_cliente = id_cliente

    def get_id(self):
        return self.placa

