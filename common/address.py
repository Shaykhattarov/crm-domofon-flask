from app import db
from app.models import User, Address, Equipment
import requests


def generate_address_hints() -> list[dict]:
    """ Функция генерации списка подсказок для адресов """
    try:
        addresses: Address = db.session.query(Address).all()
    except Exception as err:
        print(err)
        return {
            'status': 'error',
            'message': f'Произошла ошибка при обращении к базе: {err}'
        }
    else:    
        if addresses is None and len(addresses) == 0:
            return {
                'status': 'error',
                'message': 'База адресов пуста'
            }
        streets: list = []
        result: list = []
        for address in addresses:
            if address.street not in streets:
                streets.append(address.street)
        
        for street in streets:
            street_info = {}
            street_info.update(street=street, house=[], district_id=[], front_door=[], apartment=[])
            for address in addresses:
                if address.house not in street_info['house']:
                    street_info['house'].append(address.house)
                if address.district_id not in street_info['district_id']:
                    street_info['district_id'].append(address.district_id)
                if address.front_door not in street_info['front_door']:
                    street_info['front_door'].append(address.front_door)
                if address.apartment not in street_info['apartment']:
                    street_info['apartment'].append(address.apartment)
            result.append(street_info)                
            
    return {
        'status': 'Ok',
        'data': result
    }


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
    if check_kladr_address(street=street, house=house) is None:
        return False
    
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
        return preaddress

    equipment: Equipment = Equipment(
        equipment_id=equipment_list_id,
        serial_code=serial_code
    )

    db.session.add(equipment)
    db.session.commit()

    if not is_int(apartment_from):
        address: Address = Address(
                street=street,
                house=house,
                apartment=apartment_from,
                front_door=front_door,
                district_id=district_id,
                tariff_id=tariff_id,
                equipment_id=equipment.id
            )
        db.session.add(address)

    if apartment_to is None or len(apartment_to) == 0:
        address: Address = Address(
                street=street,
                house=house,
                apartment=apartment_from,
                front_door=front_door,
                district_id=district_id,
                tariff_id=tariff_id,
                equipment_id=equipment.id
            )
        db.session.add(address)

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

def is_int(string: str):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True


def check_kladr_address(street: str, house: str):
    """ Проверка адреса на существование """
    cityId: str = '7700000000000'
    kladr_url: str = "https://kladr-api.ru/api.php"
    street_url: str = f"{kladr_url}?query={street}&cityId={cityId}&oneString=1&limit=1&withParent=1&contentType=street"
    request_street = requests.get(street_url, headers={'Access-Control-Allow-Origin': '*'})
    street_data = request_street.json()
    if street_data['result'] is None or street_data['result'][0]['name'] != street:
        return None 
    
    return True

def change_address_individual_code(street: str, house: str, front_door: str, apartment: str, district: int, code: str):
    """ Изменение индивидуального кода подъезда """
    address = db.session.query(Address).filter_by(district_id=district).filter_by(street=street).filter_by(house=house).filter_by(front_door=front_door).filter_by(apartment=apartment).first()
    if address is not None:
        address.code = code
        db.session.commit()
        return address.id
    else:
        return None


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
        

def view_addresses() -> list[str] | None:
    """ Функция генерирует список всех адресов для отображения """
    addresses = db.session.query(Address).all()
    if addresses is None or addresses == []:
        return None
    
    result: list = []
    for address in addresses:
        if address.front_door is not None:
            string: str = f'ул. {address.street}, д. {address.house}, п. {address.front_door}, кв. {address.apartment}'
        else:
            string: str = f'ул. {address.street}, д. {address.house}, кв. {address.apartment}'

        result.append([address.id, string])
    return result