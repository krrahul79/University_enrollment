from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    enrollment = db.relationship('Enrollment', backref='user', lazy=True)
    def __repr__(self):
        return f"User('{self.user_id}', '{self.first_name}', '{self.last_name}')"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password, password)
    

class Course(db.Model):
    course_id = db.Column(db.String(10), unique = True, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    credits = db.Column(db.Integer)
    term = db.Column(db.String(25))
    enrollment = db.relationship('Enrollment', backref='course', lazy=True)


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'), nullable=False)
    course_id = db.Column(db.String(10),db.ForeignKey('course.course_id'), nullable=False)

    def __repr__(self):
        return f"Enrollment('{self.id}', '{self.user_id}', '{self.course_id}')"

