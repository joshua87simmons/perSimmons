from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class PostForm(Form):
  title = StringField('Title', validators = [Required()])
  body = TextAreaField('Body', validators = [Required()])
  submit = SubmitField('Submit Post')
