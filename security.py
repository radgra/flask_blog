from models.user import UserModel
from werkzeug.security import generate_password_hash, check_password_hash




def authenticate(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.query.filter_by(id=user_id)