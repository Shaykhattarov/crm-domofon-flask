from app import db



class Order(db.Model):
    __tablename__ = "order"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tariff_id = db.Column(db.Integer, db.ForeignKey('tariff.id'))

    def __repr__(self):
        return "<Order {}>".format(self.id)



class OrderPayment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True) 
    date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "<OrderPayment {}>".format(self.id)
    