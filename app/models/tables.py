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
        self.login =login
        self.senha = generate_password_hash(senha)
        self.nome = nome
        self.email = email
        self.tipo = tipo

    def get_id(self):
        return self.login
        
    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)