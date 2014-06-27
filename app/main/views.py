from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash, current_app
from flask.ext.login import current_user, login_required
from . import main
from .. import db, login_manager
from .forms import PostForm
from ..models import User, Post

@main.route('/', methods = ['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.is_authenticated() and form.validate_on_submit():
      post = Post(title = form.title.data, body = form.body.data)
      db.session.add(post)
      flash('Post successfully submitted!')
      return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
    page,
    per_page=current_app.config['PERSIMMONS_POSTS_PER_PAGE'],
    error_out=False)

    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

@main.route('/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
  post = Post.query.filter_by(id=post_id).first()
  db.session.delete(post)
  db.session.commit()
  flash('Post has been deleted!')
  return redirect(url_for('.index'))

@main.route('/post/<int:id>')
def post(id):
  post = Post.query.get_or_404(id)
  return render_template('post.html', posts=[post])

@main.route('/about')
def about():
  return render_template('about.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  post = Post.query.get_or_404(id)
  form = PostForm()
  if form.validate_on_submit():
    post.body = form.body.data
    post.title = form.title.data
    db.session.add(post)
    flash('Your post has been edited!')
    return redirect(url_for('.post', id=post.id))
  form.body.data = post.body
  return render_template('edit_post.html', form=form, post=post)
