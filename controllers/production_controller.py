from models.production import Production
from database import db
from sqlalchemy import func
from models.product import Product
from decorators.role_required import role_required

class ProductionController:
    @staticmethod
    def get_all_productions():
        return Production.query.all()

    @staticmethod
    def get_production_by_id(production_id):
        return Production.query.get(production_id)

    @staticmethod
    def add_production(data):
        new_production = Production(
            product_id=data['product_id'],
            employee_id=data['employee_id'],  
            quantity_produced=data['quantity_produced'],
            date_produced=data['date_produced']
        )
        db.session.add(new_production)
        db.session.commit()
        return new_production

    @staticmethod
    def update_production(production_id, data):
        production = Production.query.get(production_id)
        if production:
            production.product_id = data['product_id']
            production.employee_id = data['employee_id'] 
            production.quantity_produced = data['quantity_produced']
            production.date_produced = data['date_produced']
            db.session.commit()
        return production

    @staticmethod
    def delete_production(production_id):
        production = Production.query.get(production_id)
        if production:
            db.session.delete(production)
            db.session.commit()
        return production



    @staticmethod
    def save_production(data):
        if 'product_id' not in data or 'employee_id' not in data or 'quantity_produced' not in data or 'date_produced' not in data:
            return {"message": "Missing required fields"}, 400

        new_production = Production(
            product_id=data['product_id'],
            employee_id=data['employee_id'],
            quantity_produced=data['quantity_produced'],
            date_produced=data['date_produced']
        )
        db.session.add(new_production)
        db.session.commit()
        return {"message": "Production saved successfully"}



    @staticmethod
    @role_required('admin')
    def evaluate_production_efficiency(specific_date):
        subquery = db.session.query(Production).filter(Production.date_produced == specific_date).subquery()
        result = db.session.query(
            Product.name.label('product_name'),
            func.sum(subquery.c.quantity_produced).label('total_quantity_produced')
        ).join(subquery, Product.id == subquery.c.product_id
        ).group_by(Product.name).all()
        
    
        efficiency_data = [
            {"product_name": row.product_name, "total_quantity_produced": row.total_quantity_produced}
            for row in result
        ]

        return efficiency_data
