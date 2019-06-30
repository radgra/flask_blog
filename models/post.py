from db import db
from models.tag import post_tags

class PostModel(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    category = db.relationship('CategoryModel')
    tags = db.relationship('TagModel',secondary=post_tags, back_populates="posts")

    def json(self):
        return {
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "category_id":self.category_id
        }

    def json_detail(self):
        return {
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "category":self.category.json(),
            "tags":[tag.json() for tag in self.tags]
        }

    def json_with_includes(self, includes):
        includes_list = [x.strip() for x in includes.split(',')]

        obj_dict = self.json()

        if 'category' in includes_list:
            obj_dict['category'] = self.category.json()

        if 'tags' in includes_list:
            obj_dict['tags'] = [tag.json() for tag in self.tags]
        
        return obj_dict

    def __str__(self):
        return f'<self.title>'
    
    __repr__ = __str__
