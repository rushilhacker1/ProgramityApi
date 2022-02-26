from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_ngrok import run_with_ngrok


def abort_on_presence(presence_id):
    user = UserModel.query.filter_by(id=presence_id).first()
    if not user:
        abort(404, message="User not found")


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['DEBUG'] = True
run_with_ngrok(app)
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User(name = {name}, Email = {Email})"


class LangModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Lang(lang={lang})"


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="Name of the user is required", required=True)
user_put_args.add_argument("Email", type=str, help="Views of the user", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="Name of the user is required")
user_update_args.add_argument("Email", type=str, help="Views of the user")

lang_put_args = reqparse.RequestParser()
lang_put_args.add_argument("lang", type=str, help="lang is required", required=True)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'Email': fields.String
}
lang_resource_fields = {
    'id': fields.Integer,
    'lang': fields.String
}

db.create_all()


class User(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User id taken...")

        user = UserModel(id=user_id, name=args['name'], Email=args['Email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['Email']:
            result.views = args['Email']

        db.session.commit()

        return result

    def delete(self, user_id):
        abort_on_presence(user_id)
        UserModel.query.filter_by(id=user_id).delete()
        db.session.commit()
        return '', 204


class AllUsers(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return UserModel.query.all()


class Languages(Resource):
    @marshal_with(lang_resource_fields)
    def get(self, lang_id):
        result = LangModel.query.filter_by(id=lang_id).first()
        if not result:
            abort(404, message="Could not find lang with that id")
        return result

    @marshal_with(lang_resource_fields)
    def put(self, lang_id):
        args = lang_put_args.parse_args()
        result = LangModel.query.filter_by(id=lang_id).first()
        if result:
            abort(409, message="lang id taken...")

        lang = LangModel(id=lang_id, lang=args['lang'])
        db.session.add(lang)
        db.session.commit()
        return lang, 201


class AllLanguages(Resource):
    @marshal_with(lang_resource_fields)
    def get(self):
        return LangModel.query.all()


api.add_resource(User, "/user/<int:user_id>")
api.add_resource(AllUsers, "/user/")
api.add_resource(Languages, "/languages/<int:lang_id>")
api.add_resource(AllLanguages, "/languages/")

if __name__ == "__main__":
    app.run()
