from sqlalchemy import True_

import db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from models import TagModel,StoreModel,ItemModel

from schemas import TagSchema,TagandItemSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint('Tags','tags',__name__,description='tags')


@blp.route('/store/<int:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()  # lazy="dynamic" means 'tags' is a query

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # Проверяем наличие тега с таким же именем в данном магазине
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        # Создаем новый тег
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag
# @blp.route('/store/<int:store_id>/tag')
# class TagsInStore(MethodView):
#     @blp.response(200,TagSchema(many=True))
#     def get(self,store_id):
#         store = StoreModel.query.get_or_404(store_id)
#         return store.tags.all()  # lazy="dynamic" means 'tags' is a query
#
#         # store =StoreModel.query.get(store_id)
#         # return store.tags.all()
#
#     @blp.arguments(TagSchema)
#     @blp.response(201,TagSchema)
#     def post(self,tag_data,store_id):
#         # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
#         #     abort(400, message="A tag with that name already exists in that store.")
#
#         # if TagModel.query.filter(TagModel.id==store_id,TagModel.name==tag_data["name"]).first():
#         #     abort(400, message="Tag already exists")
#         tag=TagModel(**tag_data,store_id=store_id)
#         try:
#             db.session.add(tag)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             abort(500,message=str(e))
#         return tag

@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagsToItems(MethodView):
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred. Please try again.")
        return tag
    @blp.response(200,TagandItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get(item_id)
        tag=TagModel.query.get(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred. Please try again.")
        return {"message": "Item deleted successfully"}
@blp.route("/tag/<string:tag_id>")
class Tagmethod(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        print("get method called")
        tag=TagModel.query.get_or_404(tag_id)
        return tag


    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted successfully"}
        abort(
            400,
            message="Tag cannot be deleted")


