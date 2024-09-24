from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '<KEY>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

"""
flask db init

flask db migrate
flask db upgrade
"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


@app.route('/', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/', methods=['POST'])
def post_create():
    title = request.form['title']
    text = request.form['text']
    image = request.files['image']
    image.save(f'static/images/{image.filename}')
    post = Post(title=title, content=text, image=f'/static/images/{image.filename}')
    db.session.add(post)
    db.session.commit()
    return {'image_path': f'/static/images/{image.filename}'}


@app.route('/post/<int:id>', methods=['GET'])
def show_post(id):
    post = Post.query.get(id)
    comments = Comment.query.filter_by(post=post.id)
    return render_template('post_details.html', post=post, comments=comments)


@app.route('/post/<int:id>/add-comment/', methods=['POST'])
def post_add_comment(id):
    text = request.form['comment']
    comment = Comment(text=text, post=id)
    db.session.add(comment)
    db.session.commit()
    return {}
