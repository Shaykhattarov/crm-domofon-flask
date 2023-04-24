from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from app.models import Tariff, User, Application, ApplicationStatus
from common.address import generate_address_help_list
from app import db




class OperatorPay(FlaskForm):
    address = StringField("Адрес", validators=[DataRequired()])
    apartment = StringField("Квартира", validators=[DataRequired()])
    tariff = SelectField("Тариф", choices=[], validators=[DataRequired()])
    amount = StringField("Сумма", validators=[DataRequired(), Length(min=2, max=8)])
    submit = SubmitField("Оплатить")

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



class CreateApplicationForm(FlaskForm):
    date = StringField('', validators=[DataRequired()])
    address = SelectField('Адрес', choices=[], validators=[DataRequired()])
    apartment = StringField('Квартира', validators=[DataRequired()])
    master = SelectField('Мастер', choices=[], validators=[DataRequired()])
    problem = StringField('Проблема', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField("Создать")

    def add_master_choices(self):
        """ Добавление мастеров в поле """
        masters = []
        try:
            masters = db.session.query(User).filter_by(role_id=4).all()
        except Exception as err:
            print(err)

        if masters is not None and len(masters) != 0:
            for master in masters:
                self.master.choices.append((master.id, f"{master.name} - {master.phone}"))
        else:
            self.master.choices = [(0, 'Empty')]


    def add_address_choices(self):
        """ Добавление мастеров в поле """
        addresses = []
        try:
            addresses = generate_address_help_list()
        except Exception as err:
            print(err)

        if addresses is not None and len(addresses) != 0:
            for address in addresses:
                self.address.choices.append((address[0], f"{address[1]}"))
        else:
            self.address.choices = [(0, 'Empty')]


class ChangeApplicationForm(FlaskForm):
    number = SelectField('Номер заявки', choices=[], validators=[DataRequired()])
    date = StringField('', validators=[DataRequired()])
    status = SelectField('Статус', choices=[], validators=[DataRequired()])
    problem = StringField('Проблема (опишите проблемы и трудности, возникшие во время выполнения заявки)', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField("Изменить")

    def add_application_choices(self):
        """ Добавление мастеров в поле """
        apps = []
        try:
            apps = db.session.query(Application).all()
        except Exception as err:
            print(err)

        if apps is not None and len(apps) != 0:
            for app in apps:
                self.number.choices.append((app.id, f"{app.id}"))
        else:
            self.number.choices = [(0, 'Empty')]

        return self.number.choices

    def add_status_choices(self):
        """ Добавление мастеров в поле """
        stats = []
        try:
            stats = db.session.query(ApplicationStatus).all()
        except Exception as err:
            print(err)

        if stats is not None and len(stats) != 0:
            for stat in stats:
                self.status.choices.append((stat.id, f"{stat.value}"))
        else:
            self.status.choices = [(0, 'Empty')]

    


class CreateApplicationReportForm(FlaskForm):
    date = StringField('', validators=[DataRequired()])
    application = SelectField('Номер заявки', choices=[], validators=[DataRequired()])
    status = SelectField('Статус', choices=[], validators=[DataRequired()])
    master = SelectField('Мастер', choices=[], validators=[DataRequired()])
    addition = StringField("Дополнительно (опишите проблемы и трудности, возникшие во время выполнения заявки)", validators=[DataRequired()])
    image = StringField('Изображение', validators=[DataRequired()])