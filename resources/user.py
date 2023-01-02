from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from marshmallow import Schema, fields
from db import db

from models import UserModel

blp = Blueprint("Users", __name__, description="Operation on users")


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()

            return {"success": True}, 201
        except:
            abort(500, message="Internal server error")


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {"token": access_token, "refresh_token": refresh_token}

        abort(401, message="Unauthorized")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {"token": new_token}


@blp.route("/user/<int:user_id>")
class UserDetails(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:

            user = UserModel.query.get_or_404(user_id)

            return user, 200
        except:
            abort(500, message="Internal server error")

    @jwt_required()
    def delete(self, user_id):

        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except:
            abort(500, message="Internal server error")

        return {"success": True}
