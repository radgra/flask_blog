from flask_restful import Resource, reqparse
from models.category import CategoryModel
from db import db
from sqlalchemy import exc

class CategoryList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Field 'name' is required")

    def get(self):
        # categories = CategoryModel.query.all()
        # return {'data': [cat.json() for cat in categories]}
        return {"data":"works"}

    def post(self):
        data = self.parser.parse_args()
        new_cat = CategoryModel(**data)

        try:
            db.session.add(new_cat)
            db.session.commit()
        except exc.IntegrityError as e:
            return {"message": e.args[0]}, 500
        except:
            return {"message": "Something went wrong"}, 500

        return {'data': new_cat.json()}

class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Field 'name' is required")

    def get(self, id):
        cat = CategoryModel.query.get(id)
        if cat:
            return {"data": cat.json_detail()}

        return {'message': 'Category not found'}

    def put(self, id):
        cat = CategoryModel.query.get(id)
        data = self.parser.parse_args()

        if cat:
            cat.name = data['name']
            try:
                db.session.commit()
                return {'data':cat.json()}
            except exc.IntegrityError as e:
                return {"message": e.args[0]}, 500
            except:
                return {"message": "Something went wrong"}, 500

        return {'message': 'Category not found'}

    def delete(self, id):
        cat = CategoryModel.query.get(id)
        if cat:
            db.session.delete(cat)
            db.session.commit()
            return {'message': 'Category deleted'}

        return {'message': 'Category not found'}
        