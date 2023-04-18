from app import db
from app.models import UserAddress



def get_user_address_list() -> list[object] | None:
    """ Получение списка адресов в виде списка объектов из базы данных """
    address_list: list = []
    try:
        address_list: list[UserAddress] = db.session.query(UserAddress).all()
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
        if address.building is None or len(address.building) == 0:
            if address.apartment is None or len(address.apartment) == 0:
                string: str = f'ул. {address.street}, д. {address.house}, п. {address.front_door}'
            else:
                string: str = f'ул. {address.street}, д. {address.house}, п. {address.front_door}, кв. {address.apartment}'
        else:
            if address.apartment is None or len(address.apartment) == 0:
                string: str = f'ул. {address.street}, д. {address.house}, корп. {address.building},  п. {address.front_door}'
            else:
                string: str = f'ул. {address.street}, д. {address.house}, корп. {address.building}, п. {address.front_door}, кв. {address.apartment}'

        result.append([address.id, string])
    return result
