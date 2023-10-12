import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError



storeBlueprint = Blueprint("Stores", "stores",description= " opearations on stores ")


@storeBlueprint.route("/store")
class StoreListCreate(MethodView):
    
    @storeBlueprint.response(200,StoreSchema(many=True))#to ensure the format of response data, what to be included and what not
    def get(self):
        return StoreModel.query.all()
    
    @storeBlueprint.arguments(StoreSchema)#to ensure user is sending data of correct schema
    @storeBlueprint.response(201,StoreSchema)
    def post(self, data):
        store = StoreModel(**data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction on error
            print(f"IntegrityError: {str(e)}")
            abort(400, "Duplicate store not allowed")
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction on error
            print(f"SQLAlchemyError: {str(e)}")
            abort(500, message="Error creating store")
        
        return store



@storeBlueprint.route("/store/<int:store_id>")
class StoreDetails(MethodView):
    @storeBlueprint.response(200,StoreSchema)
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store
        
        
    def delete(self,store_id):
        store=StoreModel.query.get_or_404(store_id) 
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted successfully"}
        # raise NotImplementedError("Deleting store is not implemented")



# without db code is below ,dictionary is used

# storeBlueprint = Blueprint("Stores", "stores",description= " opearations on stores ")


# @storeBlueprint.route("/store")
# class StoreListCreate(MethodView):
    
#     @storeBlueprint.response(200,StoreSchema(many=True))#to ensure the format of response data, what to be included and what not
#     def get(self):
#         return stores.values()
    
#     @storeBlueprint.arguments(StoreSchema)#to ensure user is sending data of correct schema
#     @storeBlueprint.response(201,StoreSchema)
#     def post(self,data):
#         # data=request.get_json()
#         # if "name" not in data:
#         #     abort(400,message="name is required")
#         for store in stores.values():
#             if store["name"]==data["name"]:
#                 abort(400,message="store already exists")   
#         store_id=uuid.uuid4().hex
#         store={**data,"id":store_id}
#         stores[store_id]=store
#         return store,201



# @storeBlueprint.route("/store/<store_id>")
# class StoreDetails(MethodView):
#     @storeBlueprint.response(200,StoreSchema)
#     def get(self,store_id):
#         try:
#             return stores[store_id]
#         except:
#             abort(404,message="Store not found")
        
#     def delete(self,store_id):
#         try:
#             del stores[store_id]
#             return {"message":"deleted"},204
#         except:
#             abort(404,message="Store not found") 