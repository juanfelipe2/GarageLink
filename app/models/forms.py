from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired


class UserLoginForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])


class UserRegisterForm(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    login = StringField("login", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    tipo = SelectField(
        "tipo",
        validators=[DataRequired()],
        choices=['', 'Atendente', 'Gerente']
        )


class ClientRegisterForm(FlaskForm):
    id_cliente = StringField("id_cliente", validators=[DataRequired()])
    cpf = StringField("cpf", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    dataNascimento = StringField("dataNascimento", validators=[DataRequired()])
    dataCadastro = StringField("dataCadastro", validators=[DataRequired()])
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


class VehicleRegisterForm(FlaskForm):
    placa = StringField("placa", validators=[DataRequired()])
    modelo = StringField("modelo", validators=[DataRequired()])
    cor = StringField("cor", validators=[DataRequired()])
    anoFabricacao = PasswordField("anoFabricacao", validators=[DataRequired()])
    anoModelo = PasswordField("anoModelo", validators=[DataRequired()])
    id_cliente = PasswordField("id_cliente", validators=[DataRequired()])
