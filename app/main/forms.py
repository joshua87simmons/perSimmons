from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class PostForm(Form):
  title = StringField('Title', validators = [Required()])
  body = PageDownField("What's on ya mind?", validators = [Required()])
  submit = SubmitField('Submit Post')
