from flask import render_template, flash, redirect, url_for, request, session
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Categs, Post
from flask import request
from werkzeug.urls import url_parse

import os


def del_last_child(the_url):
    the_arr = the_url.split('/')
    the_arr.pop()
    return '/'.join(the_arr)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        f = request.files['image']
        f.save(os.path.join(del_last_child(app.instance_path), 'app/static/instance/img', secure_filename(f.filename)))
        url = f.filename
        post = Post(text=form.post.data, user_id=current_user.id, content=url, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    categs = Categs.query.order_by(Categs.name).all()
    return render_template('index.html', title='Home', form=form, posts=posts, categs=categs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    cur_user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=cur_user.id).order_by(Post.timestamp)
    categs = Categs.query.order_by(Categs.name).all()
    return render_template('user.html', user=cur_user, posts=posts, categs=categs)


@app.route('/category/<category>')
@login_required
def categ(category):
    cur_categ = Categs.query.filter_by(name=category).first_or_404()
    posts = Post.query.filter_by(category=cur_categ.id)
    categs = Categs.query.order_by(Categs.name).all()
    return render_template('category.html', posts=posts, categs=categs, category=cur_categ.name)
