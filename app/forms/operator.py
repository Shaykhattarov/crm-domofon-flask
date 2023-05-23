from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from app.models import Tariff, User, Application, ApplicationStatus, District
from app import db




class OperatorPay(FlaskForm):
    street = StringField('Улица', validators=[DataRequired()])
    front_door = StringField('Подъезд', validators=[])
    house = StringField('Дом', validators=[DataRequired()])
    district = SelectField('Район', choices=[], validators=[DataRequired()])
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



class CreateApplicationForm(FlaskForm):
    date = StringField('', validators=[DataRequired()])
    street = StringField('Улица', validators=[DataRequired()])
    front_door = StringField('Подъезд', validators=[])
    house = StringField('Дом', validators=[DataRequired()])
    district = SelectField('Район', choices=[], validators=[DataRequired()])
    apartment = StringField("Квартира", validators=[DataRequired()])
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



class CreateMasterReportForm(FlaskForm):
    date = StringField('', validators=[DataRequired()])
    number = SelectField('Номер заявки', choices=[], validators=[DataRequired()])
    status = SelectField('Статус', choices=[], validators=[DataRequired()])
    master = SelectField('Мастер', choices=[], validators=[DataRequired()])
    addition = StringField("Дополнительно (опишите проблемы и трудности, возникшие во время выполнения заявки)", validators=[DataRequired()])
    image = StringField('Изображение', validators=[DataRequired()])
    submit = SubmitField("Создать")

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


class ViewReportMasterForm(FlaskForm):
    master = SelectField('Мастер', choices=[], validators=[DataRequired()])
    from_date = StringField('', validators=[DataRequired()])
    to_date = StringField('', validators=[DataRequired()])
    submit = SubmitField('Вывести отчет')

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


class ViewReportApplicationForm(FlaskForm):
    street = StringField('Улица', validators=[DataRequired()])
    front_door = StringField('Подъезд', validators=[])
    house = StringField('Дом', validators=[DataRequired()])
    district = SelectField('Район', choices=[], validators=[DataRequired()])
    apartment = StringField("Квартира", validators=[DataRequired()])
    from_date = StringField("", validators=[DataRequired()])
    to_date = StringField('', validators=[DataRequired()])
    submit = SubmitField('Вывести отчёт')

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

