from app import db



class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"))
    active_sub = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __repr__(self):
        return "<Payment {}>".format(self.id)
    

class ArchivePayment(db.Model):
    __tablename__ = 'archive_payment'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<ArchivePayment {}>".format(self.payment_id)
