from datetime import datetime
from flasklrc import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_student(gnumber):
    return Students.query.get(int(gnumber))


class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    gnumber = db.Column(db.String(9), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'stud_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            stud_id = s.loads(token)['stud_id']
        except:
            return None
        return Students.query.get(stud_id)

    def __repr__(self):
        return f"Students('{self.gnumber}', '{self.name}','{self.email}','{self.image_file}')"




class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.Integer, unique=True, nullable=False )
    publisher = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Books('{self.name}','{self.publisher}','{self.name}')"


class New_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.Integer, nullable=False)
    gnumber = db.Column(db.String(9), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_returned = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}','{self.ISBN}','{self.gnumber}')"


class Old_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.Integer, nullable=False)
    gnumber = db.Column(db.String(9), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_returned = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}','{self.ISBN}','{self.gnumber}')"
