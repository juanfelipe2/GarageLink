from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional
from app.models.tables import Funcionario, Usuario
from app import db

class FunctionaryForm(FlaskForm):
    id_funcionario = StringField("id_funcionario", validators=[Optional()])
    nome = StringField("nome", validators=[DataRequired()])
    cpf = StringField("cpf", validators=[DataRequired()])
    telefone = StringField("telefone", validators=[Optional()])
    celular = StringField("celular", validators=[DataRequired()])
    endereco = StringField("endereco", validators=[DataRequired()])
    tipo = SelectField(
            "tipo",
            validators=[DataRequired()],
            choices=['', 'Atendente', 'Gerente']
        )


class UserLoginForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])

class UserForm(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    login = StringField("login", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    tipo = SelectField(
            "tipo",
            validators=[DataRequired()],
            choices=['', 'Atendente', 'Gerente']
        )
    situacao = SelectField(
            "situacao", validators=[DataRequired()],
            choices=['', 'Ativo','Inativo']
        )
    id_funcionario = SelectField("id_funcionario", validators=[DataRequired()])


class ClientForm(FlaskForm):
    id_cliente = StringField("id_cliente", validators=[Optional()])
    cpf = StringField("cpf", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    dataNascimento = StringField("dataNascimento", validators=[DataRequired()])
    dataCadastro = StringField("dataCadastro", validators=[DataRequired()])
    telefone = StringField("telefone", validators=[Optional()])
    celular = StringField("celular", validators=[Optional()])
    email = StringField("email", validators=[Optional()])
    situacao = SelectField(
            "situacao",
            validators=[DataRequired()],
            choices=['', 'Em dia', 'À pagar']
        )
    tipo = SelectField(
            "tipo",
            validators=[DataRequired()],
            choices=['', 'Mensalista', 'Único']
        )


class VehicleForm(FlaskForm):
    id_cliente = SelectField("id_cliente", validators=[Optional()])
    placa = StringField("placa", validators=[DataRequired()])
    marca = StringField("marca", validators=[DataRequired()])
    modelo = StringField("modelo", validators=[DataRequired()])
    cor = StringField("cor", validators=[DataRequired()])
    anoFabricacao = StringField("anoFabricacao", validators=[DataRequired()])
    anoModelo = StringField("anoModelo", validators=[DataRequired()])

class ServiceForm(FlaskForm):
    id_servico = IntegerField("id_servico", validators=[Optional()])
    nome = StringField("nome", validators=[DataRequired()])
    descricao = StringField("descricao", validators=[DataRequired()])
    preco = FloatField("preco", validators=[DataRequired()])
    tipo = SelectField(
            "tipo",
            validators=[DataRequired()],
            choices=['', 'Servico', 'Estacionamento']
        )
    situacao = situacao = SelectField(
            "situacao",
            validators=[DataRequired()],
            choices=['', 'Ativo', 'Inativo']
        )
