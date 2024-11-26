from models.employee import Employee
from database import db

class EmployeeController:
    @staticmethod
    def get_all_employees():
        return Employee.query.all()

    @staticmethod
    def get_employee_by_id(employee_id):
        return Employee.query.get(employee_id)

    @staticmethod
    def add_employee(data):
        new_employee = Employee(name=data['name'], position=data['position'])
        db.session.add(new_employee)
        db.session.commit()
        return new_employee

    @staticmethod
    def update_employee(employee_id, data):
        employee = Employee.query.get(employee_id)
        if employee:
            employee.name = data['name']
            employee.position = data['position']
            db.session.commit()
        return employee

    @staticmethod
    def delete_employee(employee_id):
        employee = Employee.query.get(employee_id)
        if employee:
            db.session.delete(employee)
            db.session.commit()
        return employee
