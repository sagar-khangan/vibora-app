from vibora.schemas import Schema, fields


class UserSchema(Schema):

    id: str = fields.Integer
    name: str = fields.String