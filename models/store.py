# from db import db
# from sqlalchemy import Table, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
#
# class StoreModel(db.Model):
#     __tablename__ = 'stores'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80),unique=True, nullable=False)
#     items=db.relationship('ItemModel', back_populates='store', lazy="dynamic")
#     tags=db.relationship('TagModel', back_populates='store', lazy="dynamic")
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")