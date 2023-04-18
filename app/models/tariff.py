from app import db



class Tariff(db.Model):
    __tablename__ = "tariff"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Tariff {}>".format(self.name)
