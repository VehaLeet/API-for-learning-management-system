import requests
from data_creation import generate_group_name

BASE = "http://127.0.0.1:5000"
#
# response = requests.get(BASE + "/api/v1/students")
# print(response.json())
# headers = {"Content-Type": "application/xml"}
# data = {"name": "Tyler Derden"}
#
# response = requests.post(BASE + "/api/v1/students", json=data)
# print(response.json())

# response = requests.get(BASE + "/api/v1/courses/1/students")
# print(response.json())
# print(response.text)
# data = {
#     "student_id": 1
# }
#
# response = requests.post(BASE + "/api/v1/courses/1/students", json=data)
# print(response)

# response = requests.delete(BASE + "/api/v1/courses/1/students/1")
# print(response)

# response = requests.get(BASE + "/api/v1/students/227", headers=headers)
# print(response.json())
# print(response.text)
# print(response.headers.get("Content-Type"))
# print(response.status_code)

# response = requests.delete(BASE + "/api/v1/students/9")
# print(response.json())

# response = requests.get(BASE + "/api/v1/students/9", headers=headers)
# print(response.json())

# #
# data = {
#     "group_id": 10,
#     "first_name": "Tyler",
#     "last_name": "Derden",
#     "course": "Law"
# }
# response = requests.put(BASE + "/api/v1/students/201", json=data)
# print(response.json())

# response = requests.delete(BASE + "/api/v1/students/201")
# print(response)

# response = requests.get(BASE + "/api/v1/students")
# print(response.json())

# data = {
#     "course": "Marketing"
# }
# response = requests.put(BASE + "/api/v1/students", headers=headers, json=data)
# print(response.json())

# response = requests.get(BASE + "/api/v1/groups/3")
# print(response.json())

# data = {
#     "name": "WI-67"
#     # "name": generate_group_name(1)[0]
# }
#
# response = requests.post(BASE + "/api/v1/groups", json=data)
# print(response.json())
#
# response = requests.get(BASE + "/api/v1/groups/1")
# print(response.json())

# data = {
#     "name": generate_group_name(1)[0],
#     "student": "Tutankhamen Shaffer"
# }
# #
# response = requests.put(BASE + "/api/v1/groups/1", json=data)
# print(response.json())

# response = requests.delete(BASE + "/api/v1/groups/4")
# print(response.json())

# response = requests.get(BASE + "/api/v1/groups/3")
# print(response.json())

# response = requests.get(BASE + "/api/v1/courses")
# print(response.json())

# response = requests.delete(BASE + "/api/v1/courses/3")
# print(response.json())

# response = requests.get(BASE + "/api/v1/courses/3")
# print(response.json())

# data = {
#     "name": "Military",
#     "description": "Weapons, armors, vehicles"
# }
# # #
# response = requests.post(BASE + "/api/v1/courses", json=data)
# print(response.json())

# response = requests.get(BASE + "/api/v1/courses/11")
# print(response.json())

# data = {
#     "name": "Military tech",
#     "description": "Weapons, armors, vehicles"
# }
#
# response = requests.put(BASE + "/api/v1/courses/1", headers=headers, json=data)
# print(response.json())

# response = requests.delete(BASE + "/api/v1/courses/11")
# print(response.json())

#
# response = requests.get(BASE + "/api/v1/courses/11")
# print(response.json())