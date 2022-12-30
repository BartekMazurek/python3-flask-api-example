from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import db

from models import TagModel

blp = Blueprint("Tags", __name__, description="Operation on tags")


class TagPreviewSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    store_id = fields.Int(required=True)


@blp.route("/tag")
class TagPreview(MethodView):

    @blp.arguments(TagPreviewSchema)
    @blp.response(201, TagPreviewSchema)
    def post(self, item_data):

        tag = TagModel(**item_data)

        try:
            db.session.add(tag)
            db.session.commit()
        except:
            abort(500, message="Internal server error")

        return tag

@blp.route("/tag/<int:tag_id>")
class TagDetails(MethodView):

    @blp.response(200, TagPreviewSchema)
    def get(self, tag_id):
        try:

            tag = TagModel.query.get_or_404(tag_id)

            return tag, 200
        except:
            abort(500, message="Internal server error")

    def delete(self, tag_id):

        tag = TagModel.query.get_or_404(tag_id)

        try:
            db.session.delete(tag)
            db.session.commit()
        except:
            abort(500, message="Internal server error")

        return {"success": True}

