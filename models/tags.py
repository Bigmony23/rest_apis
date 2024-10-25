# from db import db
# from sqlalchemy import Table, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# class TagModel(db.Model):
#     __tablename__ = 'tags'
#     id = db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String(80), unique=False, nullable=False)
#     store_id=db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
#
#     store=db.relationship("StoreModel",back_populates="tags")
#     items = db.relationship("items", back_populates="tags", secondary="items_tags")
#
#
from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")