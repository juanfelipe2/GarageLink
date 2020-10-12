from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
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
    tipo = SelectField("tipo", validators=[DataRequired()], choices=['', 'Atendente','Gerente'])
    situacao = SelectField("situacao", validators=[DataRequired()], choices=['', 'Ativo','Inativo'])
    id_funcionario = SelectField("id_funcionario", validators=[DataRequired()])
