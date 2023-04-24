from app import db, app
import os, uuid
from app.models import Application



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


def create_application(address: str, apartment: str, master_id: int, date: str, problem: str, image: object) -> dict:
    """ Создание новой заявки на ремонт """

    file = upload_application(image)

    application = Application(
        address=address,
        apartment=apartment,
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