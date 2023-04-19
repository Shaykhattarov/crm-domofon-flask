from app import db



class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment_list.id"))
    serial_code = db.Column(db.String(1000))

    def __repr__(self):
        return "<Equipment {}>".format(self.name)
    

class EquipmentList(db.Model):
    __tablename__ = "equipment_list"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))

    def __repr__(self):
        return "<EquipmentList {}>".format(self.name)