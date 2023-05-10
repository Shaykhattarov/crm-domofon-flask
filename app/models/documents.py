from app import db


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3000), nullable=False)
    name_on_server = db.Column(db.String(3000), nullable=False)

    def __repr__(self):
        return f"<Document {self.name}>"