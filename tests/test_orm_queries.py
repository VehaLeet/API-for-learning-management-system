import random
import pytest
import models
from crud_and_special import *

# Find all groups with less or equals student count.
# Find all students related to the course with a given name.
# Add new student
# Delete student by STUDENT_ID
# Add a student to the course (from a list)
# Remove the student from one of his or her courses


@pytest.mark.parametrize('test_input, expected',
                         [(16, 3)])
def test_read_group_by_count(test_input, expected, client, app):
    assert len(find_group_by_count(test_input)) == expected


@pytest.mark.parametrize('test_input, expected',
                         [('Law', 29)])
def test_read_group_by_course(test_input, expected, client, app):
    assert len(find_students_by_course(str(test_input))) == expected


@pytest.mark.parametrize('test_input, expected',
                         [('Barnacle Boi', 'Barnacle Boi')])
def test_add_student(test_input, expected, client, app):
    student = add_student(test_input)
    assert f"{student.first_name} {student.last_name}" == expected


@pytest.mark.parametrize('test_input, expected',
                         [(random.randint(1, 200), None)])
def test_delete_student(test_input, expected, client, app):
    delete_student(test_input)
    assert models.Student.query.filter_by(id=test_input).first() == expected


def test_add_student_from_list(client, app):
    add_course('Programming')
    course = models.Course.query.filter_by(name='Programming').first()
    students = student_list_from_database(1)
    add_students_to_course(course.name, students)
    for student in students:
        assert course in student.course


def test_remove_student_from_course(client, app):
    student = Student.query.filter_by(id=10).first()
    removed_course = remove_student_from_course(student.id)
    assert removed_course not in student.course



# from queries import *
#
#
# def test_q_groups_by_count(runner):
#     result = runner.invoke(cli=q_groups_by_count, args=['15'])
#     assert 'Group HO-12, have 13 students.' in result.output
#
#
# def test_q_students_by_course(runner):
#     result = runner.invoke(cli=q_students_by_course, args=['Law'])
