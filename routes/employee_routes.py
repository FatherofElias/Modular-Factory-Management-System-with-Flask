from flask import Blueprint, request, jsonify
from controllers.employee_controller import EmployeeController
from models.schemas.employee_schema import EmployeeSchema
from jwt import jwt_required
from decorators.role_required import role_required
from __init__ import limiter

bp = Blueprint('employees', __name__, url_prefix='/employees')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

@bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_employees():
    employees = EmployeeController.get_all_employees()
    return employees_schema.jsonify(employees)

@bp.route('/<int:employee_id>', methods=['GET'])
@limiter.limit("5 per minute")
def get_employee(employee_id):
    employee = EmployeeController.get_employee_by_id(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    return employee_schema.jsonify(employee)

@bp.route('/', methods=['POST'])
@limiter.limit("2 per minute")
def add_employee():
    data = request.json
    new_employee = EmployeeController.add_employee(data)
    return employee_schema.jsonify(new_employee), 201

@bp.route('/<int:employee_id>', methods=['PUT'])
@limiter.limit("2 per minute")
def update_employee(employee_id):
    data = request.json
    updated_employee = EmployeeController.update_employee(employee_id, data)
    if not updated_employee:
        return jsonify({'message': 'Employee not found'}), 404
    return employee_schema.jsonify(updated_employee)

@bp.route('/<int:employee_id>', methods=['DELETE'])
@limiter.limit("2 per minute")
def delete_employee(employee_id):
    deleted_employee = EmployeeController.delete_employee(employee_id)
    if not deleted_employee:
        return jsonify({'message': 'Employee not found'}), 404
    return employee_schema.jsonify(deleted_employee)


@bp.route('/performance', methods=['GET'])
@limiter.limit("5 per minute")
def get_employee_performance():
    performance_data = EmployeeController.analyze_employee_performance()
    return jsonify(performance_data)

@bp.route('/performance', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_employee_performance():
    performance_data = EmployeeController.analyze_employee_performance()
    return jsonify(performance_data)