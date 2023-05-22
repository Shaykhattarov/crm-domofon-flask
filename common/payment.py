from app import db, app
import requests, json, math
from datetime import datetime, timedelta
from app.models import User, Address, Payment, Tariff, Subscription



def operator_pay_lk(district_id: int, street: str, house: str, front_door: str, apartment: str, amount: int, tariff_id: str=1):
    """ Оплата через оператора """

    # Проверяем есть ли такой адрес в базе данных
    address = db.session.query(Address).filter_by(district_id=district_id).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).filter_by(apartment=apartment).first()
    if address is None:
        return {
            'status': 'error',
            'message': 'Такого адреса не существует'
        }

    # Получаем данные о пользователях
    users = db.session.query(User).filter_by(address_id=address.id).all()
    if users is None or len(users) == 0:
        return {
            'status': 'error',
            'message': 'Пользователи с таким адресом не был найдены'
        }
    
    for user in users:
        if user.subscription_id is None:
            subscription = Subscription (
                tariff_id=tariff_id,
                start_date=datetime.today()
            )

            user.subscription_id = subscription.id
            db.session.add(subscription)
            db.session.commit()
            

        sub = db.session.query(Subscription).get(user.subscription_id)
        tariff = db.session.query(Tariff).get(sub.tariff_id)
        
        if tariff is None:
                return {
                    'status': 'error',
                    'message': 'Данные о тарифах заполнены некорректно'
                }
        
        add_period_days: int = math.trunc(amount / tariff.price)
        if add_period_days < 1:
            return {
                'status': 'error',
                'message': 'Введена слишком маленькая сумма'
            }
        
        payment = Payment (
            subscription_id=sub.id,
            date=datetime.today(),
            period=datetime.today() + timedelta(days=add_period_days),
            amount=amount
        )

        db.session.add(payment)
        
        sub.option = "Индивидуально"
        if sub.active == 1:
            sub.end_date = sub.end_date + timedelta(days=add_period_days)
 
        if sub.active == 0:
            sub.end_date = datetime.today() + timedelta(days=add_period_days)
            sub.active = 1
        
        db.session.add(payment)
        db.session.commit()   

        return {
            'status': 'good',
            'message': 'Оплата прошла успешно'
        }                
        


def successfull_payment(order_id=None):
    response = {
        'error': ''
    }

    if order_id is None:
        response['error'] = 'error'
        response['message'] = 'Неизвестный номер заказа'
        return response

    url = f"{app.config['EQUIRE_GET_ORDER']}/{order_id}" 
    headers = {'Content-type': 'application/json'}
 
    answer = requests.get(url, headers=headers)
    response_answer = json.loads(answer.text)
    order_response = response_answer.get('orders', {})
    
    if order_response is None or order_response == {}:
        return {'error': 'error', 'message': 'Нет ответа от эквайринга!'}
    
    status_payment = order_response[0].get('status', False)
    merchant_order_id = order_response[0].get('merchant_order_id', None)
    amount = float(order_response[0].get('amount', None))

    if merchant_order_id is not None:
        if status_payment:
            if status_payment == "charged":
                resp = __save_order(merchant_order_id, price=amount)
                if resp['error'] == '':
                   return response
                else:
                   return resp['message']
            else:
                response = {'error': 'error', 'status': 'rejected', 'message': 'Оплата не пройдена!'}
                return response



def __save_order(user_id, price):
    """ Сохранение оплаты """
    user = db.session.query(User).get(user_id)
    if user is None:
        return {'error': 'error', 'message': 'Пользователя с таким id не существует!'}
    
    tariffs = db.session.query(Tariff).all()
    if tariffs is None or tariffs == []:
        return {'error': 'error', 'message': 'Тарифы не найдены!'}
    
    year_period: bool = False
    validation_tariff: bool = False
    for tariff in tariffs:
        if tariff.price == price:
            validation_tariff = True
        if (price // 12) == tariff.price:
            validation_tariff = True
            year_period = True
    if not validation_tariff:
        return {
            'error': 'error',
            'message': 'Тарифы не найдены!'
        }
    
    if year_period:
        option = 'Ежегодно'
        end_date = end_date = datetime.today() + timedelta(days=365)
    else:
        option = 'Ежемесячно'
        end_date = end_date = datetime.today() + timedelta(days=30)

    if user.subscription_id is None:
        sub = Subscription(
            tariff_id=tariff.id,
            option=option,
            start_date=datetime.today(),
            end_date=end_date,
            active=1
        )
        db.session.add(sub)
        db.session.commit()
        
        user.subscription_id = sub.id

        payment = Payment(
            subscription_id=sub.id,
            date=datetime.today(),
            period=end_date,
            amount=price
        )
        db.session.add(payment)
        db.session.commit()
    else:
        sub = db.session.query(Subscription).get(user.subscription_id)
        
        if sub.active == 1:
            if year_period:
                sub.option = option
                sub.end_date = sub.end_date + timedelta(days=365)
            else:
                sub.option = option
                sub.end_date = sub.end_date + timedelta(days=30)
            
            sub.start_date = datetime.today()

            payment = Payment(
                subscription_id=sub.id,
                date=sub.start_date,
                period=sub.end_date,
                amount=price
            )
            db.session.add(payment)
            db.session.commit()
        else:
            if year_period:
                sub.option = option
                sub.end_date = sub.end_date + timedelta(days=365)
            else:
                sub.option = option
                sub.end_date = sub.end_date + timedelta(days=30)

            sub.start_date = datetime.today()
            sub.active = 1

            payment = Payment(
                subscription_id=sub.id,
                date=sub.start_date,
                period=sub.end_date,
                amount=price
            )
            db.session.add(payment)
            db.session.commit()
    return {
        'error': ''
    }



"""
def __save_order_2(user_id, amount):
    Сохранение оплаты
    user = db.session.query(User).get(user_id)
    tariff = db.session.query(Tariff).filter_by(price=amount).first()
    year = False
    if tariff is None:
        year = True
        tariff = db.session.query(Tariff).filter_by(price=(amount // 12)).first()
        if tariff is None:
            return {
                'error': 'error',
                'message': 'Неизвестная сумма'
            }
    
    if year:
        sub_option = "Ежегодно"
        end_date = datetime.today() + timedelta(days=365)
    else:
        sub_option = "Ежемесячно"
        end_date = datetime.today() + timedelta(days=30)

    if user.subscription_id is None:
        sub = Subscription(
            tariff_id=tariff.id,
            option=sub_option,
            start_date=datetime.today(),
            end_date=end_date,
            active=1
        )

        db.session.add(sub)
        db.session.commit()

        user.subscription_id = sub.id

        payment = Payment (
            subscription_id=sub.id,
            date=datetime.today(),
            period=end_date,
            amount=amount
        )

        db.session.add(payment)
        db.session.commit()     
    else:
        sub = db.session.query(Subscription).get(user.subscription_id)
    

        if sub.active == 1:
            if year:
                sub.end_date = sub.end_date + timedelta(days=365)
            else:
                sub.end_date = sub.end_date + timedelta(days=30)
            
            sub.option = sub_option
        else:
            sub.active = 1
            sub.start_date = datetime.today()
            sub.end_date = end_date
            sub.option = sub_option

        db.session.add(payment)
        db.session.commit()

    return {
        'error': ''
    }
"""


def equiring(user_id: int, amount: int):
    """ Эквайринг """
    url = app.config['EQUIRE_URL_CREATE']
    response = {
        'error': '',
        'payment_url': ''
    }

    user = db.session.query(User).get(user_id)
    address = db.session.query(Address).get(user.address_id)
    if address is None:
        return {'error': 'error', 'message': 'Адрес неизвестен'}

    city = 'Москва'
    address = f"ул. {address.street}, д. {address.house}, п. {address.front_door}, кв. {address.apartment}"

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

    result: list = []

    user = db.session.query(User).get(user_id)
   
    if user.subscription_id is not None:
        sub = db.session.query(Subscription).get(user.subscription_id)
        tariff = db.session.query(Tariff).get(sub.tariff_id)
        payments = db.session.query(Payment).filter_by(subscription_id=sub.id).all()
        for payment in payments:
            status = ''
            print(payment.period, sub.end_date, type(payment.period), type(sub.end_date))
            if payment.period == sub.end_date:
                status = True
            else:
                status = False

            result.append({
                'payment_date': datetime.strftime(payment.date, "%d.%m.%Y"),
                'end_date': datetime.strftime(payment.period, "%d.%m.%Y"),
                'tariff': tariff.name,
                'option': sub.option,
                'status': status
            })
    
    return result



def check_subscriptions():
    users = db.session.query(User).filter_by(role_id=1).all()

    for user in users:
        if user.subscription_id is None:
            continue
        sub = db.session.query(Subscription).get(user.subscription_id)
        if sub.end_date < datetime.date(datetime.today()):
            sub.active = 0
            db.session.commit()
        else:
            continue



def get_user_debt(user_id: int):
    user = db.session.query(User).get(user_id)
    sub = db.session.query(Subscription).get(user.subscription_id)
    if sub.active == 1:
        return {
            'error': '',
            'message': 'None'
        }
    
    end_date = sub.end_date
    today = datetime.today().date()
    tariff = db.session.query(Tariff).get(sub.tariff_id)
    add_period_days = tariff.price / 30
    
    if end_date < today:
        dif = today - end_date
        debt = dif.days * add_period_days
        return {
            'error': '',
            'message': debt
        }
    else:
        return {
            'error': '',
            'message': 'None'
        }
