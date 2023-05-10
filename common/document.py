import os
from app import app, db
import uuid
from app.models import Document


def upload_document(file: object) -> str:
    """ Сохранение документа на сервер """
    
    filename: str = file.filename
    newname = f'{uuid.uuid1()}.{filename.split(".")[1]}'
    filepath: str = os.path.join(app.config['UPLOAD_DOCUMENT'], newname)
    file.save(filepath)

    document = Document(
        name=filename,
        name_on_server=f"/static/images/documents/{newname}"
    )

    db.session.add(document)
    db.session.commit()

    return filepath


def view_document() -> object:
    try:
        doc = db.session.query(Document).all()
    except Exception as err:
        print(err)
        return {'status': False, 'message': err}
    else:
        return {'status': True, 'message': doc}

