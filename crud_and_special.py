from flask import current_app
from flask_restful import abort
from models import *
import random
import xml.etree.ElementTree as ET


# basic CRUD
# READ
def students_info():
    students = Student.query.all()
    result = {}
    for student in students:
        student_courses = [course.name for course in student.course]
        result[student.id] = {
            "First_name": student.first_name,
            "Last_name": student.last_name,
            "Courses": student_courses,
            "Group_id": student.group_id
        }
    return result


def student_info(student_id: int):
    student = db.session.query(Student).filter_by(id=student_id).first()
    student_courses = [course.name for course in student.course]
    return {
        "Id": student.id,
        "First_name": student.first_name,
        "Last_name": student.last_name,
        "Courses": student_courses,
        "Group_id": student.group_id
    }


def groups_info():
    groups = Group.query.all()
    result = {}
    for group in groups:
        students = [f"{student.first_name} {student.last_name}" for student in group.student]
        result[group.id] = {
            "name": group.name,
            "students": students
        }
    return result


def group_info(group_id: int):
    group = db.session.query(Group).filter_by(id=group_id).first()
    students = [f"{student.first_name} {student.last_name}" for student in group.student]
    return {
        "name": group.name,
        "students": students
    }


def find_group_by_count(count):
    groups = Group.query.join(Student).group_by(Group.id).having(db.func.count(Student.id) <= int(count)).all()
    return groups


def find_students_by_course(course: str) -> list:
    return Student.query.join(Student.course).filter(Course.name == course).all()


def student_list_from_database(quantity: int) -> list:
    result = []
    students = Student.query.all()
    for student in range(quantity):
        result.append(random.choice(students))
    return result


def group_name(group_id: int = None):
    group = Group.query.filter_by(id=group_id).first()
    return group.name


# UPDATE
def edit_student(student_id: int, data: dict):
    student = Student.query.filter_by(id=student_id).first()
    student.group_id = data["group_id"]
    student.first_name = data["first_name"]
    student.last_name = data["last_name"]
    if data["course"]:
        course = Course.query.filter_by(name=data["course"]).first()
        student.course.append(course)
    db.session.commit()
    return Student.query.filter_by(id=student_id).first()


def edit_group(group_id: int, data: dict):
    group = Group.query.filter_by(id=group_id).first()
    group.name = data["name"]
    if data["student"]:
        split_name = data["student"].split(' ')
        student = Student.query.filter(Student.first_name == split_name[0], Student.last_name == split_name[1]).first()
        group.student.append(student)
    db.session.commit()
    return group


def edit_course(course_id: int, data: dict):
    course = Course.query.filter_by(id=course_id).first()
    course.name = data["name"]
    course.description = data["description"]
    db.session.commit()
    return Course.query.filter_by(id=course_id).first()


def add_students_to_course(course_name: str, students_list: list):
    course = Course.query.filter_by(name=course_name).first()
    students = students_list
    for student in students:
        student.course.append(course)
    db.session.commit()


def add_student_to_course(course_id: id, student_id: int):
    course = Course.query.filter_by(id=course_id).first()
    student = Student.query.filter_by(id=student_id).first()
    student.course.append(course)
    db.session.commit()
    return student


def remove_student_from_course(course_id: int, student_id: int):
    course = db.session.query(Course).filter_by(id=course_id).first()
    student = db.session.query(Student).filter_by(id=student_id).first()

    removed_course = student.course.pop()
    return removed_course


# CREATE
def add_student(student_name: str):
    name = student_name
    first_name, last_name = name.split(' ')
    insert_data = Student(first_name=first_name, last_name=last_name)
    db.session.add(insert_data)
    db.session.commit()
    return insert_data


def add_group(group_name: str):
    insert_data = Group(name=group_name)
    db.session.add(insert_data)
    db.session.commit()
    return insert_data


def add_course(course_name: str, description: str = None):
    insert_data = Course(name=course_name, description=description)
    db.session.add(insert_data)
    db.session.commit()
    return insert_data


# DELETE
def delete_student(student_id: int):
    student = Student.query.filter_by(id=student_id).first()
    db.session.delete(student)
    db.session.commit()


def delete_group(group_id: int):
    group = Group.query.filter_by(id=group_id).one()
    db.session.delete(group)
    db.session.commit()


def delete_course(course_id: int):
    db.session.query(student_course_rel).filter_by(course_id=course_id).delete()
    db.session.commit()
    db.session.query(Course).filter_by(id=course_id).delete()
    db.session.commit()


# special
def xml_format_students(data: list):
    root = ET.Element("students")
    for el in data:
        student = ET.SubElement(root, 'student')
        student_id = ET.SubElement(student, 'id')
        group_id = ET.SubElement(student, 'group_id')
        first_name = ET.SubElement(student, 'first_name')
        last_name = ET.SubElement(student, 'last_name')
        course = ET.SubElement(student, 'course')

        student_id.attrib = {"student": str(el.id)}
        student_id.text = str(el.id)
        group_id.text = str(el.group_id)
        first_name.text = el.first_name
        last_name.text = el.last_name
        course_names = [c.name for c in el.course]
        course_str = ', '.join(course_names)
        course.text = course_str

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


def xml_format_student(data):
    el = data
    root = ET.Element("student")
    student_id = ET.SubElement(root, 'id')
    group_id = ET.SubElement(root, 'group_id')
    first_name = ET.SubElement(root, 'first_name')
    last_name = ET.SubElement(root, 'last_name')
    course = ET.SubElement(root, 'course')

    student_id.text = str(el.id)
    group_id.text = str(el.group_id)
    first_name.text = el.first_name
    last_name.text = el.last_name
    course_names = [c.name for c in el.course]
    course_str = ', '.join(course_names)
    course.text = course_str

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


def xml_format_groups(data: list):
    root = ET.Element("groups")
    for el in data:
        group = ET.SubElement(root, 'group')
        group_id = ET.SubElement(group, 'id')
        name = ET.SubElement(group, 'name')
        student = ET.SubElement(group, 'student')

        group_id.attrib = {"group": str(el.id)}
        group_id.text = str(el.id)
        name.text = el.name
        students = [f"{s.first_name} {s.last_name}" for s in el.student]
        student_str = ', '.join(students)
        student.text = student_str

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


def xml_format_group(data):
    el = data
    root = ET.Element("group")
    group_id = ET.SubElement(root, 'id')
    name = ET.SubElement(root, 'name')
    student = ET.SubElement(root, 'student')

    root.attrib = {}
    group_id.text = str(el.id)
    name.text = el.name
    students = [f"{s.first_name} {s.last_name}" for s in el.student]
    student_str = ', '.join(students)
    student.text = student_str

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


def xml_format_courses(data: list):
    root = ET.Element("courses")
    for el in data:
        course = ET.SubElement(root, 'course')
        course_id = ET.SubElement(course, 'id')
        name = ET.SubElement(course, 'name')
        description = ET.SubElement(course, 'description')

        course.attrib = {"group": str(el.id)}
        course_id.text = str(el.id)
        name.text = el.name
        description.text = el.description

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


def xml_format_course(data):
    el = data
    root = ET.Element("courses")
    course_id = ET.SubElement(root, 'id')
    name = ET.SubElement(root, 'name')
    description = ET.SubElement(root, 'description')

    root.attrib = {}
    course_id.text = str(el.id)
    name.text = el.name
    description.text = el.description

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


def xml_format_course_students(data):
    el = data
    root = ET.Element("students")
    students = ET.SubElement(root, 'students')
    total = ET.SubElement(root, 'total')

    root.attrib = {}
    students_list = [f'{s.first_name} {s.last_name}' for s in el.student]
    student_str = ', '.join(students_list)
    students.text = student_str
    total.text = str(len(el.student))

    return current_app.response_class(ET.tostring(root), mimetype='application/xml')


# validators

def abort_if_student_doesnt_exist(student_id: int):
    # students = Student.query.all()
    student = db.session.query(Student).filter_by(id=student_id).first()
    if student is None:
        abort(404, message=f"Student doesn't exist")


def abort_if_student_exist(student_name: str):
    name = student_name
    first_name, last_name = name.split(' ')
    students = Student.query.all()
    student = db.session.query(Student).filter(Student.first_name == first_name, Student.last_name == last_name).first()
    if student in students:
        abort(404, message=f"Student {student.first_name} {student.last_name}, already exist.")


def abort_if_group_doesnt_exist(group_id: int):
    groups = Group.query.all()
    group = db.session.query(Group).filter_by(id=group_id).first()
    if group not in groups:
        abort(404, message=f"Group doesn't exist")


def abort_if_group_exist(group_name: str):
    groups = Group.query.all()
    group = db.session.query(Group).filter_by(name=group_name).first()
    if group in groups:
        abort(404, message=f"Group {group.name}, already exist.")


def abort_if_course_doesnt_exist(course_id: int):
    courses = Course.query.all()
    course = db.session.query(Course).filter_by(id=course_id).first()
    if course not in courses:
        abort(404, message=f"Course doesn't exist")


def abort_if_course_exist(course_name: str):
    courses = Course.query.all()
    course = db.session.query(Course).filter_by(name=course_name).first()
    if course in courses:
        abort(404, message=f"Course {course.name}, already exist.")


def validate_record_existence(model, record_id: int, exists: bool = True, error_message: str = None):
    """
    Validates if a record with the given ID exists or doesn't exist in the database.
    :param model: SQLAlchemy model class for the record.
    :param record_id: ID of the record to check.
    :param exists: If True, checks if the record exists. If False, checks if the record doesn't exist.
    :param error_message: Custom error message to display if the record existence check fails.
    """
    record = model.query.get(record_id)
    if exists:
        if record is None:
            error_message = error_message or f"Record with ID {record_id} doesn't exist"
            abort(404, message=error_message)
    else:
        if record is not None:
            error_message = error_message or f"Record with ID {record_id} already exists"
            abort(409, message=error_message)
