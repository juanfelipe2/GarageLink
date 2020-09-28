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
    tipo = SelectField("tipo", validators=[DataRequired()], choices=['', 'Atendente','Gerente'])