from app import db



class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('application_status.id'))
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    image = db.Column(db.String(300), nullable=False)
    problem = db.Column(db.String(3000), nullable=False)

    def __repr__(self):
        return f"<Application {self.id}>"
    


class ApplicationReport(db.Model):
    __tablename__ = "application_report"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("application.id"), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    addition = db.Column(db.String(3000), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<ApplicationReport {self.id} - {self.application_id}>"



class ApplicationStatus(db.Model):
    __tablename__ = "application_status"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<ApplicationStatus {self.id} - {self.value}>"
    
    




