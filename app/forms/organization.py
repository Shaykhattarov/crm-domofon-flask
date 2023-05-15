from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from app import db
from app.models import EquipmentList, Tariff, District, Address



class OrganizationCreateAddress(FlaskForm):
    street = StringField("Улица", validators=[DataRequired()])
    district = SelectField("Район", choices=[], validators=[DataRequired()])
    house = StringField("Дом", validators=[DataRequired()])
    front_door = StringField("Подъезд")
    equipment = SelectField("Оборудование", choices=[])
    to_apartment = StringField("Квартиры по ", validators=[DataRequired()])
    from_apartment = StringField("Квартиры с  ", validators=[DataRequired()])
    serial_code = StringField("Серийный номер блока вызова", validators=[DataRequired()])
    tariff = SelectField("Тарифы на обслуживание", choices=[])
    submit = SubmitField("Создать")

    def add_equipment_choices(self):
        """ Добавление выбора в поле Оборудование """
        equip = []
        try:
            equip = db.session.query(EquipmentList).all()
        except Exception as err:
            print(err)

        if equip is not None and len(equip) != 0:
            for eq in equip:
                self.equipment.choices.append((eq.id, eq.name))
        else:
            self.equipment.choices = [('0', 'Empty')]

    def add_tariff_choices(self):
        """ Добавление выбора в поле Тариф """
        tariff = []
        try:
            tariff = db.session.query(Tariff).all()
        except Exception as err:
            print(err)

        if tariff is not None and len(tariff) != 0:
            for el in tariff:
                self.tariff.choices.append((el.id, el.name))
        else:
            self.tariff.choices = [('0', 'Empty')]

    def add_district_choices(self):
        """ Добавление выбора в поле Тариф """
        district = []
        try:
            district = db.session.query(District).all()
        except Exception as err:
            print(err)

        if district is not None and len(district) != 0:
            for el in district:
                self.district.choices.append((el.id, el.name))
        else:
            self.district.choices = [('0', 'Empty')]


class OrganizationChangeIndividualCode(FlaskForm):
    street = StringField("Улица", validators=[DataRequired()])
    district = SelectField("Район", choices=[], validators=[DataRequired()])
    house = StringField("Дом", validators=[DataRequired()])
    front_door = StringField("Подъезд")
    apartment = StringField("Квартира")
    code = StringField("Код", validators=[DataRequired(), Length(min=4, max=10)])
    submit = SubmitField("Сохранить")

    def add_district_choices(self):
        """ Добавление выбора в поле Тариф """
        district = []
        try:
            district = db.session.query(District).all()
        except Exception as err:
            print(err)

        if district is not None and len(district) != 0:
            for el in district:
                self.district.choices.append((el.id, el.name))
        else:
            self.district.choices = [('0', 'Empty')]
