import os
from app import app
import uuid


def upload_document(file: object) -> str:
    """ Сохранение документа на сервер """
    
    filename: str = file.filename
    filepath: str = os.path.join(app.config['UPLOAD_DOCUMENT'], f'{uuid.uuid1()}_{filename}')
    file.save(filepath)

    return filepath


