from app.models import Address
from app import db


def generate_address_help_list() -> list[dict]:
    """ Генерируется список подсказок адресов пользователю """
    address: Address = db.session.query(Address).all()

    address_list: list[dict] = []
    
    for addr in address:
        address_list.append({
            "id": addr.id,
            "street": addr.street,
            "house": addr.house,
            "front_door": addr.front_door,
            "apartment": addr.apartment,
            "district_id": addr.district_id
        })
        
    return address_list


def generate_streets_help_list(district_id: int) -> list[dict]:
    """ Генерируется списко подсказок улиц после выбора района """
    address: Address = db.session.query(Address).filter_by(district_id=district_id).all()
    address_list: list[dict] = []
    for addr in address:
        address_list.append({
            "id": addr.id,
            "street": addr.street,
            "house": addr.house,
            "front_door": addr.front_door,
            "apartment": addr.apartment,
            "district_id": addr.district_id
        })
    return address_list


def generate_houses_help_list(street: str) -> list[dict]:
    """ Генерирует список подсказок домов после выбора получения улицы """
    address: Address = db.session.query(Address).filter_by(street=street).all()
    address_list: list[dict] = []
    for addr in address:
        address_list.append({
            "id": addr.id,
            "street": addr.street,
            "house": addr.house,
            "front_door": addr.front_door,
            "apartment": addr.apartment,
            "district_id": addr.district_id
        })
    return address_list

    
