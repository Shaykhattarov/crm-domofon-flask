from app import db



class UserAddress(db.Model):
    __tabelname__ = "user_address"

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    apartment = db.Column(db.String(200))
    
    def __repr__(self):
        return '<UserAddress {}>'.format(self.street)
    


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(2000), nullable=False)
    house = db.Column(db.String(200), nullable=False)
    front_door = db.Column(db.String(200))
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"))
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"))
    individual_code = db.Column(db.String(16))

    def __repr__(self):
        return "<Address> {}".format(self.street)