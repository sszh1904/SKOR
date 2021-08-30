from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_POOL_RECYCLE = int(os.getenv("SQLALCHEMY_POOL_RECYCLE"))
SQLALCHEMY_TRACK_MODIFICATIONS = False if os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == 'False' else True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('skorDB') or 'mysql+mysqlconnector://skor:skorPassword@localhost:3306/skor'
app.config['SQLALCHEMY_POOL_RECYCLE'] = SQLALCHEMY_POOL_RECYCLE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# app.config['SQLALCHEMY_POOL_SIZE'] = 20

db = SQLAlchemy(app)
CORS(app)


class User(db.Model):
    __abstract__ = True

    name = db.Column(db.String(80), nullable=False)
    password= db.Column(db.String(100), nullable=False)
    # actualPassword = db.Column(db.String(100), nullable=False)
    lastLogin = db.Column(db.String(30), nullable=True)
    isLogin = db.Column(db.Integer, nullable=False, server_default='0')

    def json(self):
        return {
            "email": self.email,
            "name":self.name,
            "password":self.password,
            # "actualPassword": self.actualPassword,
            "lastLogin": self.lastLogin,
            "isLogin": self.isLogin
        }

class Admin(User):
    __tablename__ = 'admin'
    email = db.Column(db.String(80), primary_key=True)

class Student(User):
    __tablename__ = 'student'
    email = db.Column(db.String(80), primary_key=True)

class Faculty(User):
    __tablename__ = 'faculty'
    email = db.Column(db.String(80), primary_key=True)

class Instructor(User):
    __tablename__ = 'instructor'
    email = db.Column(db.String(80), primary_key=True)

class Term(db.Model):
    __tablename__ = 'term'
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    startDate= db.Column(db.String(10), nullable=False)
    endDate = db.Column(db.String(10), nullable = False)
    isCurrent = db.Column(db.Integer, server_default="0", nullable=False)

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "startDate":self.startDate,
            "endDate":self.endDate,
            "isCurrent":self.isCurrent
        }

class TATerm(db.Model):
    __tablename__ = 'taTerm'
    email = db.Column(db.String(80), db.ForeignKey('student.email', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['acadYear', 'termNo'],
            ['term.acadYear', 'term.termNo'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        ), {}
    )

    def json(self):
        return {
            "email": self.email,
            "acadYear": self.acadYear,
            "termNo": self.termNo,
        }

class Course(db.Model):
    __tablename__ = 'course'
    courseCode = db.Column(db.String(10), primary_key=True)
    courseName = db.Column(db.String(80), nullable=False)

    def json(self):
        return {
            "courseCode": self.courseCode,
            "courseName":self.courseName
        }

class CourseOffering(db.Model):
    __tablename__ = 'courseOffering'
    acadYear = db.Column(db.String(10), primary_key=True) 
    termNo = db.Column(db.Integer, primary_key=True) 
    courseCode = db.Column(db.String(10), db.ForeignKey('course.courseCode', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['acadYear', 'termNo'],
            ['term.acadYear', 'term.termNo'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        ), {}
    )

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode
        }

class Section(db.Model):
    __tablename__ = 'section'
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    courseCode= db.Column(db.String(10), primary_key=True)
    sectionNo = db.Column(db.Integer, primary_key=True)

    facultyEmail = db.Column(db.String(80), db.ForeignKey('faculty.email', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    instructorEmail = db.Column(db.String(80), db.ForeignKey('instructor.email', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)
    taEmail = db.Column(db.String(80), db.ForeignKey('taTerm.email', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)
    
    day = db.Column(db.String(10), nullable = False)
    startDate = db.Column(db.String(10), nullable = False)
    startTime = db.Column(db.String(10), nullable = False)
    endTime = db.Column(db.String(10), nullable = False)
    participationScoreLimit = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['acadYear', 'termNo', 'courseCode'],
            ['courseOffering.acadYear', 'courseOffering.termNo', 'courseOffering.courseCode'],
            ondelete='CASCADE',
            onupdate='CASCADE'
        ), {}
    )

    def json(self):
        return {
            "acadYear":self.acadYear,
            "termNo":self.termNo,
            "courseCode":self.courseCode,
            "sectionNo":self.sectionNo,
            "facultyEmail":self.facultyEmail,
            "instructorEmail": self.instructorEmail,
            "taEmail":self.taEmail,
            "day":self.day,
            "startDate": self.startDate,
            "startTime": self.startTime,
            "endTime":self.endTime,
            "participationScoreLimit": self.participationScoreLimit
        }

class Enrolment(db.Model):
    __tablename__ = 'enrolment'
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    courseCode= db.Column(db.String(10), primary_key=True)
    sectionNo = db.Column(db.Integer, primary_key=True)
    studentEmail = db.Column(db.String(80), db.ForeignKey('student.email', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['acadYear', 'termNo', 'courseCode', 'sectionNo'],
            ['section.acadYear', 'section.termNo', 'section.courseCode', 'section.sectionNo'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        ), {}
    )

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode,
            "sectionNo": self.sectionNo,
            "studentEmail": self.studentEmail
        }

class PriorityCall(db.Model):
    __tablename__ = 'priorityCall'
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    courseCode= db.Column(db.String(10), primary_key=True)
    sectionNo = db.Column(db.Integer, primary_key=True)
    studentEmail = db.Column(db.String(80), db.ForeignKey('enrolment.studentEmail', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['acadYear', 'termNo', 'courseCode', 'sectionNo'],
            ['section.acadYear', 'section.termNo', 'section.courseCode', 'section.sectionNo'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        ), {}
    )

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode,
            "sectionNo": self.sectionNo,
            "studentEmail": self.studentEmail
        }

class Session(db.Model):
    __tablename__ = 'session'
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    courseCode= db.Column(db.String(10), primary_key=True)
    sectionNo = db.Column(db.Integer, primary_key=True)
    sessNo = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    available = db.Column(db.Integer, server_default="0", nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['acadYear', 'termNo', 'courseCode', 'sectionNo'],
            ['section.acadYear', 'section.termNo', 'section.courseCode', 'section.sectionNo'],
            onupdate="CASCADE",
            ondelete="CASCADE"
        ), {}
    )

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode,
            "sectionNo": self.sectionNo,
            "sessNo": self.sessNo,
            "date": self.date,
            "available": self.available
        }

class Participation(db.Model):
    __tablename__ = 'participation'
    datetime = db.Column(db.String(30), primary_key=True)
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    courseCode= db.Column(db.String(10), primary_key=True)
    sectionNo = db.Column(db.Integer, primary_key=True)
    sessNo = db.Column(db.Integer, primary_key=True)
    studentEmail = db.Column(db.String(80), primary_key=True)
    score = db.Column(db.Integer, nullable=False, server_default="0")
    isAccepted = db.Column(db.Integer, nullable=False, server_default="0")

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode,
            "sectionNo": self.sectionNo,
            "sessNo": self.sessNo,
            "studentEmail": self.studentEmail,
            "datetime": self.datetime,
            "score": self.score,
            "isAccepted": self.isAccepted
        }

class StudentSessionScore(db.Model):
    __tablename__ = 'studentSessionScore'
    acadYear = db.Column(db.String(10), primary_key=True)
    termNo = db.Column(db.Integer, primary_key=True)
    courseCode= db.Column(db.String(10), primary_key=True)
    sectionNo = db.Column(db.Integer, primary_key=True)
    sessNo = db.Column(db.Integer, primary_key=True)
    studentEmail = db.Column(db.String(80), primary_key=True)
    score = db.Column(db.Integer, nullable=False, server_default="0")

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode,
            "sectionNo": self.sectionNo,
            "sessNo": self.sessNo,
            "studentEmail": self.studentEmail,
            "score": self.score
        }

class ParticipationScoreLog(db.Model):
    __tablename__ = 'participationScoreLog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    acadYear = db.Column(db.String(10), nullable=False)
    termNo = db.Column(db.Integer, nullable=False)
    courseCode= db.Column(db.String(10), nullable=False)
    sectionNo = db.Column(db.Integer, nullable=False)
    sessNo = db.Column(db.Integer, nullable=False)
    studentEmail = db.Column(db.String(80), nullable=False)
    logDatetime = db.Column(db.String(30), nullable=False)
    participationRecordDatetime = db.Column(db.String(30), nullable=True)
    action = db.Column(db.Text, nullable=False)
    actionBy = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def json(self):
        return {
            "acadYear": self.acadYear,
            "termNo": self.termNo,
            "courseCode": self.courseCode,
            "sectionNo": self.sectionNo,
            "sessNo": self.sessNo,
            "studentEmail": self.studentEmail,
            "logDatetime": self.logDatetime,
            "participationRecordDatetime": self.participationRecordDatetime,
            "action": self.action,
            "actionBy": self.actionBy,
            "role": self.role
        }

class SkorEmail(db.Model):
    __tablename__ = 'skorEmail'

    email = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(10), nullable=False)
    selected = db.Column(db.Integer, server_default="0", nullable=False)

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "domain": self.domain,
            "selected": self.selected
        }

class Configuration(db.Model):
    __tablename__ = "configuration"

    id = db.Column(db.Integer, primary_key=True)
    testMode = db.Column(db.Integer, nullable=False, server_default="0")

    def json(self):
        return {
            "id": self.id,
            "testMode": self.testMode
        }


db.create_all()

