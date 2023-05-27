from app import db, app
from app.models import ApplicationReport, Application
import uuid, os
from datetime import datetime

from app.models.tariff import Tariff
from app.models import Address, User, Subscription
from .payment import get_user_debt

def create_report(app_id: int, status_id: int, master_id: int, addition: str, image: str, date: str):
    file = upload_report(image)

    app = db.session.query(Application).get(app_id)
    app.status = status_id
    db.session.commit()

    report = ApplicationReport(
        application_id=app_id,
        master_id=master_id,
        addition=addition,
        image=file,
        date=date
    )

    db.session.add(report)
    db.session.commit()


def upload_report(file):
    filename = file.filename
    new_filename = f"{uuid.uuid1()}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_IMAGE'], f'reports/{new_filename}')
    file.save(filepath)
    return new_filename


def view_report_about_master(master_id: int, from_date: str, to_date: str):
    from_date = datetime.strptime(from_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    applications_count = db.session.query(Application).filter_by(master_id=master_id).filter_by(status=3).filter(Application.date >= from_date, Application.date <= to_date).count()
    return_applications = db.session.query(Application).filter(Application.address_id == Application.address_id, Application.date >= from_date, Application.date <= to_date).count()
    return [applications_count, return_applications]


def view_report_about_applications(district_id: int, street: str, house: str, front_door: str, apartment: str, from_date: str, to_date: str):
    from_date = datetime.strptime(from_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    address = db.session.query(Address).filter_by(district_id=district_id).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).filter_by(apartment=apartment).first()
    if address is None:
        return {
            'error': 'error',
            'message': 'Данный адрес не зарегистрирован!'
        }
    applications_count = db.session.query(Application).filter_by(status=3).filter_by(address_id=address.id).filter(Application.date >= from_date, Application.date <= to_date).count()
    return_applications = db.session.query(Application).filter_by(address_id=address.id).filter(Application.address_id == Application.address_id, Application.date >= from_date, Application.date <= to_date).count()
    return {'error': '','message': [applications_count, return_applications]}


def view_report_about_payments(district_id: int, street: str, house: str, front_door: str, apartment: str, from_date: str, to_date: str):

    from_date = datetime.strptime(from_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%d.%m.%Y").strftime("%Y-%m-%d")
    address = db.session.query(Address).filter_by(district_id=district_id).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).filter_by(apartment=apartment).first()
    if address is None:
        return {
            'error': 'error',
            'message': 'Данный адрес не зарегистрирован!'
        }
    
    user = db.session.query(User).filter_by(address_id=address.id).first()
    if user is None:
        return {
            'error': 'error',
            'message': 'Пользователя с таким адресом не существует'
        }
    sub = db.session.query(Subscription).get(user.subscription_id)
    if sub is None:
        return {
            'error': 'error',
            'message': 'Подписка не приобреталась'
        }
    pay_option = sub.option
    tariff = db.session.query(Tariff).get(sub.tariff_id)
    tariff = f"{tariff.name} - {tariff.price}"
    debt_amount = get_user_debt(user.id)
    if debt_amount['message'] != 'None':
        return {
            'error': '',
            'message': [debt_amount, pay_option, tariff]
        }
    else:
        return {
            'error': '',
            'message': [0, pay_option, tariff]
        }
