from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length


class UserLogin(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired(), Length(min=2, max=25)])
    email = EmailField('Введите email', validators=[DataRequired(), Length(min=5, max=2100)])
    submit = SubmitField('продолжить')


class UserRegistration(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Введите email', validators=[DataRequired(), Length(min=5, max=2100)])
    phone = StringField('Введите телефон', validators=[DataRequired(), Length(min=2, max=25)])
    street = StringField("Введите улицу", validators=[DataRequired(), Length(max=300)])
    district = StringField("Введите район", choices=[], validators=[DataRequired(), Length(max=300)])
    house = StringField("Введите дом", validators=[DataRequired(), Length(max=50)])
    front_door = StringField("Введите подъезд", validators=[DataRequired(), Length(max=50)])
    apartment = StringField("Введите квартиру", validators=[DataRequired(), Length(max=10)])
    recaptcha = RecaptchaField()
    submit = SubmitField('продолжить')

    def add_district_choices(self):
        """ Заполнение подсказок по районам """
        pass