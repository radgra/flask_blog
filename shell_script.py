from db import db
from app import app
from models.category import CategoryModel
from models.post import PostModel
from models.tag import TagModel

def run_shell():
    db.init_app(app)
    app.app_context().push()


def seed_all():
    db.create_all()
    # Categories
    sport = CategoryModel(name="Sport")
    politics = CategoryModel(name="Politics")   
    db.session.add(sport)
    db.session.add(politics)
    db.session.commit()

    # Posts
    post1 = PostModel(title="Some post about sport")
    post1.category = sport
    post2 = PostModel(title="Politics sucks etc")
    post2.category = politics

    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    # Tags
    tag1 = TagModel(name="Trump")
    tag2 = TagModel(name="Real Madrid")
    tag3= TagModel(name="Champtions League")
    tag4= TagModel(name="World Affairs")

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)
    db.session.commit()
