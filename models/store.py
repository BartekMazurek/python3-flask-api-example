from db import db

class StoreModel(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic", cascade="all, delete, delete-orphan")
