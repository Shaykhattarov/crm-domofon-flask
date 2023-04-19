from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length


class UserLogin(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired(), Length(min=2, max=25)])
    email = EmailField('Введите email', validators=[DataRequired(), Length(min=5, max=2100)])
    submit = SubmitField('продолжить')


class UserRegistration(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired(), Length(min=2, max=25)])
    email = EmailField('Введите email', validators=[DataRequired(), Length(min=5, max=2100)])
    phone = StringField('Введите телефон', validators=[DataRequired(), Length(min=2, max=25)])
    address = StringField('Введите адрес', validators=[DataRequired(), Length(min=2, max=25)])
    recaptcha = RecaptchaField()
    submit = SubmitField('продолжить')