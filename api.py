from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal
from flask import request, make_response
from crud_and_special import *
import models


def response_json_xml_students(students: list, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_students(students))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(students, student_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


def response_json_xml_student(student, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_student(student))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(student, student_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


def response_json_xml_groups(groups: list, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_groups(groups))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(groups, group_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


def response_json_xml_group(group, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_group(group))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(group, group_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


def response_json_xml_courses(courses: list, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_courses(courses))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(courses, course_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


def response_json_xml_course(course, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_course(course))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(course, course_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


def response_json_xml_course_students(course, format_type: str = None, content_type: str = None):
    if format_type == "xml" or content_type == 'application/xml':
        response = make_response(xml_format_course_students(course))
        response.headers.set('Content-Type', 'application/xml')
        response.status_code = 200
        return response
    else:
        response = make_response(marshal(course, course_students_fields))
        response.headers.set('Content-Type', 'application/json')
        response.status_code = 200
        return response


api = Api()

student_fields = {
    "id": fields.Integer,
    "group_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "course": fields.String(attribute=lambda student: ', '.join([c.name for c in student.course]) if student else None)
}


class StudentsPage(Resource):
    def get(self):
        courses_query = request.args.get('course')
        if courses_query:
            students = find_students_by_course(courses_query)
            format_type = request.args.get('format')
            content_type = request.headers.get('Content-Type')

            return response_json_xml_students(students, format_type, content_type)

        else:
            students = models.Student.query.all()
            format_type = request.args.get('format')
            content_type = request.headers.get('Content-Type')

            return response_json_xml_students(students, format_type, content_type)

    @marshal_with(student_fields)
    def post(self):
        students_post = reqparse.RequestParser()
        students_post.add_argument('name', type=str, help='Name of the Student required.', required=True)
        data = students_post.parse_args()
        abort_if_student_exist(data['name'])
        return add_student(data['name']), 201

    def put(self):
        students_put = reqparse.RequestParser()
        students_put.add_argument('course', type=str, help='Name of the course required.', required=True)
        data = students_put.parse_args()
        students = models.Student.query.all()
        add_students_to_course(data["course"], students)
        return 202

    def delete(self):
        models.db.session.query(models.Student).delete()
        db.session.commit()
        return 204


class StudentPage(Resource):
    def get(self, student_id):
        abort_if_student_doesnt_exist(student_id)
        student = models.Student.query.filter_by(id=student_id).first()
        format_type = request.args.get('format')
        content_type = request.headers.get('Content-Type')

        return response_json_xml_student(student, format_type, content_type)

    @marshal_with(student_fields)
    def put(self, student_id):
        abort_if_student_doesnt_exist(student_id)
        student_put = reqparse.RequestParser()
        student_put.add_argument('id', type=int)
        student_put.add_argument('group_id', type=int)
        student_put.add_argument('first_name', type=str, help='first_name of the Student required.', required=True)
        student_put.add_argument('last_name', type=str, help='last_name of the Student required.', required=True)
        student_put.add_argument('course', type=str)

        data = student_put.parse_args()
        student = edit_student(student_id, data)
        return student, 202

    def delete(self, student_id):
        abort_if_student_doesnt_exist(student_id)
        delete_student(student_id)
        return 204


group_fields = {
    "id": fields.Integer,
    "name": fields.String,
    # "student": fields.String
    "student": fields.String(
        attribute=lambda group: ', '.join([f"{s.first_name} {s.last_name}" for s in group.student]) if group else None)

}


class GroupsPage(Resource):
    def get(self):
        count = request.args.get('count')
        if count:
            groups = find_group_by_count(count)
            format_type = request.args.get('format')
            content_type = request.headers.get('Content-Type')
            return response_json_xml_groups(groups, format_type, content_type)

        else:
            groups = models.Group.query.all()
            format_type = request.args.get('format')
            content_type = request.headers.get('Content-Type')
            return response_json_xml_groups(groups, format_type, content_type)

    @marshal_with(group_fields)
    def post(self):
        groups_post = reqparse.RequestParser()
        groups_post.add_argument('name', type=str, help='Name of the Group required.', required=True)
        data = groups_post.parse_args()
        abort_if_group_exist(data["name"])
        group = add_group(data["name"])
        return group, 201

    def delete(self):
        models.db.session.query(models.Group).delete()
        db.session.commit()
        return 204


class GroupPage(Resource):
    def get(self, group_id):
        abort_if_group_doesnt_exist(group_id)
        group = models.Group.query.filter_by(id=group_id).first()
        format_type = request.args.get('format')
        content_type = request.headers.get('Content-Type')
        return response_json_xml_group(group, format_type, content_type)

    @marshal_with(group_fields)
    def put(self, group_id):
        group_put = reqparse.RequestParser()
        group_put.add_argument('name', type=str, help='Name of the Group required.', required=True)
        group_put.add_argument('student', type=str)
        data = group_put.parse_args()
        group = edit_group(group_id, data)
        return group, 202

    def delete(self, group_id):
        abort_if_group_doesnt_exist(group_id)
        delete_group(group_id)
        return 204


course_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "student": fields.String(
        attribute=lambda course: ', '.join(
            [f"{s.first_name} {s.last_name}" for s in course.student]) if course else None)
}


class CoursesPage(Resource):
    def get(self):
        courses = models.Course.query.all()
        format_type = request.args.get('format')
        content_type = request.headers.get('Content-Type')
        return response_json_xml_courses(courses, format_type, content_type)

    @marshal_with(course_fields)
    def post(self):
        courses_post = reqparse.RequestParser()
        courses_post.add_argument('name', type=str, help='Name of the Course required.', required=True)
        courses_post.add_argument('description', type=str)

        data = courses_post.parse_args()
        abort_if_course_exist(data["name"])
        course = add_course(data["name"], data["description"])
        return course, 201

    def delete(self):
        models.db.session.query(models.Course).delete()
        db.session.commit()
        return 204


class CoursePage(Resource):
    def get(self, course_id):
        abort_if_course_doesnt_exist(course_id)
        course = models.Course.query.filter_by(id=course_id).first()
        # course_students_query = request.args.get('')
        format_type = request.args.get('format')
        content_type = request.headers.get('Content-Type')
        return response_json_xml_course(course, format_type, content_type)

    @marshal_with(course_fields)
    def put(self, course_id):
        course_put = reqparse.RequestParser()
        course_put.add_argument('name', type=str, help='Name of the Course required.', required=True)
        course_put.add_argument('description', type=str)

        data = course_put.parse_args()
        course = edit_course(course_id, data)
        return course, 202

    def delete(self, course_id):
        abort_if_course_doesnt_exist(course_id)
        delete_course(course_id)
        return 204


course_students_fields = {
    "students": fields.String(
        attribute=lambda course: ', '.join(
            [f"{s.first_name} {s.last_name}" for s in course.student]) if course else None),
    "total on course": fields.Integer(attribute=lambda course: len(course.student))
}


class CourseStudentsPage(Resource):
    def get(self, course_id):
        abort_if_course_doesnt_exist(course_id)
        course = models.Course.query.filter_by(id=course_id).first()
        format_type = request.args.get('format')
        content_type = request.headers.get('Content-Type')
        return response_json_xml_course_students(course, format_type, content_type)

    @marshal_with(course_students_fields)
    def post(self, course_id):
        courses_student_post = reqparse.RequestParser()
        courses_student_post.add_argument('student_id', type=int, help='Id of the Course required.', required=True)
        data = courses_student_post.parse_args()

        abort_if_course_doesnt_exist(course_id)
        course = models.Course.query.filter_by(id=course_id).first()
        add_student_to_course(course_id, data['student_id'])
        return course, 201


class DeleteCourseStudents(Resource):
    def delete(self, course_id, student_id):
        course = Course.query.filter_by(id=course_id).first()
        student = Student.query.filter_by(id=student_id).first()
        course.student.remove(student)
        db.session.commit()
        return 204


api.add_resource(StudentsPage, '/api/v1/students')
api.add_resource(StudentPage, '/api/v1/students/<student_id>')
api.add_resource(GroupsPage, '/api/v1/groups')
api.add_resource(GroupPage, '/api/v1/groups/<group_id>')
api.add_resource(CoursesPage, '/api/v1/courses')
api.add_resource(CoursePage, '/api/v1/courses/<course_id>')
api.add_resource(CourseStudentsPage, '/api/v1/courses/<course_id>/students')
api.add_resource(DeleteCourseStudents, '/api/v1/courses/<course_id>/students/<student_id>')
