from datetime import datetime, timedelta
import requests, json
import math
from app import db, app
from app.models import User, UserAddress, Address, Payment, Tariff, ArchivePayment
from flask import redirect
from .address import parse_address


def operator_pay_lk(address: str, apartment: str, amount: int):
    """ Оплата через оператора """
    street, house, front_door = parse_address(address)
    month = 30 # В одном месяце 30 дней

    # Проверяем есть ли такой адрес в базе данных
    address = db.session.query(Address).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).first()
    if address is None:
        return {
            'status': 'error',
            'message': 'Такого адреса не существует'
        }
    
    # Получаем его полный адрес
    user_address = db.session.query(UserAddress).filter_by(address_id=address.id).filter_by(apartment=apartment).first()
    if user_address is None:
        return {
            'status': 'error',
            'message': 'Такого адреса пользователя не существует'
        }

    # Получаем данные о пользователях
    users = db.session.query(User).filter_by(address_id=user_address.id).all()
    if users is None or len(users) == 0:
        return {
            'status': 'error',
            'message': 'Пользователи с таким адресом не был найдены'
        }
    
    for user in users:
        if user.payment_id is None:
            continue

        payment = db.session.query(Payment).get(user.payment_id)

        if payment is None:
            print('[ERROR] У пользователя, проживающего по этому адресу, нет проведенных платежей')
        else:
            tariff = db.session.query(Tariff).get(payment.tariff_id)
            if tariff is None:
                    return {
                        'status': 'error',
                        'message': 'Данные о тарифах заполнены некорректно'
                    }
            
            add_period_days: int = math.trunc(amount / (tariff.price / month))

            if add_period_days == 0:
                return {
                    'status': 'error',
                    'message': 'Введена слишком маленькая сумма'
                }

            if payment.active_sub == 1:
                payment_date = datetime.now()
                end_date = payment.end_date + timedelta(days=add_period_days)
                payment.payment_date = payment_date
                payment.end_date = end_date

                db.session.commit()    

                return {
                    'status': 'good',
                    'message': 'Оплата прошла успешно'
                }
            
            if payment.active_sub == 0:
                payment_date = datetime.now()
                end_date = payment_date + timedelta(days=add_period_days)

                payment.payment_date = payment_date
                payment.end_date = end_date
                payment.active_sub = 1

                db.session.commit()

                return {
                    'status': 'good',
                    'message': 'Оплата прошла успешно'
                }                
        
    return {'status': 'error', 'message': 'Оплата по данному адресу никогда не производилась'}


def successfull_payment(request):
    response = {
        'error': ''
    }
    req_result = request.get_data()
    number_order = req_result['order_id']
    if number_order is None:
        response['error'] = 'error'
        response['message'] = 'Неизвестный номер заказа'
        return response

    url = f"{app.config['EQUIRE_GET_ORDER']}/{number_order}" 
    headers = {'Content-type': 'application/json'}
    answer = requests.get(url, headers=headers)
    response_answer = json.loads(answer.text)
    order_response = response_answer.get('orders', {})
    print(answer)
    if order_response is not None:
        status_payment = order_response[0].get('status', False)
        merchant_order_id = order_response[0].get('merchant_order_id', None)
        amount = order_response[0].get(amount, None)
        if merchant_order_id is not None:
            if status_payment:
                if status_payment == "charged":
                    resp = __save_order(merchant_order_id, amount=amount)
                    if resp['error'] == '':
                       return response
                    else:
                       return resp['message']
                else:
                    response['message'] = 'Неизвестный статус'
                    return response


def __save_order(user_id, amount):
    tariff = db.session.query(Tariff).filter_by(amount=amount).first()
    year = False
    if tariff is None:
        year = True
        tariff = db.session.query(Tariff).filter_by(amount=(amount // 12)).first()
        if tariff is None:
            return {
                'error': 'error',
                'message': 'Неизвестная сумма'
            }
    if year:
        end_date = datetime.now() + timedelta(days=365)
    else:
        end_date = datetime.now() + timedelta(days=30)

    payment: Payment = Payment (
        tariff_id=tariff.id,
        active_sub=1,
        payment_date=datetime.now(),
        end_date=end_date
    )
    db.session.add(payment)
    db.session.commit()

    user = db.session.query(User).get(user_id)
    if user.payment_id is not None:
        archive = ArchivePayment(
            payment_id = user.payment_id,
            user_id = user.id
        )
        user.payment_id = payment.id
        db.session.add(archive)
        db.session.commit()

    user.payment_id = payment.id
    db.session.commit()

    return {
        'error': ''
    }





def equiring(user_id: int, amount: int):
    """ Эквайринг """

    url = app.config['EQUIRE_URL_CREATE']
    response = {
        'error': '',
        'payment_url': ''
    }

    user = db.session.query(User).get(user_id)
    user_address = db.session.query(UserAddress).get(user.address_id)
    address = db.session.query(Address).get(user_address.address_id)
    city = 'Москва'
    address = f"ул. {address.street}, д. {address.house}, п. {address.front_door}, кв. {user_address.apartment}"

    headers = {'Content-type': 'application/json', 'Accept': '*/*'}

    data = {
        "merchant_order_id": int(user_id),
        'amount': amount,
        'options': {
            'auto_charge': 1,
            'language': 'ru',
            'return_url': app.config['EQUIRE_RETURN_URL']
        },
        'client': {
            "address": address,
            "city": city,
            "country": "RUS",
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
        },
        "description": "Покупка продуктов или услуг на сайте домофон-тб.рф"
    }

    try:
        answer = requests.post(url=url, headers=headers, data=json.dumps(data))
    except Exception as err:
        print(f'[ERROR] Equire error: {err}')
        return {
            'error': 'error',
            'message': 'Ошибка запроса'
        }
    else:
        response_2can = json.loads(answer.text)
        head = answer.headers
        order_id_in_system = response_2can['orders'][0].get('id', None)
        if order_id_in_system is not None:
            response["payment_url"] = head['Location']
            return response
        else:
            return {
                'status': 'error',
                'message': 'Ошибка в проведении платежа'
            }


def get_payments(user_id: int) -> list[dict]:
    payments: list = []

    user = db.session.query(User).get(user_id)
    if user.payment_id is not None:
        payment = db.session.query(Payment).get(user.payment_id)
        archive = db.session.query(ArchivePayment).filter_by(user_id=user.id).order_by(ArchivePayment.id).all()
        archive_payments = []
        for el in archive:
            payment = db.session.query(Payment).get(el.id)
            archive_payments.append(payment)
        
        print(archive, payment)
    
    return payments