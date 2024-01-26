import string
import random
from models import db, Group, Student, Course
from factory import create_app


# group name randomizer
def generate_group_name(quantity: int) -> list:
    group_name = []
    for i in range(quantity):
        two_letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
        two_numbers = ''.join(random.choice(string.digits) for _ in range(2))
        concatenated = f'{two_letters}-{two_numbers}'
        group_name.append(concatenated)
    return group_name


# create group class instance
def create_groups(names: list) -> list:
    names_container = names
    result = []
    for name in names_container:
        group = Group(name=name)
        result.append(group)
    return result


# add group in to database
def add_group(group_list: list):
    groups = group_list
    for group in groups:
        if not Group.query.count() == 10:
            db.session.add(group)


def create_courses():
    courses = ["Nursing", "Mathematics", "Computer Science",
               "Mechanical Engineering", "Marketing", "Law",
               "Accounting", "Architecture", "Medicine", "Biology"]
    for element in courses:
        if not Course.query.count() == 10:
            insert_data = Course(name=element)
            db.session.add(insert_data)


# student name randomizer
def generate_student_name(quantity: int) -> list:
    first_name = ["Yosemite", "Ito", "Midwestern", "Picasso",
                  "Tutankhamen", "Everglade", "Jove", "Sicily", "Citroen", "Ozark",
                  "Gonzales", "Fallopian", "Gerhard", "Osiris", "Garvey", "Monica",
                  "Paolo", "Kerr", "Cassius", "Annie"]

    last_name = ["Austin", "Montevideo", "Simmons", "Russell",
                 "Eugene", "Vicksburg", "Shaffer", "Actaeon",
                 "Bernardo", "Drexel", "Colby", "Paz",
                 "Mawr", "Hans", "Lancashire", "Otto",
                 "Colloq", "Magog", "Vaughan", "Severn"]

    full_name = []
    for _ in range(quantity):
        full_name.append(f'{random.choice(first_name)} {random.choice(last_name)}')

    return full_name


# create student class instance
def create_students(names: list) -> list:
    names_list = names
    result = []
    for name in names_list:
        split_name = name.split()
        student = Student(first_name=split_name[0], last_name=split_name[1])
        result.append(student)
    return result


# add student in to database
def add_students(students_list: list):
    db.session.add_all(students_list)


def assign_students_to_courses():
    courses_container = Course.query.all()
    students = Student.query.all()
    for student in students:
        for _ in range(random.randint(1, 3)):
            student.course.append(random.choice(courses_container))


def assign_students_to_groups():
    students = Student.query.all()
    groups = Group.query.all()
    for student in students:
        group = random.choice(groups)
        if len(group.student) <= 10 or not len(group.student) == 30:
            student.group_id = group.id


app = create_app('config.Config')


@app.cli.command("create-data")
def create_data():
    add_students(create_students(generate_student_name(200)))
    add_group(create_groups(generate_group_name(10)))
    create_courses()
    assign_students_to_groups()
    assign_students_to_courses()
    db.session.commit()
