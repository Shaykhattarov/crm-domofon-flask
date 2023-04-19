from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class OrganizationCreateAddress(FlaskForm):
    address = StringField("Адрес", validators=[DataRequired()])
    front_door = StringField("Подъезд", validators=[DataRequired()])
    equipment = SelectField("Оборудование", coerce=False)
    serial_code = StringField("Серийный номер блока вызова", validators=[DataRequired()])
    tariff = SelectField("Тарифы на обслуживание", coerce=False)
    submit = SubmitField("Создать")

    def add_equipment_choices():
        pass

    def add_tariff_choices():
        pass


