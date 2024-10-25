import uuid

from flask_jwt_extended import jwt_required,get_jwt
from sqlalchemy.exc import SQLAlchemyError

import db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp=Blueprint('item',__name__)

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema)

    def get(self,item_id):

        item=ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self,item_id):
        jwt=get_jwt()
        if not jwt.get('is_admin'):
            abort(401,message='Admin privilege required.')
        item=ItemModel.query.get_or_404(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'message':'Item deleted successfully'}
        else:
            abort(404,Message='Item not found')


    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put(self, item_data,item_id):
        item = ItemModel.query.get(item_id)
        if item:

            item.price = item_data['price']
            item.name=item_data['name']
        else:
            item=ItemModel(id=item_id**item_data)
        db.session.add(item)
        db.session.commit()
        return item

@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(201,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
        # return {"stores": list(stores.values())}
        # return {"items": list(items.values())}
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemUpdateSchema)
    def post(self,item_data):
        item=ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Something went wrong while inserting item")

        return item

