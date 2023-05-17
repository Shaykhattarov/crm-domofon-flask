from app import db, app
import os, uuid
from app.models import Application, Address
from datetime import datetime



def count_application() -> int:
    app = db.session.query(Application).count()
    return app


def change_application(num: str, date: str, problem: str, status_id: int, image: object):
    file = upload_application(image)

    application = db.session.query(Application).get(num)
    application.date = date,
    application.problem = problem
    application.status = status_id
    application.image = file

    db.session.commit()


def create_application(street: str, house: str, front_door: str, district_id: int, apartment: str, master_id: int, date: str, problem: str, image: object) -> dict:
    """ Создание новой заявки на ремонт """
    file = upload_application(image)
    address = db.session.query(Address).filter_by(district_id=district_id).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).filter_by(apartment=apartment).first()
    if address is None:
        return {
            'error': 'error',
            'message': 'Данный адрес не зарегистрирован!'
        }
    date = datetime.strptime(date, "%d.%m.%Y").date()
    application = Application(
        address_id=address.id,
        master_id=int(master_id),
        status=1,
        date=date,
        problem=problem,
        image=file
    )

    db.session.add(application)
    db.session.commit()

    return {
        'error': ''
    }


def upload_application(file: object):
    filename = file.filename
    new_filename = f"{uuid.uuid1()}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_IMAGE'], f'applications/{new_filename}')
    file.save(filepath)
    return new_filename