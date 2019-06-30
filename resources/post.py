from flask_restful import Resource, reqparse
from flask import request
from models.post import PostModel
from models.category import CategoryModel
from flask_jwt import jwt_required
from models.tag import TagModel
from db import db
from sqlalchemy import exc


class PostList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help="Field 'title' is required")
    parser.add_argument('category_id', type=int, required=True,
                        help="Field 'category_id' is required")
    parser.add_argument('content', type=str)

    @jwt_required()
    def get(self):
        # pierwsze zadanie - jak parsowac query_params - moze decorator ?
        # filtrowanie na podstawie category_id i tag_id
        # includes
        # pagination
        query = PostModel.query
        cat_id = request.args.get('category_id')
        tag_id = request.args.get('tag_id')
        includes = request.args.get('include')
        page = request.args.get('page', 1)
        per_page = request.args.get('page_size', 1)
            
        if cat_id:
            # roznica miedzy filter_by i filter
            # https://stackoverflow.com/questions/2128505/whats-the-difference-between-filter-and-filter-by-in-sqlalchemy
            query = query.filter_by(category_id=cat_id)
        if tag_id:
            # sprawdzic czy to query jest w porzadku
            query = query.filter(PostModel.tags.any(TagModel.id.in_([tag_id,])))
        tag_id = request.args.get('tag_id')

        try:
            page_obj = query.paginate(page=int(page), per_page=int(per_page))
        except:
            return {"message": "Something went wrong"}, 500

        #posts = query.all()
        if includes:
            return {
                    'pages':page_obj.pages,
                    'total':page_obj.total,
                    'data': [post.json_with_includes(includes) for post in page_obj.items]
                    }    

        return {
            'pages':page_obj.pages,
            'total':page_obj.total,
            'data': [post.json() for post in page_obj.items]
            }

    def post(self):
        data = self.parser.parse_args()

        # Foreign key constraint
        category_exist = CategoryModel.query.get(data['category_id'])
        if category_exist is None:
            return {'message': 'Category with such id doesnt exist.'}

        new_post = PostModel(**data)
        try:
            db.session.add(new_post)
            db.session.commit()
        except exc.IntegrityError as e:
            return {"message": e.args[0]}, 500
        except:
            return {"message": "Something went wrong"}, 500

        return {'data': new_post.json()}


class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('category_id', type=int)
    parser.add_argument('content', type=str)

    def get(self, id):
        post = PostModel.query.get(id)
        if post:
            return {"data": post.json_detail()}

        return {'message': 'Post not found'}

    def put(self, id):
        post = PostModel.query.get(id)
        data = self.parser.parse_args()

        # Foreign key constraint
        if post and data.get('category_id'):
            category_exist = CategoryModel.query.get(data['category_id'])
            if category_exist is None:
                return {'message': 'Category with such id doesnt exist.'}

        if post:
            # Pattern for partial updates - data.get('title',post.title) nie dziala bo parser automatycznie ustawia fieldy na None
            if data['title']:
                post.title = data['title']
            if data['content']:
                post.content = data['content']
            if data['category_id']:
                post.category_id = data['category_id']

            try:
                db.session.commit()
                return {'data':post.json()}
            except exc.IntegrityError as e:
                return {"message": e.args[0]}, 500
            except:
                return {"message": "Something went wrong"}, 500

        return {'message': 'Post not found'}

    def delete(self, id):
        post = PostModel.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return {'message': 'Post deleted'}
#
        return {'message': 'Post not found'}

class PostTag(Resource):
    def post(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('tags', type=int, action='append')
        data = parser.parse_args()

        post = PostModel.query.get(id)
        if post is None:
            return {'message': 'Post not found'}

        # 1 remove all associations
        # 2 test if foreign key exists
        # 3 append all - extend
        # Ten pattern po prostu nie znajduje modelu jesli id jest zle !
        # Nie wrzuca Erroru Foreignkey Constraint
        tags = TagModel.query.filter(TagModel.id.in_(data['tags'])).all()
        # post.tags[:] = tags 
        post.tags = tags 

        # Na razie mozna obejsc problem Errou sprawdzajac pythonem dlugosc listy i ids z id przekazanymi w body
        # Jesli nie beda sie zgadzaly rzucam error

        db.session.commit()

        return {"data":[tag.id for tag in tags]}
    
    def get(self,id):
        post = PostModel.query.get(id)
        if post is None:
            return {'message': 'Post not found'}
 
        return {"data":[tag.id for tag in post.tags]}

