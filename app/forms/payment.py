from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClientPaymentForm(FlaskForm):
    number = StringField("Номер карты", validators=[DataRequired(), Length(min=20, max=20)])
    period = StringField("Срок действия карты", validators=[DataRequired(), Length(min=5, max=5)])
    cvv = StringField("CVV", validators=[DataRequired(), Length(min=3, max=3)])
    name = StringField("Имя на карте", validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField('Оплатить')