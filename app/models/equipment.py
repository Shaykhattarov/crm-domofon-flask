from app import db



class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    serial_code = db.Column(db.String(1000))

    def __repr__(self):
        return "<Equipment {}>".format(self.name)