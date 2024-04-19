# aditya-sarana-graha-test

# Stack

- Python 3.12
- Flask 2.3.3
- Flask SQLAlchemy
- Docker

# Steps to run App

- Make sure docker installed in your computer
- On your teminal type `make run-app`

# API List

- Create User
  - [POST] /api/users/create
- Login
  - [POST] /api/login
- Create Employee
  - [POST] /api/employees/create
- Get All Employees
  - [GET] /api/employees/get
- Update User
  - [PUT] /api/employees/update/<uuid:employee_id>
- Delete User
  - [DELETE] /api/employees/delete/<uuid:employee_id>
- Add salary to employee
  - [POST] /api/salary/<uuid:employee_id>
- Get Employee by ID (inc. Salary)
  - [GET] /api/employees/get/<uuid:employee_id>
