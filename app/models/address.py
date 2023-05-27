from app import db    


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(2000), nullable=False)
    house = db.Column(db.String(200), nullable=False)
    front_door = db.Column(db.String(200), nullable=False)
    apartment = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Integer)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    tariff_id = db.Column(db.Integer, db.ForeignKey('tariff.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))

    def __repr__(self):
        return "<Address> {}".format(self.street)
    

class District(db.Model):
    __tablename__ = "district"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Disrtict {self.name}>'