from sqlalchemy import func
from models.employee import Employee
from models.production import Production
from database import db
from decorators.role_required import role_required

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

    @staticmethod
    @role_required('admin')
    def save_employee(data):
        
        new_employee = Employee(
            name=data['name'],
            position=data['position'],
            department=data['department']
        )
        db.session.add(new_employee)
        db.session.commit()
        return {"message": "Employee saved successfully"}



    @staticmethod
    @role_required('admin')
    def analyze_employee_performance():
        result = db.session.query(
            Employee.name.label('employee_name'),
            func.sum(Production.quantity_produced).label('total_quantity_produced')
        ).join(Production, Employee.id == Production.employee_id
        ).group_by(Employee.name).all()
        
       
        performance_data = [
            {"employee_name": row.employee_name, "total_quantity_produced": row.total_quantity_produced}
            for row in result
        ]

        return performance_data
