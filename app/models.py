from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(64), unique = True)
  username = db.Column(db.String(64), unique = True)
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref = 'user')

  @property
  def password(self):
    raise AttributeError('password is not readable attribute')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<User %r>' %self.username

class Post(db.Model):
  __tablename__ = "posts"
  id = db.Column(db.Integer, primary_key = True)
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __repr__(self):
    return '<Post %r>' % (self.body)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
