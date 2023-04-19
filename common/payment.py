from app import db
from app.models import User, UserAddress, Address, Payment, Tariff
from address import parse_address


def operator_pay_lk(address: str, apartment: str, amount: str):
    """ Оплата через оператора """
    street, house, front_door = parse_address(address)
    
    return 