from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range

class RecordInputSchema(Schema):
    req_by = fields.Str(required=True, validate=Length(min=1 , error='Field Cannot be empty'))
    ref_id = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    lea = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    cr = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    accno = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    order_type = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    service = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    service_id = fields.Str(required=True, validate=Length(min=1, error='Field Cannot be empty'))
    cct = fields.Str(required=True, validate=Length(min=10))

class Validate:
    def validateReq(self):
        try:
            RecordInputSchema().load(self)
            return 'success'
        except ValidationError as err:
            return err.messages
