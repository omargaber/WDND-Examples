from config import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(), nullable=False)
    # We can add an attribute here to be able to
    # refer to the associated courses for the students using backref
    courses = db.relationship("Enrollment", backref="classes")

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(), nullable=False)
    students = db.relationship("Enrollment", backref="student_list")


# Association Table or the table/model that maps the many to many relationship
# COULD ALSO BE IMPLEMENTED AS A TABLE RATHER THAN AN OBJECT
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course = db.relationship("Course", backref="students_enrolled")
    student = db.relationship("Student", backref="classes_enrolled")
