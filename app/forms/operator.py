from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length



class OperatorPay(FlaskForm):
    address = StringField("Адрес", validators=[DataRequired()])
    apartment = StringField("Квартира", validators=[DataRequired()])
    amount = StringField("Сумма", validators=[DataRequired(), Length(min=2, max=8)])
    submit = SubmitField("Оплатить")


class MaterReport(FlaskForm):
    application_id = StringField('Номер заявки', validators=[DataRequired()])
    status = StringField('Статус', validators=[DataRequired()])
    master = StringField('Мастер', validators=[DataRequired()])
    addition = StringField('Дополнительно (опишите проблемы и трудности, возникшие во время выполнения заявки)', validators=[DataRequired()])