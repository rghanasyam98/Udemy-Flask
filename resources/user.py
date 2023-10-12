from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from models import UserModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt,get_jwt_identity
from blacklist import BLOCKLIST

userBlueprint=Blueprint("User","user", description="operations on user")

@userBlueprint.route("/user")
class UserRegisterView(MethodView):
    
    @userBlueprint.arguments(UserSchema)
    def post(self,data):
        print(data)
        if UserModel.query.filter(UserModel.username == data["username"]).first():
            abort(409,message="User already exists")
        user=UserModel(
            username=data["username"],
            password=pbkdf2_sha256.hash(data["password"])
        )   
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))     
        return {"message":"registration successful"},201    
    
@userBlueprint.route("/login")    
class UserLogin(MethodView):
    
    @userBlueprint.arguments(UserSchema)
    def post(self,data):
        user=UserModel.query.filter(UserModel.username == data["username"]).first()
        if user and pbkdf2_sha256.verify(data["password"],user.password):
            access_token=create_access_token(identity=user.id,fresh=True)
            refresh_token=create_refresh_token(identity=user.id)
            return {'access_token':access_token,"refresh_token":refresh_token},200
        abort(400,message="Invalid username or password")

@userBlueprint.route("/refresh") 
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        # getting the user id inside token
        user=get_jwt_identity() 
        # creating a new access token but fresh field is set to false for more restrictions
        new_token=create_access_token(identity=user,fresh=False)
        return {"new_access_token": new_token}      

    
        
@userBlueprint.route("/user/<int:id>") 
class UserDetails(MethodView):
    
    @userBlueprint.response(200,UserSchema)
    def get(self,id):
        user=UserModel.query.get_or_404(id)
        return user 
    def delete(self,id):
        user=UserModel.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))   
        return {"message":"deleted successfully"},200     
              
@userBlueprint.route("/logout")
class UserLogout(MethodView):
    
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"successfully logged out"},200
                      