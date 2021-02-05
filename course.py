from app import app, db
from app.models import User, Post, Categs


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Categs': Categs}
