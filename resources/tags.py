import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items,stores
from schemas import TagSchema,PlainTagSchema,TagAndItemSchema
from models import ItemModel,StoreModel,TagModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


tagBlueprint=Blueprint("Tags","tags",description="opearations on tags")

@tagBlueprint.route("/store/<int:store_id>/tag")
class TagListCreate(MethodView):
    
    @tagBlueprint.response(200,PlainTagSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @tagBlueprint.arguments(TagSchema)
    @tagBlueprint.response(201,TagSchema)
    def post(self,data,store_id):
        tag=TagModel(store_id=store_id,**data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))
        return tag        
        
        
@tagBlueprint.route("/item/<int:item_id>/tag/<int:tag_id>")        
class LinkTagsToItem(MethodView):
    
    @tagBlueprint.response(201,TagSchema)
    def post(self,item_id,tag_id):
        print("***")
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        
        # to link
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))  
        return tag  
    
    @tagBlueprint.response(201,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        
        # to link
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))  
        return {"message":"successfully removed link","item":item,"tag":tag}    
            
            
        
        
        
@tagBlueprint.route("/tag/<int:tagId>")    
class TagDetails(MethodView):
    
    @tagBlueprint.response(200,TagSchema)
    def get(self,tagId):
        tag=TagModel.query.get_or_404(tagId)
        return tag
    
    # @tagBlueprint.response(200, {"message": "tag deleted"})
    # @tagBlueprint.alt_response(400, {"message": "tag is associated with items, could not delete"})
    def delete(self,tagId):
        tag=TagModel.query.get_or_404(tagId)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "tag deleted"}
        abort(400,message="tag is associated with items ,could not delete")    
        
    