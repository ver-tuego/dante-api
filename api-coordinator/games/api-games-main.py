# coordinator.py
import threading

from flask import Flask, request
from flask_restful import Resource, Api
import pingpong_server, actionDB
import random

app = Flask(__name__)
api = Api(app)


class GameCoordinator(Resource):
    def get(self):
        id = request.args.get("id")

        queue = actionDB.get_queue()

        if not queue:
            port = random.randint(100, 10000)
            actionDB.add_queue(port)
            thread = threading.Thread(target=pingpong_server.create_server, args=(port,))
            thread.start()

            return {"port": port}
        return {"port": queue[1]}


api.add_resource(GameCoordinator, '/api/coordinator-api/v1/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3566', debug=False)
