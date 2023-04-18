from app import db



class UserAddress(db.Model):
    __tabelname__ = "user_address"

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(2000), nullable=False)
    house = db.Column(db.String(200), nullable=False)
    building = db.Column(db.String(200))
    front_door = db.Column(db.String(200))
    apartment = db.Column(db.String(200))
    individual_code = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<UserAddress {}>'.format(self.street)
    


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(2000), nullable=False)
    house = db.Column(db.String(200), nullable=False)
    building = db.Column(db.String(200))
    front_door = db.Column(db.String(200))

    def __repr__(self):
        return "<Address> {}".format(self.street)