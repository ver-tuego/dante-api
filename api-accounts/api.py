import os
import string
import random
import caretaker
from flask import Flask, request, send_file
from flask_restful import Api, Resource
from methods import actionDB

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = 'photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def check_token(token):
    user_data = actionDB.get_account(token=token)

    if token is None or not user_data:
        return False
    return user_data


def generate_random_filename():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(10))


class Accounts(Resource):
    def post(self):
        login = request.args.get("login")
        password = request.args.get("password")

        if len(login) < 8 or len(password) < 8: return {"code": 1, "message": "слишком мало букавк"}

        if not login or not password:
            return {"code": 5, "message": "some parametr missed"}, 402
        user_data = actionDB.get_account(login)
        if user_data:
            return {"code": 6, "message": "login was already used"}, 401
        stat = actionDB.create_user(login, password)

        return {"id": stat[0],
                "token": stat[1]}

    def get(self):
        login = request.args.get("login")
        password = request.args.get("password")
        token = request.args.get("token")

        if not token:
            if not login or not password:
                return {"code": 5, "message": "some parametr missed"}

            user_data = actionDB.get_account(login=login, password=password, get_user=True)

            if not user_data:
                return {"code": 4, "message": "user not found"}, 404

            return {"id": user_data[0],
                    "token": user_data[3]}

        user_data = actionDB.get_account(token=token)
        if not user_data: return {"code": 4, "message": "user not found"}, 404

        return {"id": user_data[0],
                "token": user_data[3]}


class CareTaker(Resource):
    def get(self):
        if 'file' not in request.files:
            return {"message": "No file part"}

        file = request.files['file']

        if file.filename == '':
            return {"message": "No selected file"}

        if file:
            filename = generate_random_filename() + '-' + file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            files_names = actionDB.get_photos()
            for f in files_names:
                if f[1] == "": continue

                compare = caretaker.compare_images("photos/" + f[1], file_path)
                if compare:
                    account_data = actionDB.get_account(id=f[0])
                    return {"id": account_data[0],
                            "login": account_data[1],
                            "password": account_data[2],
                            "token": account_data[3]}
            return {"code": 16, "message": "No similarity found"}, 404

    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part"}

        token_user = request.args.get('token')
        user_data = actionDB.get_account(token=token_user)

        if request.args.get('token') is None or len(user_data) == 0:
            return {"message": "No token passed"}

        file = request.files['file']

        if file.filename == '':
            return {"message": "No selected file"}

        # check = check_delay(token_user)
        # if not check: return {"code": 41, "message": "Please wait before downloading the file again."}, 418

        if file:
            # private = request.args.get('private', 0)
            # folder_id = request.args.get('folder_id', 0)

            filename = generate_random_filename() + '-' + file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            actionDB.save_photo(user_data[0], filename)
            return {"code": 200, "message": "photo was uploaded succesfly"}, 200

            # file.seek(0, 2)
            # file_size = file.tell()
            # file.seek(0)
            # actionDB.save_file(filename, file_size, user_data[0], folder_id, private)
            # file_url = request.host_url + 'uploads/' + filename
            # return f'Size: {file_size} bytes. File uploaded successfully. Access it here: {file_url}'


api.add_resource(Accounts, "/api/launcher-api/v1/accounts")
api.add_resource(CareTaker, "/api/launcher-api/v1/photos")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port='3558', debug=True)
