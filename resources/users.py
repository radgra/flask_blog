from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

class UserList(Resource):
    def get(self):
        users = UserModel.query.all()
        return {'data': [user.json() for user in users]}

    

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Field 'username' is required")
    parser.add_argument('password', type=str, required=True, help="Field 'password' is required")
    def post(self):
        data = self.parser.parse_args()
        new_user = UserModel(username=data['username'], password=generate_password_hash(data['password']))

        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError as e:
            return {"message": e.args[0]}, 500
        except:
            return {"message": "Something went wrong"}, 500

        return {'data': new_user.json()}