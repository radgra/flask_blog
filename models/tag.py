from db import db

post_tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    posts = db.relationship('PostModel',secondary=post_tags, back_populates="tags")

    def json(self):
        return {
            "id":self.id,
            "name":self.name
        }