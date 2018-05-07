from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from flask_ckeditor import CKEditorField

"""-----------------WTF FORMS-----------------"""

#ARTICLE FORM CLASS
class PostForm(FlaskForm):

    title = StringField ('Title', validators=[DataRequired()])
    subtitle = StringField ('Subtitle', validators=[DataRequired()])
    author = StringField ('Author', validators=[DataRequired()])
    content = CKEditorField ('Content', validators=[DataRequired()])

#LOGIN FORM CLASS
class LoginForm(FlaskForm):

    username = StringField (_l('Username'), validators=[DataRequired()])
    password = PasswordField (_l('Password'), validators=[DataRequired()])
