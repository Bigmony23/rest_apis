import logging

from pyexpat.errors import messages
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.functions import current_user

import db
from flask import request, jsonify
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint,abort

from Bloclist import BLACKLIST
from models import User
from flask_jwt_extended import jwt_required, get_jwt

from models.bloclist import BloclistModel
from schemas import UserSchema, BloclistSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity

blp=Blueprint('users',__name__)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if User.query.filter(User.username == user_data["username"]).first():
            abort(409, message="Username already exists")

        user = User(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered", "user": UserSchema().dump(user)}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            user = User.query.filter(User.username == user_data["username"]).first()
            print(user)
            if not user:
                raise Exception("User not found")

            if not pbkdf2_sha256.verify(user_data["password"], user.password):
                raise Exception("Incorrect password")

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        except Exception as e:
            abort(401, message=str(e))

    # def post(self, user_data):
    #     user = User.query.filter(User.username == user_data["username"]).first()
    #     if user and pbkdf2_sha256.verify(user_data["password"], user.password):
    #         access_token = create_access_token(identity=user.id)
    #         return {"access_token": access_token}
    #     abort(401, message="Incorrect username or password")
@blp.route("/users/<int:user_id>")
class Usergetfrom(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

@blp.route("/users")
class Users(MethodView):
    def get(self):
        users = User.query.all()
        return users
@blp.route("/userdata")
class test(MethodView):
    def get(self):
        return {"test"}
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.response(201, BloclistSchema)
    def post(self):
        try:
            jti = get_jwt()['jti']
            bloclist = BloclistModel(token=jti)
            db.session.add(bloclist)
            db.session.commit()
            return {"msg": "Successfully logged out"}, 200
        except Exception as e:
            logging.error(f"Error during logout: {str(e)}")
            return jsonify({"msg": "Logout failed", "error": str(e)}), 500
@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        jti = get_jwt()['jti']
        bloclist = BloclistModel(token=jti)
        return {"access_token":new_token}

        # try:
        #     jti = get_jwt()['jti']
        #     bloclist=BloclistModel(token=jti)
        #     db.session.add(bloclist)
        #     db.session.commit()
        #     # BLACKLIST.add(jti)
        #     # logging.info(f"JWT {jti} added to blacklist")
        #     return jsonify({"msg": "Successfully logged out"}), 200
        # except Exception as e:
        #     logging.error(f"Error during logout: {str(e)}")
        #     return jsonify({"msg": "Logout failed", "error": str(e)}), 500

# class UserRegister(MethodView):
#     # @blp.response(200,UserSchema)
#     # def get(self):
#     #     users = User.query.all()
#     #     return users
#     @blp.arguments(UserSchema)
#     @blp.response(201,UserSchema)
#     def post(self,user_data):
#         if User.query.filter(User.username==user_data["username"]).first():
#             abort(409,message="Username already exists")
#         user = User(
#             username=user_data["username"],
#             password=pbkdf2_sha256.encrypt(user_data["password"])
#         )
#         db.session.add(user)
#         db.session.commit()
#         print(user)
#         return {"message":"User registered","user":UserSchema().dump(user)}, 201
# @blp.route("/users/<int:user_id>")
# class Usergetfrom(MethodView):
#     @blp.arguments(UserSchema)
#     @blp.response(200,UserSchema)
#     def get(self,user_id):
#         user=User.query.get(user_id)
#         return user
#     def delete(self,user_id):
#         user=User.query.get_or_404(user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return {"message":"User deleted"},200



