from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from datetime import datetime
from markdown import markdown
import bleach
from . import db, login_manager

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(64), unique = True)
  username = db.Column(db.String(64), unique = True)
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post')

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

  @staticmethod
  def generate_test_blog(count=100):
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
      u = User(email=forgery_py.internet.email_address(),
        username=forgery_py.internet.user_name(True),
        password=forgery_py.lorem_ipsum.word())

      db.session.add(u)
      try:
        db.session.commit()
      except IntegrityError:
        db.session.rollback()

class Post(db.Model):
  __tablename__ = "posts"
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(64), unique = True)
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  body_html = db.Column(db.Text)

  def __repr__(self):
    return '<Post %r>' % (self.body)

  @staticmethod
  def generate_test_blog(count=100):
    from random import seed, randint
    import forgery_py

    seed()
    user_count = User.query.count()

    for i in range(count):
      u = User.query.offset(randint(0,
        user_count - 1)).first()
      p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),
      title=forgery_py.lorem_ipsum.word() + str(randint(1,1000)),
      timestamp=forgery_py.date.date(True))
      db.session.add(p)
      db.session.commit()

  @staticmethod
  def on_changed_body(target, value, oldvalue, initiator):
    allowed_tags = ['a', 'abbr', 'acronym',
    'b', 'blockquote', 'code',
    'em', 'i', 'li', 'ol', 'pre',
    'strong', 'ul', 'h1', 'h2', 'h3', 'p']

    target.body_html = bleach.linkify(bleach.clean(
    markdown(value, output_format='html'),
    tags=allowed_tags, strip=True))

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

db.event.listen(Post.body, 'set', Post.on_changed_body)
