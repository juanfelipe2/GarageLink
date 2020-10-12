from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    __tableName__ = "usuario"

    login = db.Column(db.String, primary_key=True)
    senha = db.Column(db.String)
    nome = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    tipo = db.Column(db.String)

    def __init__(self, login, senha, nome, email, tipo):
        self.login = login
        self.senha = generate_password_hash(senha)
        self.nome = nome
        self.email = email
        self.tipo = tipo

    def get_id(self):
        return self.login
    
    def set_password(self, pwd):
        self.senha =  generate_password_hash(pwd)

    def verify_password(self, pwd):
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

