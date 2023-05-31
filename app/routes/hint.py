import json
from app import app
from flask import request
from common.address import generate_address_hints
from fillbase import main


@app.route('/hint/address', methods=['GET', 'POST'])
def street_hint():
    hints: list = generate_address_hints()
    return json.dumps(hints, ensure_ascii=False)

@app.route('/filldatabase', methods=['GET', 'POST'])
def fill():
     main()
     return 'Готово'
