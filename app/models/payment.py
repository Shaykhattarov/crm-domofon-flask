from app import db



class Subscription(db.Model):
    __tablename__ = "subscription"

    id = db.Column(db.Integer, primary_key=True)
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"), nullable=False)
    active = db.Column(db.Integer, default=0, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    def __repr__(self):
        return "<Subscription {} - {}>".format(self.id, self.active)



class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscription.id"))
    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.Date, nullable=False)
    option = db.Column(db.String(200))
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Payment {} - {}>".format(self.subscription_id, self.id)
    

    
