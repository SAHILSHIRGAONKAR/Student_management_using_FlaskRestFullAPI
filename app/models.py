from .database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    standard_id = db.Column(db.Integer, db.ForeignKey('standard.id'))
    city = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(10))
    marks = db.relationship('Mark', backref='student', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    marks = db.relationship('Mark', backref='subject', lazy=True)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    marks_obtained = db.Column(db.Integer)  # Changed to marks_obtained

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subjects_taught = db.relationship('Subject', backref='teacher', lazy=True)
    standards_taught = db.relationship('Standard', backref='teacher', lazy=True)

class Standard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    students = db.relationship('Student', backref='standard', lazy=True)

