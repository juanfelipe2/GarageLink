from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired
from app.models.tables import Funcionario, Usuario
from app import db


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
    id_cliente = StringField("id_cliente", validators=[DataRequired()])
    cpf = StringField("cpf", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    dataNascimento = StringField("dataNascimento", validators=[DataRequired()])
    dataCadastro = StringField("dataCadastro", validators=[DataRequired()])
    telefone = StringField("telefone", validators=[DataRequired()])
    celular = StringField("celular", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
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
    id_cliente = SelectField("id_cliente", validators=[DataRequired()])
    placa = StringField("placa", validators=[DataRequired()])
    marca = StringField("marca", validators=[DataRequired()])
    modelo = StringField("modelo", validators=[DataRequired()])
    cor = StringField("cor", validators=[DataRequired()])
    anoFabricacao = StringField("anoFabricacao", validators=[DataRequired()])
    anoModelo = StringField("anoModelo", validators=[DataRequired()])
