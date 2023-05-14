from app import db
from app.models import User, Address



def create_user(name: str, email: str, street: str, district: int, house: str, front_door: str, apartment: str, phone: str, role_id: int = 1) -> bool:
    address: Address = db.session.query(Address).filter_by(street=street).filter_by(district_id=district).filter_by(house=house).filter_by(front_door=front_door).filter_by(apartment=apartment).first()
    if address is None:
        return {
            'status': 'error',
            'message': 'Работы по данному адресу не поддерживаются. Либо адрес, введен не верно.'
        }
    
    user: User = User(
        name=name,
        email=email,
        phone=phone,
        address_id=address.id,
        role_id=role_id
    )

    db.session.add(user)
    db.session.commit()

    return {
        'status': 'good',
        'message': 'Регистрация прошла успешно'
    }

"""
def create_user(name: str, email: str, street: str, district: int, house: str, front_door: str, apartment: str, phone: str, role_id: int = 1) -> bool:

    if parse_address(address=address) is None:
        return {
            'status': 'error',
            'message': 'Адрес должен выглядить так: ул. [[улица]], д. [[дом]], п. [[подъезд]], кв. [[квартира]]'
        }
    
    street, house, front_door, apartment = parse_address(address=address)

    address = db.session.query(Address).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).first()
    if address is None: 
        return {
            'status': 'error',
            'message': 'Адрес должен выглядить так: ул. [[улица]], д. [[дом]], п. [[подъезд]], кв. [[квартира]]'
        }
    
    user_address = UserAddress (
        address_id=address.id,
        apartment=apartment
    )

    db.session.add(user_address)
    db.session.commit()

    user = User(
        name=name, 
        email=email,
        address_id=user_address.id,
        phone=phone,
        role_id=role_id
    )
    
    db.session.add(user)
    db.session.commit()
    
    return {'status': 'good', 'message': 'успешная регистрация'}


def parse_address(address: str):
    
    address = address.split(', ')
    if len(address) != 4:
        return None
    street = address[0].replace('ул. ', '')
    house = address[1].replace('д. ', '')
    front_door = address[2].replace('п. ', '')
    apartment = address[3].replace('кв. ', '')

    return street, house, front_door, apartment
"""