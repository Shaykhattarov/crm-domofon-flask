import json
from app import app
from flask import request
from common.address import generate_address_hints



@app.route('/hint/address', methods=['GET', 'POST'])
def street_hint():
    hints: list = generate_address_hints()
    return json.dumps(hints, ensure_ascii=False)
