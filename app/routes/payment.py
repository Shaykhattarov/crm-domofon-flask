
from app import app
from flask import request, redirect, url_for
from common.payment import successfull_payment



@app.route('/successfull-payment', methods=['GET', 'POST'])
def success_payment():
    order_id = request.args.get('order_id')
    response = successfull_payment(order_id=order_id)
    if response['error'] == '':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('error_payment'))
    

@app.route('/error-payment', methods=['GET', 'POST'])
def error_payment():
    return "Ошибка оплаты"

