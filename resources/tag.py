from flask_restful import Resource, reqparse
from models.tag import TagModel
from db import db
from sqlalchemy import exc


class TagList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name is required")

    def get(self):
        tags = TagModel.query.all()
        return {"data": [tag.json() for tag in tags]}

    def post(self):
        data = self.parser.parse_args()

        new_tag = TagModel(**data)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except exc.IntegrityError as e:
            return {"message": e.args[0]}, 500
        except:
            return {"message": "Something went wrong"}, 500

        return {"data": new_tag.json()}, 201


class Tag(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name is required")

    def get(self, id):
        tag = TagModel.query.get(id)
        if tag:
            return {"data": tag.json()}

        return {'message': 'Tag not found'}

    def put(self, id):
        tag = TagModel.query.get(id)
        data = self.parser.parse_args()

        if tag:
            tag.name = data['name']
            try:
                db.session.commit()
                return {'data':tag.json()}
            except exc.IntegrityError as e:
                return {"message": e.args[0]}, 500
            except:
                return {"message": "Something went wrong"}, 500

        return {'message': 'Tag not found'}

    def delete(self, id):
        tag = TagModel.query.get(id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Tag deleted'}

        return {'message': 'Tag not found'}
