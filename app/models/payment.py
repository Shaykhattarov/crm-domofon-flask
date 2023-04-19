from app import db



class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"))
    active_payment = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return "<Payment {}>".format(self.active_payment)
    
