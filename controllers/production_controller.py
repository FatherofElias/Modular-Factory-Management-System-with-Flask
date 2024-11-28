from models.production import Production
from database import db
from sqlalchemy import func
from models.product import Product

class ProductionController:
    @staticmethod
    def get_all_productions():
        return Production.query.all()

    @staticmethod
    def get_production_by_id(production_id):
        return Production.query.get(production_id)

    @staticmethod
    def add_production(data):
        new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
        db.session.add(new_production)
        db.session.commit()
        return new_production

    @staticmethod
    def update_production(production_id, data):
        production = Production.query.get(production_id)
        if production:
            production.product_id = data['product_id']
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
    def evaluate_production_efficiency(specific_date):
        subquery = db.session.query(Production).filter(Production.date_produced == specific_date).subquery()
        result = db.session.query(
            Product.name.label('product_name'),
            func.sum(subquery.c.quantity_produced).label('total_quantity_produced')
        ).join(subquery, Product.id == subquery.c.product_id
        ).group_by(Product.name).all()

        return result
