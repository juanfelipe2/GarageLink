from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import IntegerField
from wtforms import FloatField
from wtforms import DateField
from wtforms import DateTimeField
from wtforms import HiddenField
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
    id_cliente = SelectField("id_cliente", validators=[DataRequired()])
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


class MonthlyPayment(FlaskForm):
    id_cliente = SelectField("id_cliente", validators=[DataRequired()])
    id_mensalidade = IntegerField("id_mensalidade", validators=[Optional()])
    valor = FloatField("valor", validators=[DataRequired()])
    data_vencimento = DateField("data_vencimento", validators=[DataRequired()])
    data_pagamento = DateField("data_pagamento", validators=[DataRequired()])
    situacao = SelectField(
            "situacao",
            validators=[DataRequired()],
            choices=['', 'Pago', 'Em aberto', 'Vencido']
        )

class Parking(FlaskForm):
    id_estacionamento = IntegerField("id_estacionamento", validators=[DataRequired()])
    placa_veiculo = SelectField("placa_veiculo", validators=[DataRequired()])
    id_vaga = SelectField("id_vaga", validators=[DataRequired()])
    entrada = DateTimeField("entrada", validators=[DataRequired()])
    saida = DateTimeField("saida", validators=[DataRequired()])
    tempo_permanencia = DateTimeField("tempo_permanencia", validators=[DataRequired()])
    observacao = StringField("observacao", validators=[Optional()])
    desconto = FloatField("desconto", validators=[Optional()])
    valor_liquido = FloatField("valor_liquido", validators=[DataRequired()])
    valor_total = FloatField("valor_total", validators=[DataRequired()])
    valor_recebido = FloatField("valor_recebido", validators=[DataRequired()])
    troco = FloatField("troco", validators=[Optional()])
    desconto = IntegerField("desconto", validators=[Optional()])
    tipo_pagamento = SelectField(
            "tipo_pagamento",
            validators=[DataRequired()],
            choices=['', 'Dinheiro', 'Crédito', 'Débito']
        )
    situacao = SelectField(
            "situacao",
            validators=[DataRequired()],
            choices=['', 'Pago', 'Em aberto']
        )
    servicos = HiddenField("servicos")
    servicos = HiddenField("valor_hora")

class ServiceParking(FlaskForm):
     id_servico = IntegerField("id_servico", validators=[DataRequired()])
     nome = StringField("nome", validators=[DataRequired()])
     preco = FloatField("preco", validators=[DataRequired()])

class VacancyForm(FlaskForm):
    id_vaga = IntegerField("id_vaga", validators=[Optional()])
    localizacao_vaga = StringField(
        "localizacao_vaga", validators=[DataRequired()]
        )
    codigo_vaga = StringField("codigo_vaga", validators=[DataRequired()])
    situacao_vaga = StringField("situacao_vaga", validators=[DataRequired()])
    situacao_vaga = SelectField(
            "situacao_vaga",
            validators=[DataRequired()],
            choices=['', 'Livre', 'Ocupada']
        )
    veiculo_placa_veiculo = StringField("veiculo_placa_veiculo", validators=[Optional()])


class DamageForm(FlaskForm):
    id_avaria = IntegerField("id_avaria", validators=[Optional()])
    descricao_avaria = StringField(
        "descricao_avaria", validators=[DataRequired()]
        )
    observacao_avaria = StringField("observacao_avaria", validators=[DataRequired()])
    placa_veiculo = SelectField("placa_veiculo", validators=[DataRequired()], choices=[''])
