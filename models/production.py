from database import db

class Production(db.Model):
    __tablename__ = 'productions'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)  
    quantity_produced = db.Column(db.Integer, nullable=False)
    date_produced = db.Column(db.Date, nullable=False)

    product = db.relationship('Product', backref=db.backref('productions', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('productions', lazy=True))  
