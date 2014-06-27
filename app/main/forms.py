from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class PostForm(Form):
  title = StringField(validators = [Required()])
  body = PageDownField(validators = [Required()])
  submit = SubmitField('Submit')
