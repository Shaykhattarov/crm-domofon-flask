from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.models import District
from app import db


class UserLogin(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired(), Length(min=2, max=25)])
    email = EmailField('Введите email', validators=[DataRequired(), Length(min=5, max=2100)])
    submit = SubmitField('продолжить')


class UserRegistration(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Введите email', validators=[DataRequired(), Length(min=5, max=2100)])
    phone = StringField('Введите телефон', validators=[DataRequired(), Length(min=2, max=25)])
    street = StringField("Введите улицу", validators=[DataRequired(), Length(max=300)])
    district = SelectField("Выберите район", choices=[], validators=[DataRequired()])
    house = StringField("Введите дом", validators=[DataRequired(), Length(max=50)])
    front_door = StringField("Введите подъезд", validators=[DataRequired(), Length(max=50)])
    apartment = StringField("Введите квартиру", validators=[DataRequired(), Length(max=10)])
    recaptcha = RecaptchaField()
    submit = SubmitField('продолжить')


    def add_district_choices(self):
        """ Добавление выбора в поле Тариф """
        district = []
        try:
            district = db.session.query(District).all()
        except Exception as err:
            print(err)

        if district is not None and len(district) != 0:
            self.district.choices.append((0, 'Выберите район'))
            for el in district:
                self.district.choices.append((el.id, el.name))
        else:
            self.district.choices = [('0', 'Empty')]