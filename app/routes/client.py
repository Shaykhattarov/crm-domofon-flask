from app import app, db
from flask import request, redirect, url_for, flash, render_template, session
from flask_login import login_required, current_user
from app.models import Tariff
from common.payment import get_payments, equiring


@app.route('/tariffs', methods=['GET', 'POST'])
@login_required
def client_tariffs():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
       checkbox = request.form.get('agreement')
       if checkbox is None:
           flash('Пожалуйста, примите соглашение об оферте!')
           return redirect(url_for('client_tariffs'))
           
       phone = request.form.get('phone')
       notphone = request.form.get('notphone')
       if phone is not None:
           session['phone'] = True
           return redirect(url_for('tariffs_call'))
       
       if notphone is not None:
           session['phone'] = False
           return redirect(url_for('tariffs_call'))
       
    return render_template('/client/tariffs.html')



@app.route('/contract-offer')
@login_required
def contract_offer():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('/client/contract_offer.html')



@app.route('/payments')
@login_required
def client_payments():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    payments = []
    payments: list[dict] = get_payments(user_id=current_user.id)
    
    return render_template('/client/payments.html', payments=payments)
    


@app.route('/tariffs-call')
@login_required
def tariffs_call():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if session['phone']:
        tariff = db.session.query(Tariff).get(1)
    else:
        tariff = db.session.query(Tariff).get(2)

    session['month'] = tariff.price
    session['year'] = tariff.price * 12
    
    return render_template('/client/tariffs_call.html', month=tariff.price, year=(tariff.price * 12))



@app.route('/tariffs-call-month', methods=['GET', 'POST'])
def tariffs_call_month():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))

    response = equiring(user_id=current_user.id, amount=session['month'])
    if response is None or response['error'] == '':
        return redirect(response['payment_url'])
    else:
        if response['message'] is not None:
            flash(response['message'])
            return redirect(url_for('tariff-calls'))
        else:
            flash('Ошибка оплаты')
            return redirect(url_for('tariff-calls'))



@app.route('/tariffs-call-year', methods=['GET', 'POST'])
def tariffs_call_year():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    response = equiring(user_id=current_user.id, amount=session['year'])
    if response['error'] == '':
        return redirect(response['payment_url'])
    else:
        if response['message'] is not None:
            flash(response['message'])
            return redirect(url_for('tariff-calls'))
        else:
            flash('Ошибка оплаты')
            return redirect(url_for('tariff-calls'))

