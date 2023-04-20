from datetime import datetime, timedelta
import requests, json
import math
from app import db, app
from app.models import User, UserAddress, Address, Payment, Tariff
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


def client_pay():
    pass



def equiring(user_id: int, amount: int, return_url: str):
    """ Эквайринг """

    url = app.config['EQUIRE_URL_CREATE']

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
            'return_url': return_url
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
    else:
        response_2can = json.loads(answer.text)
        head = answer.headers
        order_id_in_system = response_2can['orders'][0].get('id', None)
        if order_id_in_system is not None:
            client_pay()
