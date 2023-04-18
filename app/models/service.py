from app import db


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    tariff_id = db.Column(db.Integer, db.ForeignKey('tariff.id'))

    def __repr__(self):
        return "<Service {}>".format(self.id)