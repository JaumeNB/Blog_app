from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_ckeditor import CKEditorField
from app.models import Editors, Tags
from app import app

"""-----------------WTF FORMS-----------------"""

#ARTICLE FORM CLASS
class PostForm(FlaskForm):

    title = StringField ('Title', validators=[DataRequired()])
    subtitle = StringField ('Subtitle', validators=[DataRequired()])
    author = StringField ('Author', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    content = CKEditorField ('Content', validators=[DataRequired()])

    def validate_tags(self, tags):

        app.logger.info("validation")

        unregistered_tab = False
        unregistered_tab_list = []
        separated_tags = str(tags.data).split("-")
        db_tags_objects = Tags.query.all()

        db_tags = []
        for db_tag_object in db_tags_objects:
            db_tags.append(db_tag_object.name)

        for single_tag in separated_tags:
            if single_tag not in db_tags:
                app.logger.info(str(single_tag) + " is not in the DB, register it")
                unregistered_tab = True
                unregistered_tab_list.append(single_tag)

        if unregistered_tab:
            raise ValidationError('Unregistered tab found: ' + str(unregistered_tab_list))
        else:
            app.logger.info("tags are validated")

#LOGIN FORM CLASS
class LoginForm(FlaskForm):

    username = StringField ('Username', validators=[DataRequired()])
    password = PasswordField ('Password', validators=[DataRequired()])

#TAB FORM CLASS
class TagForm(FlaskForm):

    name = StringField ('Name', validators=[DataRequired()])

    def validate_name(self, name):

        db_tags_objects = Tags.query.all()
        db_tags = []

        for db_tag_object in db_tags_objects:
            db_tags.append(db_tag_object.name)

        app.logger.info(db_tags)
        app.logger.info(name)

        if str(name.data) in db_tags:
            app.logger.info(str(name.data) + " is already in the DB")
            raise ValidationError('tag is already in the DB')
        else:
            app.logger.info("tag is validated")
