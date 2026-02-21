from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserQuerySchema(Schema):
    page = fields.Int()
    limit = fields.Int()
    email = fields.Str()


class PaginationMetaSchema(Schema):
    page = fields.Int(required=False)
    limit = fields.Int(required=False)
    total = fields.Int(required=True)
    pages = fields.Int(required=False)


class UserListResponseSchema(Schema):
    data = fields.List(fields.Nested(UserSchema))
    meta = fields.Nested(PaginationMetaSchema)
