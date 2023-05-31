import pandas
from app import db
from app.models import Address


def parse_excel() -> list[dict]:
    """ Достаем данные из exce и парсим """
    filepath = 'E:/OpenServer/domains/domofon.loc/Copy of Технология безопасности 01.01.18. Останкино 1..xlsx'
    excel_data = pandas.read_excel(filepath, sheet_name="Лист1", keep_default_na=False)    
    parse_apartments: list = excel_data['№ кв.'].tolist()
    addresses: list[dict] = parse_addresses_from_excel(parse_apartments)
    addresses: list[dict] = generate_addresses_with_apartments(streets=addresses, parse_column=parse_apartments)
    return addresses



def generate_addresses_with_apartments(streets: list[dict], parse_column: list) -> list[dict]:
    addresses: list[dict] = []
    val = False
    old_el = ''
    for street in streets:
        if 'front_door' not in street.keys():
            street_name: str = f"{street['street']} ул. д.{street['house']}"
        else:
            street_name: str = f"{street['street']} ул. д.{street['house']} к.{street['front_door']}"
        for el in parse_column:
            if el == '' or el is None or el == 'ВСЕГО:' or el == 'nan':
                continue
            
            if not val and str(el) == street_name:
                val = True
                continue

            if val and el != 'ИТОГО:' and el != old_el:
                if 'front_door' not in street.keys():
                    addresses.append({
                        'street': street['street'],
                        'house': street['house'],
                        'apartment': str(el)
                    })
                else:
                    addresses.append({
                        'street': street['street'],
                        'house': street['house'],
                        'housing': street['front_door'],
                        'apartment': str(el)
                    })

            if el == 'ИТОГО:':
                val = False

            old_el = el

    return addresses
    
            

def parse_addresses_from_excel(parse_column: list) -> list[dict]:
    addresses: list[dict] = []
    address: dict = {}
    for el in parse_column:
        if el is None or el == '' or el == 'ИТОГО:' or el == 'ВСЕГО:' or el == 'nan':
            continue
        
        if len(str(el)) >= 5:
            el = el.split('д.')
            try:
                address = {
                    'street': el[0][:len(el[0]) - 1].replace(' ул.', ''),
                    'house': el[1].replace(' ', '')
                }
            except IndexError as err:
                pass

            if 'к.' in address['house']:
                address['house'] = el[1].split('к.')[0].replace(' ', '')
                address['front_door'] = el[1].split('к.')[1].replace(' ', '')
            
            addresses.append(address)

    return addresses



def save_to_database(addresses: list[dict]):
    for address in addresses:
        if 'housing' in address.keys():
            address_db = Address(
                street=address['street'],
                house=f'{address["house"]} к.{address["housing"]}',
                tariff_id=1,
                apartment=address['apartment'],
                district_id=1
            )
        else:
            address_db = Address(
                street=address['street'],
                house=address["house"],
                tariff_id=1,
                apartment=address['apartment'],
                district_id=1
            )
        db.session.add(address_db)
        db.session.commit()
        print(address_db.id)


def main():
    print('[INFO] Начало работы программы')
    print('[INFO] Чтение и парсинг excel-файла')
    addresses: list[dict] = parse_excel()
    print('[INFO] Сохранение в базу данных')
    save_to_database(addresses)
    print('[INFO] Конец работы программы')
    