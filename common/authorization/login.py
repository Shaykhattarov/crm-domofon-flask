from app import db
from app.models import User


def authentication(name: str, email: str) -> dict | None:
    try:
        user = db.session.query(User).filter_by(name=name, email=email).first()
    except Exception as err:
        return {'status': False, 'result': err}
    else:
        if user is not None:
            return {'status': True, 'result': user}
        else:
            return {'status': False, 'result': None}