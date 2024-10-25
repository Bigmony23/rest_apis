import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint,abort
# from db import stores
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
blp=Blueprint('store',__name__,description="Operation on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        if store:
            db.session.delete(store)
            db.session.commit()
            return {'message':'Store deleted successfully'}
        else:
            abort(404,message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        try:
            stores = StoreModel.query.all()
            return stores
        except Exception as e:
            return {"message": str(e)}, 500  # Возвращаем сообщение об ошибке

    # @blp.route("/store")
# class StoreList(MethodView):
#     @jwt_required
#     @blp.response(200,StoreSchema(many=True))
#     def get(self):
#         return StoreModel.query.all()
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store already exists")
        except SQLAlchemyError:
            abort(500, message="Something went wrong while inserting item")

        return store



