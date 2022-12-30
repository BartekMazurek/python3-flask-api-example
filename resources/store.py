from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import db

from models import StoreModel

blp = Blueprint("Stores", __name__, description="Operation on stores")


class TagPreviewSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class StorePreviewSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    country = fields.Str(required=True)
    city = fields.Str(required=True)
    address = fields.Str(required=True)
    tags = fields.Nested(TagPreviewSchema())


class StoreEditSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    country = fields.Str(required=True)
    city = fields.Str(required=True)
    address = fields.Str(required=True)


@blp.route("/store")
class StorePreview(MethodView):

    @blp.response(200, StorePreviewSchema(many=True))
    def get(self):
        try:
            return StoreModel.query.all()

        except:
            abort(500, message="Internal server error")

    @blp.arguments(StoreEditSchema)
    @blp.response(201, StoreEditSchema)
    def post(self, item_data):

        store = StoreModel(**item_data)

        try:
            db.session.add(store)
            db.session.commit()
        except:
            abort(500, message="Internal server error")

        return store

    @blp.arguments(StoreEditSchema)
    @blp.response(201, StoreEditSchema)
    def put(self, item_data):

        store = StoreModel.query.get(item_data["id"])

        if store:

            store.name = item_data["name"]
            store.country = item_data["country"]
            store.city = item_data["city"]
            store.address = item_data["address"]

        else:

            store = StoreModel(**item_data)

        try:
            db.session.add(store)
            db.session.commit()
        except:
            abort(500, message="Internal server error")

        return store

@blp.route("/store/<int:store_id>")
class StoreDetails(MethodView):

    @blp.response(200, StoreEditSchema)
    def get(self, store_id):
        try:

            store = StoreModel.query.get_or_404(store_id)

            return store, 200
        except:
            abort(500, message="Internal server error")

    def delete(self, store_id):

        store = StoreModel.query.get_or_404(store_id)

        try:
            db.session.delete(store)
            db.session.commit()
        except:
            abort(500, message="Internal server error")

        return {"success": True}