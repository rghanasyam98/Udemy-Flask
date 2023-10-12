from flask import Flask,jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from db import db
from models import StoreModel, ItemModel  # Make sure to import your models
from resources.stores import storeBlueprint
from resources.items import itemBlueprint
from resources.tags import tagBlueprint
from resources.user import userBlueprint

from flask_jwt_extended import JWTManager 
from blacklist import BLOCKLIST

import os

def create_app(db_url=None):
    app = Flask(__name__)

    # Configuration settings
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # Initialize the database connection

    # for managing the database migrations
    migrate=Migrate(app,db)

    api = Api(app)
    
    # CONFIGURATIONS FOR JWT
    # KEY usuallt will be simple but need complex ,can use secrets module for generating complex secret keys
    #  print(secrets.SystemRandom().getrandbits(128))  => 265200694421817549795466256129199097072
    app.config["SECRET_KEY"] ="jose"
    jwt=JWTManager(app) 
    
    # we are able to add additional data to the jwt token 
    # this function automatically works when we create a access token
    @jwt.additional_claims_loader
    def add_claims_loader(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    # jwt_required needed aaya request verumbo aadyam below fn's will be executed
    # below fn checks the passed token is a blocked or not
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload.get("jti") in BLOCKLIST
    
    # executes if above fn returns true
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "message":"Token revoked"
                }
            ),401
        )
            
    #jwt required aayittulla functionlek fresh token aano pass cheyyunnth ennu aadyam tanne chk cheyyaan 
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return (
            jsonify({
                "message":"Token not fresh"
            }),401
        )
    
     
    # adding custom messages for jwt related errors
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (
    #         jsonify({ 
    #                 "message": "Invalid token",
    #                  "error":"token seems to be invalid"
    #                  }),401
    #     )
        
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header,jwt_payload):
    #     return (
    #         jsonify({ 
    #                 "message": "expired token",
    #                  "error":"token seems to be expired"
    #                  }),401
    #     )   
        
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return(
    #         jsonify(
    #             {
    #               "description": "missing token" , 
    #               "error":"token is missing"
    #             }
    #         )
    #     )     


    # Create database tables
    with app.app_context():
        db.create_all()

    api.register_blueprint(storeBlueprint)
    api.register_blueprint(itemBlueprint)
    api.register_blueprint(tagBlueprint)
    api.register_blueprint(userBlueprint)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


# all the below code is converted to class based approch of flask smorest

# ****************************************************************

# @app.get("/store")
# def getAllStores():
#     return {"store":list(stores.values())}

# @app.post("/store")
# def createStore():
#     data=request.get_json()
#     if "name" not in data:
#         abort(400,message="name is required")
#     for store in stores.values():
#         if store["name"]==data["name"]:
#             abort(400,message="store already exists")   
#     store_id=uuid.uuid4().hex
#     store={**data,"id":store_id}
#     stores[store_id]=store
#     return store,201

# @app.get("/store/<string:store_id>")
# def getOneStore(store_id):
#     try:
#         return stores[store_id],200
#     except:
#         abort(404,message="Store not found")
        
# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message":"deleted"},204
#     except:
#         abort(404,message="Store not found") 

# @app.post("/item")
# def create_item():
#     data=request.get_json()
#     if "name" not in data or "price" not in data or "store_id" not in data:
#         abort(400,message="name,price,store_id is required")
        
#     if data["store_id"] not in stores:
#        abort(404,message="store not found")    
       
#     for item in items.values():
#         if item["store_id"] == data["store_id"] and item["name"] == data["name"]:
#             abort(400,message="this item is already in the store")   
    
#     item_id=uuid.uuid4().hex
#     item={**data,"id":item_id}
#     items[item_id]=item
#     return item,201    
             
       
 
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     print(item_id)
#     try:
#         return items[item_id],200
#     except:
#         abort(404,message="Item not found")  
        
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message":"deleted"},204
#     except:
#         abort(404,message="Item not found")  
        
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     data=request.get_json()
#     print(data)
#     # if "name" not in data or "price" not in data:
#     #     abort(400,message="missing name or price") 
#     try:
#         item=items[item_id]
#         item |= data
#         return item,200
#     except:
#         abort(404,message="Item not found")               

# @app.get("/item")
# def getAllItems():
#     return {"items":list(items.values())}
    


# ***********************************************************

# stores=[
#     {
#         "name":"max",
#         "items":[
#             {
#                 "product":"shirt",
#                 "price":1000
#             }
#         ]
#     },
#     {
#         "name":"nike",
#         "items":[
#             {
#                 "product":"shoe",
#                 "price":2000
#             }
#         ]
#     }
# ]


# @app.get("/store")
# def getAllStores():
#     return {"store":stores}

# @app.post("/store")
# def createStore():
#     data=request.get_json()
#     new_store={"name":data["name"],"items":[]}
#     stores.append(new_store)
#     return new_store,201

# @app.post("/store/<string:shop>/item")
# def create_item(shop):
#     data=request.get_json()
#     for store in stores:
#         if store["name"]== shop:
#             new_item={"name":data["name"],"price":data["price"]}
#             store["items"].append(new_item)
#             return new_item,201
#     return {"message":"store not found"},404    
             
# @app.get("/store/<string:shop>")
# def getOneStore(shop):
#     print(shop)
#     for store in stores:
#         if store["name"] == shop:
#             return {"data":store},200
#     return {"message":"store not found"},404
 
# @app.get("/store/<string:shop>/item")
# def getStoreItem(shop):
#     for store in stores:
#         if store["name"] == shop:
#             return {"data":store["items"]},200    
#     return {"message":"store not found"},404    
    
# this code acts as an entry point


