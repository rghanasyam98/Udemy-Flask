from marshmallow import Schema,fields

class PlainItemSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)
    
    
class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()
    store_id=fields.Integer() 
    
class PlainStoreSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
    
class PlainTagSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)       
    
class StoreSchema(PlainStoreSchema):
    items=fields.List(fields.Nested(PlainItemSchema(),dump_only=True))
    # tags=fields.List(fields.Nested(PlainTagSchema(),dump_only=True))
    
class ItemSchema(PlainItemSchema):
    store_id=fields.Integer(required=True,load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema(), dump_only=True))            
    
class TagSchema(PlainTagSchema):
    store_id=fields.Integer(required=True,dump_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(PlainItemSchema(),dump_only=True))    
    
#this kind of schemas are used when we have additional data in response (e.g. message) that are not part of the model but we need other model fields
class TagAndItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(PlainItemSchema)
    tag=fields.Nested(PlainTagSchema)    
    
    
class UserSchema(Schema):
    id=fields.Integer(dump_only=True)
    username=fields.Str()
    password=fields.Str(load_only=True)    