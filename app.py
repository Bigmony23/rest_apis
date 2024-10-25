import os
import string
import uuid
import secrets
from audioop import error

from flask import Flask, jsonify
from flask_smorest import Api
from db import db
import models
from flask_jwt_extended import JWTManager

from models.bloclist import BloclistModel
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from flask_migrate import Migrate
from Bloclist import BLACKLIST
def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "http://cdn.jsdelivr.net/npm/swagger-ui-dist"




    # Исправление строки подключения к базе данных
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.environ.get("DATABASE_URL", "sqlite:///test.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    app.config["JWT_SECRET_KEY"] ="321551518961346964345693773380940211202"
        # secrets.SystemRandom().getrandbits(128))
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_bloclist(jwt_header, jwt_payload):
        jwt=jwt_payload['jti']
        return BloclistModel.query.filter_by(token=jwt).first()
        # return jwt_payload["jti"] in BLACKLIST
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "description":"The token has been revoked","error":"token revoked"
        }),401


    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token expired","error":"Token is expired"}),
            401,

        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Token invalid","error":"Token is invalid"}),
            401
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify({"message": "Token not found","error":"Token not found"}),
            401
        )
    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "Token is not fresh","error":"Token is not fresh"}),
        )



    # with app.app_context():
    #     db.create_all()  # Создание таблиц в контексте приложения
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    if __name__ == "__main__":
        app.run(debug=True)
    return app
# def create_app(db_url=None):
#     app = Flask(__name__)
#
#     app.config["PROPAGATE_EXCEPTIONS"] = True
#     app.config["API_TITLE"] = "Stores REST API"
#     app.config["API_VERSION"] = "v1"
#     app.config["OPENAPI_VERSION"] = "3.0.3"
#     app.config["OPENAPI_URL_PREFIX"] = "/"
#     app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
#     app.config["OPENAPI_SWAGGER_UI_URL"] = "http://cdn.jsdeliver.net/npm/swagger-ui-dist"
#     api = Api(app)
#     api.register_blueprint(ItemBlueprint)
#     api.register_blueprint(StoreBlueprint)
#     app.config["SQLALCHEMY_DATABASE_URI"] =db_url or os.getenv( "sqlite:///test.db")
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.init_app(app)
#     db.create_all()
#     return app

    # stores =[
    #     {
    #         "name": "My store",
    #         "items":[
    #         {"name":'chair',
    #         "price": 20.00
#         }
#         ]
#     }
#
# ]
# stores=[]
# items={
#     1:{
#         "name": "Chair",
#         "price": 20.00
#     },
#     2:{
#         "name": "Table",
#         "price": 34.00
#     }
# }
# items={}


# method get


