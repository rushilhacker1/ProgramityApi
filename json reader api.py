# Imports
import json
from flask import Flask, jsonify
from flask_restful import Api, Resource, abort

# Inits
app = Flask(__name__)
api = Api(app)

# Getting Json data from json.json file
with open("json.json") as f:
    data = json.load(f)


class Users(Resource):
    def get(self, user_id):
        user_data = [data.get("UserId") == user_id]
        if len(user_data) == 0:
            abort(404, message="user not found")
        return jsonify({"user_data": data})


api.add_resource(Users, "/<int:user_id>")

app.run(host='0.0.0.0', debug=True)
