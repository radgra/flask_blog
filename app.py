from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.tag import TagList, Tag
from resources.post import PostList, Post, PostTag
from resources.category import CategoryList, Category
from resources.users import UserList, UserRegister
from security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_USERNAME_KEY'] = 'username'

app.secret_key = 'kdsalfjlksjflkdsjf'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


# JWT

# Resources
api.add_resource(TagList, '/tags')
api.add_resource(Tag, '/tags/<int:id>')
api.add_resource(PostList, '/posts')
api.add_resource(Post, '/posts/<int:id>')
api.add_resource(PostTag, '/posts/<int:id>/tags')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/categories/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')

# Init
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)