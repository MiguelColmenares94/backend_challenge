from marshmallow import Schema, fields


class HealthSchema(Schema):
    status = fields.String(required=True)
    database = fields.String(required=True)
