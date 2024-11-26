from models.production import Production
from database import db

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
