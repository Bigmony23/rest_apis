from db import db
class BloclistModel(db.Model):
    __tablename__ = 'bloclist'
    id = db.Column(db.Integer, primary_key=True)
    token=db.Column(db.String(255))