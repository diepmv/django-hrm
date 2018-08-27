# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from sqlalchemy import Table, Column, Integer, Numeric, String, DateTime
from django.contrib.auth.hashers import check_password
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from django.db import models
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime



# Create your models here.



engine = create_engine('mysql+pymysql://root:maivandiep@127.0.0.1/hrm?charset=utf8')
# engine = create_engine('mysql+pymysql://root:my-secret-pw@localhost/hrm')


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()



# skill_employee_association = Table('employee_skill', Base.metadata,
#                                    Column("id", Integer, primary_key=True),
#                                    Column("skill_id", Integer, ForeignKey("skill.id")),
#                                     Column("empoyee_id", Integer, ForeignKey("employee.id")),
#                                    Column("start_date", Date),
#                                    Column("end_date", Date)
#                                    )

class EmployeeSkillLink(Base):
    __tablename__ = "employee_skill"
    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    start_date = Column(Date())
    end_date = Column(Date())
    employee = relationship("Employee", backref="skill_assoc")
    skill = relationship("Skill", backref="employee_assoc")


# employee_relationship_association = Table("employee_relationship", Base.metadata,
#                                           Column("id", Integer, primary_key=True),
#                                           Column("employee_id", Integer, ForeignKey("employee.id")),
#                                           Column("relationship_id", Integer, ForeignKey("relationship.id")),
#                                           Column("name", String(100))
#                                           )

class EmployeeRelationshipLink(Base):
    __tablename__ = "employee_relationship"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    relationship_id = Column(Integer, ForeignKey("relationship.id"))
    name = Column(String(100))
    employee = relationship("Employee", backref = "relationship_assoc")
    relationship = relationship("Relationship", backref="employee_assoc")




# employee_school_association = Table("employee_school", Base.metadata,
#                                     Column("id", Integer, primary_key=True),
#                                     Column("employee_id", Integer, ForeignKey("employee.id")),
#                                     Column("school_id", Integer, ForeignKey("school.id")),
#                                     Column("degree_type", String(100)),
#                                     Column("start_date", Date()),
#                                     Column("end_date", Date())
#                                     )


class EmployeeSchoolLink(Base):
    __tablename__ = "employee_school"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    school_id = Column(Integer, ForeignKey("school.id"))
    degree_type = Column(String(100))
    start_date = Column(Date())
    end_date = Column(Date())
    employee = relationship("Employee", backref="school_assoc")
    school = relationship("School", backref="employee_assoc")




# class ExampleModel(models.Model):
#     model_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    type = Column(String(70))
    path  = Column(Text(), default='avatar.png')
    employee = relationship("Employee",uselist=False ,back_populates="image")




class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer(), primary_key=True)
    subject = Column(String(100))
    content = Column(Text())


class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer(), primary_key=True)
    message_id = Column(Integer(), ForeignKey('message.id'))
    message = relationship('Message')
    user_id = Column(Integer(), ForeignKey('employee.id'))
    seen = Column(Boolean(), default=False)



class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer(), primary_key=True)
    is_superuser = Column(Boolean())
    is_active = Column(Boolean())
    name = Column(String(100), index=True)
    gender = Column(String(1))
    dob = Column(Date())
    pos_id = Column(Integer(), ForeignKey('position.id'))
    parent = Column(Integer(),ForeignKey('employee.id'))

    username = Column(String(50), unique=True)
    password = Column(String(100))

    email = Column(String(255))
    image_id = Column(Integer(), ForeignKey('image.id'))
    image = relationship('Image', back_populates="employee")

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    deleted_on = Column(DateTime(), default=None)
    # bio = Column(Text())
    bio = Column(Unicode(100, collation="utf8_bin"))

    document = relationship("Document", back_populates = "employee")

    skills = relationship("Skill", secondary = "employee_skill", back_populates="employees")

    relationships = relationship("Relationship", secondary = "employee_relationship", back_populates="employees")
    schools = relationship("School", secondary = "employee_school", back_populates="employees")



    def get_object(self, queryset=None):
        obj = session.query(Employee, pk=self.kwargs['staff_id']).first()
        return obj

    @property
    def get_children(self):
        return session.query(Employee).filter_by(parent = self.id)


    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def has_profile_picture(self):
        return self.image_id
#
# class Skill(Base):
#     __tablename__ = "skill"
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(30))
#
# class Employee_Skill(Base):
#     __tablename__ = "emp_skill"
#     emp_id = Column(Integer(), ForeignKey('employee.id'))
#     skill_id = Column(Integer(), ForeignKey('skill.id'))
#     start_date = Column(Date())
#     end_date = Column(Date())



class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer(), primary_key=True)

    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship("Employee", back_populates = "document")

    name = Column(String(100))
    type = Column(String(300))
    path = Column(Text(), default='')
    def is_image(self):
        return self.type[0:5] == "image" and self.name != "pdf.png" and self.name != "doc.jpg"

    def is_pdf(self):
        return self.type == "application/pdf"

    def is_doc(self):
        return self.type == "application/msword"


class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    employees = relationship("Employee", secondary="employee_skill", back_populates = "skills")




class Relationship(Base):
    __tablename__ = "relationship"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))
    employees = relationship("Employee", secondary = "employee_relationship", back_populates="relationships")



class School(Base):
    __tablename__ = "school"
    id = Column(Integer(), primary_key=True)
    name = Column(Unicode(100, collation="utf8_bin"))
    address = Column(Unicode(300, collation="utf8_bin"))
    employees = relationship("Employee", secondary="employee_school", back_populates="schools")




class ResetPassword(Base):
    __tablename__ = 'resetpassword'
    id = Column(Integer(),primary_key=True)
    email = Column(String(255))
    token = Column(Text())
    reset_on = Column(DateTime(), default=datetime.now)

class CreateNewUser(Base):
    __tablename__ = 'createnewuser'
    id = Column(Integer(), primary_key=True)
    email = Column(String(255))
    token = Column(Text())
    created_on = Column(DateTime(), default=datetime.now)


Base.metadata.create_all(engine)



