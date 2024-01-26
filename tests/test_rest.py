import json
import pytest
from flask_restful import marshal
from flask import jsonify
from crud_and_special import *
from api import student_fields, group_fields, course_fields, course_students_fields
import models


test_data = [
    ('/api/v1/students', lambda app: jsonify(marshal(models.Student.query.all(), student_fields)).json),
    ('/api/v1/students/1', lambda app: jsonify(marshal(models.Student.query.get(1), student_fields)).json),
    ('/api/v1/students?course=Law', lambda app: jsonify(marshal(find_students_by_course('Law'), student_fields)).json),
    ('/api/v1/groups', lambda app: jsonify(marshal(models.Group.query.all(), group_fields)).json),
    ('/api/v1/groups/1', lambda app: jsonify(marshal(models.Group.query.get(1), group_fields)).json),
    ('/api/v1/groups?count=20', lambda app: jsonify(marshal(find_group_by_count(20), group_fields)).json),
    ('/api/v1/courses', lambda app: jsonify(marshal(models.Course.query.all(), course_fields)).json),
    ('/api/v1/courses/1', lambda app: jsonify(marshal(models.Course.query.get(1), course_fields)).json),
    (
        '/api/v1/courses/1/students',
        lambda app: jsonify(marshal(models.Course.query.get(1), course_students_fields)).json)
]


@pytest.mark.parametrize('test_input, expected', test_data)
def test_get_query_json(test_input, expected, client, app):
    assert client.get(test_input).status_code == 200
    assert client.get(test_input).json == expected(app)


test_data_xml = [
    ('/api/v1/students',
     lambda app: xml_format_students(models.Student.query.all()).get_data(as_text=True)
     ),
    ('/api/v1/students/1',
     lambda app: xml_format_student(models.Student.query.filter_by(id=1).first()).get_data(as_text=True)
     ),
    ('/api/v1/students?course=Law',
     lambda app: xml_format_students(find_students_by_course('Law')).get_data(as_text=True)
     ),
    ('/api/v1/groups',
     lambda app: xml_format_groups(models.Group.query.all()).get_data(as_text=True)
     ),
    ('/api/v1/groups/1',
     lambda app: xml_format_group(models.Group.query.filter_by(id=1).first()).get_data(as_text=True)
     ),
    ('/api/v1/groups?count=20',
     lambda app: xml_format_groups(find_group_by_count(20)).get_data(as_text=True)
     ),
    ('/api/v1/courses',
     lambda app: xml_format_courses(models.Course.query.all()).get_data(as_text=True)
     ),
    ('/api/v1/courses/1',
     lambda app: xml_format_course(models.Course.query.filter_by(id=1).first()).get_data(as_text=True)
     ),
    ('/api/v1/courses/1/students',
     lambda app: xml_format_course_students(models.Course.query.filter_by(id=1).first()).get_data(as_text=True)
     )
]


@pytest.mark.parametrize('test_input, expected', test_data_xml)
def test_get_resources_xml_format(test_input, expected, client, app):
    headers = {"Content-Type": 'application/xml'}
    assert client.get(test_input, headers=headers).get_data(as_text=True) == expected(app)


@pytest.mark.parametrize('test_input, expected', [
    ({'url': '/api/v1/students', 'data': {"name": "Ben Stiller"}},
     {"first_name": "Ben", "last_name": "Stiller"})
])
def test_student_post(test_input, expected, client, app):
    headers = {"Content-Type": "application/json"}
    created = client.post(test_input['url'], data=json.dumps(test_input['data']), headers=headers).json
    assert created['first_name'] == 'Ben'
    assert created['last_name'] == 'Stiller'


@pytest.mark.parametrize('test_input, expected', [
    ({'url': '/api/v1/groups', 'data': {"name": "SS-82"}},
     {"name": "SS-82"}),
    ({'url': '/api/v1/courses', 'data': {"name": "Driving"}},
     {"name": "Driving"}
     )
])
def test_group_course_post(test_input, expected, client, app):
    headers = {"Content-Type": "application/json"}
    created = client.post(test_input['url'], data=json.dumps(test_input['data']), headers=headers).json
    assert created['name'] == expected['name']


@pytest.mark.parametrize('test_input', [({'url': '/api/v1/courses/1/students', 'data': {"student_id": 1}})])
def test_course_students_post(test_input, client, app):
    headers = {"Content-Type": "application/json"}
    course = Course.query.filter_by(id=1).first()
    student = Student.query.filter_by(id=1).first()
    client.post(test_input['url'], data=json.dumps(test_input['data']), headers=headers)
    assert student in course.student


@pytest.mark.parametrize('test_input', ['/api/v1/courses/1/students/1'])
def test_course_students_delete(test_input, client, app):
    course = Course.query.filter_by(id=1).first()
    student = Student.query.filter_by(id=1).first()
    client.delete(test_input)
    assert student not in course.student


@pytest.mark.parametrize('test_input, expected',
                         [({'url': '/api/v1/students/1', 'data': {
                             "group_id": 10,
                             "first_name": "Tyler",
                             "last_name": "Derden",
                             "course": "Law"
                         }},
                           {
                               "group_id": 10,
                               "first_name": "Tyler",
                               "last_name": "Derden",
                               "course": "Law"
                           })
                          ])
def test_put_student(test_input, expected, client, app):
    headers = {"Content-Type": "application/json"}
    created = client.put(test_input['url'], data=json.dumps(test_input['data']), headers=headers).json
    assert created['first_name'] == expected['first_name']
    assert created['last_name'] == expected['last_name']
    assert created['group_id'] == expected['group_id']
    assert expected['course'] in created['course']

@pytest.mark.parametrize('test_input, expected',
                         [({'url': '/api/v1/groups/1', 'data': {
                             "name": "C3-PO",
                             "student": "Ito Vicksburg"
                         }},
                           {
                               "name": "C3-PO",
                               "student": "Ito Vicksburg"
                           })
                          ])
def test_put_group(test_input, expected, client, app):
    headers = {"Content-Type": "application/json"}
    created = client.put(test_input['url'], data=json.dumps(test_input['data']), headers=headers).json
    assert created['name'] == expected['name']
    assert expected['student'] in created['student']

@pytest.mark.parametrize('test_input, expected',
                         [({'url': '/api/v1/courses/1', 'data': {
                             "name": "Military tech",
                             "description": "Weapons, armors, vehicles"
                         }},
                           {
                               "name": "Military tech",
                               "description": "Weapons, armors, vehicles"
                           })
                          ])
def test_put_course(test_input, expected, client, app):
    headers = {"Content-Type": "application/json"}
    created = client.put(test_input['url'], data=json.dumps(test_input['data']), headers=headers).json
    assert created['name'] == expected['name']
    assert created['description'] == expected['description']


@pytest.mark.parametrize('test_input, expected',
                         [("/api/v1/students/23", {'message': "Student doesn't exist"}),
                          ("/api/v1/groups/8", {'message': f"Group doesn't exist"}),
                          ("/api/v1/courses/8", {'message': "Course doesn't exist"})])
def test_delete(test_input, expected, client, app):
    client.delete(test_input)
    assert client.get(test_input).json == expected
