from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length



class OperatorPay(FlaskForm):
    address = StringField("Адрес", validators=[DataRequired()])
    apartment = StringField("Квартира", validators=[DataRequired()])
    amount = StringField("Сумма", validators=[DataRequired(), Length(min=2, max=8)])
    submit = SubmitField("Оплатить")