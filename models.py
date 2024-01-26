# from factory import db
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

student_course_rel = db.Table('student_course_rel',
                              db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                              db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
                              )


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    student = db.relationship('Student', backref='group')

    def __repr__(self):
        return f'<Group: {self.name}>'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    course = db.relationship('Course', secondary=student_course_rel, backref='student')

    def __repr__(self):
        return f'<Student: {self.first_name} {self.last_name}>'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(50))

    def __repr__(self):
        return f'<Course: {self.name}>'
