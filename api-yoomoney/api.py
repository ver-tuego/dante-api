import os
import string
import random
from flask import Flask, request, send_file
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Finances(Resource):
    def post(self):
        return {"code": 1}, 200

api.add_resource(Finances, "/api/yoomoney-api/v1")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3561', debug=True)
