from db import db

class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    posts = db.relationship('PostModel')

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
        }

    def json_detail(self):
        return {
            "id":self.id,
            "name":self.name,
            'posts':[post.json() for post in self.posts]
        }