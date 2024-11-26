from marshmallow import fields
from schema import ma

class ProductionSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity_produced = fields.Int(required=True)
    date_produced = fields.Date(required=True)