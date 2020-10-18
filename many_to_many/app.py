from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
import sys

# Start a python shell and follow these steps
from config import app, db
from models import *


# Lets populate our tables
# List of Courses
courses = ['English', 'Math', 'Science']

# List of students
students = ['Ahmed', 'Omar']

for course in courses:
    new_course = Course(course_name=course)
    db.session.add(new_course)
    db.session.commit()

for student in students:
    new_student = Student(student_name=student)
    db.session.add(new_student)
    db.session.commit()


# Lets enroll one of the students to a course
# Lets enroll Ahmed in English

# Getting object Ahmed
x = Student.query.filter_by(student_name="Ahmed").one()
# Lets print the result of our query
# You may need to to implement __repr__ in the class to view 
# it in details but there is always a workaround

print(x.id)
print(x.student_name)
print(x.__dict__)


# Now that we have the object Ahmed, lets get the object English and print the result of the query
y = Course.query.filter_by(course_name="English").one()
print(y.id)
print(y.course_name)
print(y.__dict__)



# We now have both student and class and we need to enroll them using the association class
# Below are a few methods as to how we can create this relationship
new_enrollment = Enrollment(student_id=x.id, course_id=y.id)
db.session.add(new_enrollment)
db.session.commit()

# What happened here is that I enrolled Ahmed in the course of English, lets enroll him in another course, Math
z = Course.query.filter_by(course_name="Math").one()
print(z.id)
print(z.course_name)
print(z.__dict__)

# We still have object Ahmed stored on variable x, ergo we still have his id
new_math_enrollment = Enrollment(student_id=x.id, course_id=z.id)
db.session.add(new_math_enrollment)
db.session.commit()


# Lets query and check all the courses Ahmed is enrolled in:
# Since we added a backref in the student model (classes) line 9,
# we can get through this attribute all the classes Ahmed is enrolled in
# If we print x.courses where x is the variable holding the object Ahmed, we'd know more about it

print(x.courses)

# The return for this print statement is expected to be the two course objects, Ahmed has been enrolled in
# Lets now create an object containing the following data about Ahmed:
# his name, number of courses he's enrolled in and these courses names

data = {}

x = Student.query.filter_by(student_name="Ahmed").one()

data['student_name'] = x.student_name
data['student_id'] = x.id
data['number_of_courses'] = len(x.courses)
data['courses'] = []
for enrolled in x.courses:
    # Since I'm looping over enrollment objects, I have access to their attributes.
    # I'm interested in the course name. How would I get that?
    # I notice that the enrollment object has an attribute 'course' which refers to the associated Course object, which in turn
    # has the attribute course_name
    data['courses'].append(enrolled.course.course_name)


print(data)



# Lets say I want to test the backref of the course and view all students enrolled in a certain class, English for example
y = Course.query.filter_by(course_name='English').one()
print(y.students)

# You dont really need to have backref everywhere, but having them gives you more flexibility and options in accessing 
# associated objects