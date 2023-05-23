import datetime
import os
import random
from flask import Blueprint, flash, redirect, render_template, abort, request, current_app, send_from_directory, url_for
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename

from samizdat.db import session
from samizdat.models import Category, Post
from samizdat.forms import EditorForm

bp = Blueprint('blog', __name__,
               template_folder='templates')


ALLOWED_EXT = {'png', 'jpeg', 'jpg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@bp.route('/')
@bp.route('/posts', methods=['GET', 'POST'])
def index():
    categories = session.query(Category).all()
    posts = session.query(Post).all()
    try:
        return render_template('feed.html', posts=posts, categories=categories)
    except TemplateNotFound:
        abort(404)
        
@bp.route('/posts-by-tag/<tag_id>')
def posts_by_tag(tag_id):
    posts = session.query(Post).filter(Post.category_id == tag_id).all()
    return render_template('posts.html', posts=posts)

@bp.route('/posts/create', methods=['GET', 'POST'])
def create():
    form = EditorForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.dirname(
                current_app.instance_path) + current_app.config['UPLOAD_FOLDER'], filename))

        header = request.form['header']
        content = request.form['content']
        post = Post()
        post.category_id = random.randint(1, 6)
        post.header = header
        post.content = content
        post.img = filename
        post.user_id = 1
        post.date = datetime.date.today()
        session.add(post)
        session.commit()
    return render_template('editor.html')


@bp.route('/posts/<post_id>')
def show(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    return render_template('show.html', post=post)


@bp.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
def update(post_id):
    if request.method == 'POST':
        header = request.form['header']
        content = request.form['content']
        post = session.query(Post).filter(Post.id == post_id).first()
        post.header = header
        post.content = content
        post.user_id = 1
        post.date = datetime.date.today()
        session.add(post)
        session.commit()
    return render_template('editor.html')


@bp.route('/posts/<post_id>/delete')
def destroy(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    session.delete(post)
    session.commit()
    return 'deleted'


@bp.route('/test')
def test():
    return 'lol'


    
