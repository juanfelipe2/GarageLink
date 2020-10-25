from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user

from . import monthly_payment
from app import db
from app.models.forms import MonthlyPayment
from app.models.tables import Mensalidade, Cliente

@monthly_payment.route('/cadastro-de-mensalidade', methods=['GET','POST'])
def register_monthly_payment():
    #Guarda de rota, apenas usuário autenticado pode registrar
    if current_user.is_authenticated:
        form = MonthlyPayment()
        
        if form.is_submitted():
            #Obtem informações do formulário de registro
            id_cliente = form.id_cliente.data
            valor = form.valor.data
            data_vencimento = form.data_vencimento.data
            data_pagamento = form.data_pagamento.data
            situacao =  form.situacao.data.lower()

            #Cria objeto Mensalidade
            monthly_payment = Mensalidade(
                    valor=valor,
                    data_vencimento=data_vencimento,
                    data_pagamento=data_pagamento,
                    situacao=situacao,
                    id_cliente=id_cliente
                )

            #Grava no banco de dados
            db.session.add(monthly_payment)
            db.session.commit()

            #Redireciona para lista de usuários
            return redirect(url_for('monthly_payment.list_monthly_payment'))
        
        #carrega combo box com a lista de funcionários
        elif not form.id_cliente.data:
            form.id_cliente.choices = Cliente.list_of_clients_no_monthly()
            form.process()

        return render_template('monthly_payment/monthly_payment_register.html', form=form)
    
    return redirect('pagina-inicial')

@monthly_payment.route('/lista-de-mensalidades', methods=['GET'])
def list_monthly_payment():
    if current_user.is_authenticated and current_user.is_manager():
        monthly_payments = Mensalidade.query.filter_by(excluido_mensalidade = False)
        return render_template('monthly_payment/monthly_payment_list.html', monthly_payments=monthly_payments)

    return redirect('pagina-inicial')

@monthly_payment.route('/editar-mensalidade/<string:id_mensalidade>', methods=['GET','POST'])
def edit_monthly_payment(id_mensalidade):
    if current_user.is_authenticated and current_user.is_manager():
        form = MonthlyPayment()

        if form.is_submitted():
            #Obtem usuário cadastrado no banco de dados
            monthly_payment = Mensalidade.query.filter_by(id_mensalidade=id_mensalidade).first()
            
            #Obtem informações do formulário
            valor = form.valor.data
            data_vencimento = form.data_vencimento.data
            data_pagamento = form.data_pagamento.data
            situacao =  form.situacao.data.lower()

            #Altera informações para alteração no banco de dados
            monthly_payment.valor_mensalidade = valor
            monthly_payment.data_vencimento_mensalidade = data_vencimento
            monthly_payment.data_pagamento_mensalidade = data_pagamento
            monthly_payment.situacao_mensalidade = situacao

            #Grava no banco de dados
            db.session.add(monthly_payment)
            db.session.commit()

            return redirect(url_for('monthly_payment.list_monthly_payment'))
        else:
            monthly_payment = Mensalidade.query.filter_by(id_mensalidade=id_mensalidade).first()

            if monthly_payment: 
                client = Cliente.query.filter_by(id_cliente=monthly_payment.cliente_id_cliente).first()
                
                #carrega campos de seleção
                form.id_cliente.choices = [(client.id_cliente, client.nome_cliente)]
                form.situacao.default = monthly_payment.situacao_mensalidade.capitalize()
                form.process()
            return render_template('monthly_payment/monthly_payment_edit.html', form=form, monthly_payment=monthly_payment)
    
    return redirect('pagina-inicial')

@monthly_payment.route('/excluir-mensalidade/<string:id_mensalidade>', methods=['GET','POST'])
def delete_monthly_payment(id_mensalidade):
    if current_user.is_authenticated and current_user.is_manager():
        monthly_payment = Mensalidade.query.filter_by(id_mensalidade=id_mensalidade).first()
        monthly_payment.excluido_mensalidade = True
        db.session.add(monthly_payment)
        db.session.commit()
        return redirect(url_for('monthly_payment.list_monthly_payment'))

    return redirect('pagina-inicial')