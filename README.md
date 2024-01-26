# API for learning management system


## Introduction

System that can track groups, students on specific courses.

## Features

You can check, add, modify, delete:
- students;
- groups;
- courses;
from API using HTTP methods.(GET, POST, PUT, DELETE)

### Prerequisites

All libraries and additional modules contains in "requirements.txt"
 - use: "pip install -r .\requirements.txt"

## Getting started

To set up and run project on a local machine.
1. Set your database URI in config.py file: "SQLALCHEMY_DATABASE_URI";
2. Create tables using command: "flask --app table_creation create_database"
3. Start server :"flask --app manage run"

for demonstrating you can use data creation test command:
"flask --app data_creation create-data"
this command creates randomized students, groups, courses, and divides into groups and courses.

For using that API you need to utilize these endpoints:
- 'http://localhost:5000/api/v1/students':
    GET - display list of all students in database;
    POST - add student to database("name": "Firstname Lastname");
    DELETE - delete all students;

- 'http://localhost:5000/api/v1/students/<student_id>':
    GET - display information about a specific student;
    PUT - change student info, 
    example:("group_id": "WI-67", "first_name": "Firstname", "last_name": "Lastname", "course": "Military");
    DELETE - delete student;

- 'http://localhost:5000/api/v1/groups':
    GET - display list of all groups in database;
    POST - add group to database, example: ("name": "Your-group-name");
    DELETE - delete all groups;

- 'http://localhost:5000/api/v1/groups/<group_id>':
    GET - display information about a specific group;
    PUT - add student to specific group or change group name, 
    example: ("name": "WI-67","student": "Firstname Lastname");
    DELETE - delete specific group;

- 'http://localhost:5000/api/v1/courses':
    GET - display list of all courses in database;
    POST - add course to database, example: ("name": "Military", "description": "Weapons, armors, vehicles");
    DELETE - delete all courses;

- 'http://localhost:5000/api/v1/courses/<course_id>':
    GET - display information about a specific course;
    PUT - add\change description or name of specific course, 
    example: ("name": "Military vehicles","description": "Only vehicles");
    DELETE - delete specific course;

- 'http://localhost:5000/api/v1/courses/<course_id>/students':
    GET - display information about all students on specific course;
    POST - add student to specific course, example: ("student_id": 1);

- 'http://localhost:5000/api/v1/courses/<course_id>/students/<student_id>':
    DELETE - remove student from course, example: ("student_id": 1) 

Alternatively you can get info from database, use CLI commands:
- "flask --app queries q_groups_by_count (count)" gives list of all students on group with <= count value;
- "flask --app queries q_students_by_course (Name of course)" gives list of all students on specific course;
- "flask --app queries q_add_student (Firstname Lastname)" add a student to database;
- "flask --app queries q_delete_student_byid (student_id)" delete specific student;

