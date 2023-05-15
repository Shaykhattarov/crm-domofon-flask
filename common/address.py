from app import db
from app.models import User, Address, Equipment



def get_user_address_list() -> list[object] | None:
    """ Получение списка адресов в виде списка объектов из базы данных """
    address_list: list = []
    try:
        address_list: list[Address] = db.session.query(Address).all()
    except Exception as err:
        print('[ERROR] Exception in getting adresses: {}'.format(err))
    else:
        if len(address_list) == 0:
            return []
        else:
            return address_list


def prepare_user_address_list(address_list: list) -> list[list[int, str]]:
    """ Подготавливает адреса из базы данных, делая из списка объектов список строк адресов """
    result: list = []
    for address in address_list:
        if address.front_door is not None:
            string: str = f'ул. {address.street}, д. {address.house}, п. {address.front_door}, кв. {address.apartment}'
        else:
            string: str = f'ул. {address.street}, д. {address.house}, кв. {address.apartment}'

        result.append([address.id, string])
    return result


def save_address(street: str, house: str, front_door: str, apartment_from: int, apartment_to: int, tariff_id: str, district_id: int, equipment_list_id: str, serial_code: str):
    """ Сохранение адреса и добавленного оборудования в Базу данных """

    preaddress = db.session.query(Address).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).filter(Address.apartment <= apartment_to, Address.apartment >= apartment_from).all()
    if preaddress is not None and len(preaddress) != 0:
        
        equipment: Equipment = Equipment(
            equipment_id=equipment_list_id,
            serial_code=serial_code
        )
        
        db.session.add(equipment)
        db.session.commit()
        for address in preaddress:
            address.district_id = district_id
            address.tariff_id = tariff_id
            address.equipment_id = equipment.id

        db.session.commit() 
        return preaddress.id

    equipment: Equipment = Equipment(
        equipment_id=equipment_list_id,
        serial_code=serial_code
    )

    db.session.add(equipment)
    db.session.commit()
    
    if apartment_from > apartment_to:
        return False
    if apartment_to <= 0 or apartment_from < 0:
        return False 

    try:
        for apart in range(apartment_from, apartment_to + 1):       
            address: Address = Address(
                street=street,
                house=house,
                apartment=apart,
                front_door=front_door,
                district_id=district_id,
                tariff_id=tariff_id,
                equipment_id=equipment.id
            )
            db.session.add(address)

    except Exception as err:
        print(f'[ERROR] Error in creating address: {err}')
    else:
        db.session.commit()
        return address.id
    
    return False


def change_address_individual_code(address: str, code: str):
    """ Изменение индивидуального кода подъезда """
    address = parse_address(address=address)
   
    address = db.session.query(Address).filter_by(street=address[0]).filter_by(house=address[1]).filter_by(front_door=address[2]).first()

    if address is not None:
        address.individual_code = code
        db.session.commit()
        return address.id
    else:
        return None
    

def parse_address(address: str):
    """ Парсим адрес для изменения кода подъезда """
    address = address.split(', ')

    street = address[0].replace('ул. ', '')
    house = address[1].replace('д. ', '')
    front_door = address[2].replace('п. ', '')

    return [street, house, front_door]


def generate_apartment_help_list(address: str):
    """ Получение списка подсказок квартир для введенного адреса(поиск идет по списку пользователей)  """
    address = parse_address(address=address)
    
    street = address[0]
    house = address[1]
    front_door = address[2]

    address = db.session.query(Address).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).first()

    if address is None:
        return None
    
    user_addresses = db.session.query(Address).filter_by(address_id=address.id).all()

    if user_addresses is None or len(user_addresses) == 0:
        return None

    apartment_list: list = []
    for user_address in user_addresses:
        apartment_list.append((str(user_address.id), user_address.apartment))
    
    if len(apartment_list) != 0: 
        return apartment_list
    else:
        return None


#
#def generate_address_help_list():
#    """ Генерирует списко подсказок для ввода адреса """
#    addresses: Address = db.session.query(Address).order_by(Address.street).all()
#
#    address_list: list = []
#    for address in addresses:
#        fulladdress: str = f"ул. {address.street}, д. {address.house}, п. {address.front_door}"
#        address_list.append((str(address.id), fulladdress))
#
#    return address_list


def get_individual_code(user_id: int) -> str:
    """ Получение индивидуального кода открытия домофона """
    user = db.session.query(User).get(user_id)
    if user.address_id is None:
        return 'Отсутствует'
    else:
        address = db.session.query(Address).get(user.address_id)
        if address.code is None:
            return 'Отсутствует'
        else:
            return address.code