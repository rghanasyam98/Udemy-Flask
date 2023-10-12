import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items,stores
from schemas import ItemSchema,ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt



itemBlueprint=Blueprint("Items","items",description="opearations on items")


@itemBlueprint.route("/item")
class ItemListCreate(MethodView):
    
    @itemBlueprint.response(200,ItemSchema(many=True))#DEFINES the format of response data,what will be included and what will not
    def get(self):
        return ItemModel.query.all()
     
    @jwt_required(fresh=True)#neeed to have jwt token along with the request to provide access 
    @itemBlueprint.arguments(ItemSchema) #to ensure user is sending data of correct schema  
    @itemBlueprint.response(201,ItemSchema)  
    def post(self,data):
        item=ItemModel(**data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Error creating item")    
        
        return item    


@itemBlueprint.route("/item/<int:item_id>")
class ItemDetails(MethodView):
    
    @itemBlueprint.response(200,ItemSchema)
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
    
    @itemBlueprint.arguments(ItemUpdateSchema) #to ensure user is sending data of correct schema 
    @itemBlueprint.response(200,ItemSchema)      
    def put(self,data,item_id):
        item=ItemModel.query.get(item_id)
        if item:
            item.name=data["name"]
            item.price=data["price"]
            
        else:#item id already illengil pass cheytha data vech new instance aayit add cheyyunnu
            item=ItemModel(id=item_id,**data)
        db.session.add(item)
        db.session.commit()
        return item        
        # raise NotImplementedError("put is not implemented")
        
    @jwt_required()        
    def delete(self,item_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(400,message="Admin is authorized to delete")
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item Deleted successfully"}
        # raise NotImplementedError("delete is not implemented")



# wirh dictionary without db is below

# itemBlueprint=Blueprint("Items","items",description="opearations on items")


# @itemBlueprint.route("/item")
# class ItemListCreate(MethodView):
    
#     @itemBlueprint.response(200,ItemSchema(many=True))#DEFINES the format of response data,what will be included and what will not
#     def get(self):
#         return items.values()
     
#     @itemBlueprint.arguments(ItemSchema) #to ensure user is sending data of correct schema  
#     @itemBlueprint.response(201,ItemSchema)  
#     def post(self,data):
#         # data=request.get_json()
#         # if "name" not in data or "price" not in data or "store_id" not in data:
#         #     abort(400,message="name,price,store_id is required")
        
#         if data["store_id"] not in stores:
#             abort(404,message="store not found")    
#         for item in items.values():
#             if item["store_id"] == data["store_id"] and item["name"] == data["name"]:
#                 abort(400,message="this item is already in the store")   
    
#         item_id=uuid.uuid4().hex
#         item={**data,"id":item_id}
#         items[item_id]=item
#         return item    


# @itemBlueprint.route("/item/<string:item_id>")
# class ItemDetails(MethodView):
    
#     @itemBlueprint.response(200,ItemSchema)
#     def get(self,item_id):
#         try:
#             return items[item_id]
#         except:
#             abort(404,message="Item not found")
    
#     @itemBlueprint.arguments(ItemUpdateSchema) #to ensure user is sending data of correct schema 
#     @itemBlueprint.response(200,ItemSchema)      
#     def put(self,data,item_id):
#         # data=request.get_json()
#         # print(data)
#         # if "name" not in data or "price" not in data:
#         #     abort(400,message="missing name or price") 
#         try:
#             item=items[item_id]
#             item |= data
#             return item
#         except:
#             abort(404,message="Item not found")
            
#     def delete(self,item_id):
#         try:
#             del items[item_id]
#             return {"message":"deleted"},204
#         except:
#             abort(404,message="Item not found") 