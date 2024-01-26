import click
from crud_and_special import *
from factory import create_app

app = create_app('config.Config')


@app.cli.command('q_groups_by_count')
@click.argument('count')
def q_groups_by_count(count):
    groups = Group.query.join(Student).group_by(Group.id).having(db.func.count(Student.id) <= int(count)).all()
    for group in groups:
        print(f"Group {group.name}, have {len(group.student)} students.")


@app.cli.command('q_students_by_course')
@click.argument('course')
def q_students_by_course(course):
    students = find_students_by_course(course)
    print(f'Studying on {course} course:')
    for student in students:
        print(f"{student.first_name} {student.last_name}.")


@app.cli.command('q_add_student')
@click.argument('name')
def q_add_student(name):
    student = add_student(name)
    print(student_info(student.id))


@app.cli.command('q_delete_student_byid')
@click.argument('student_id')
def q_delete_student_byid(student_id):
    delete_student(student_id)
    student = db.session.query(Student).filter_by(id=student_id).first()
    if not student:
        print('Student with that id deleted.')


@app.cli.command('q_add_student_to_course')
@click.argument('course')
def q_add_student_to_course(course):
    students_list = student_list_from_database(3)
    dedicated_course = Course.query.filter_by(name=course).first()
    add_students_to_course(course, students_list)
    for student in students_list:
        if dedicated_course in student.course:
            print(f'Student {student.first_name} {student.last_name} added to {course}, course.')
        else:
            print(f'Student {student.first_name} {student.last_name} not added to {course}, course.')


@app.cli.command('q_remove_student_from_course')
@click.argument('student_name')
def q_remove_student_from_course(student_name):
    removed_course = remove_student_from_course(student_name)
    print(f'Student {student_name}, was removed from {removed_course} course.')
