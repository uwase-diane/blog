from flask_wtf import  FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required, Email
from wtforms import ValidationError
from ..models import Subscription

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField('Title',validators = [Required()])
    description = TextAreaField('Description',validators = [Required()])
   
    submit = SubmitField('submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment',validators=[Required()])
    submit = SubmitField('Comment')

class UpdateBlogForm(FlaskForm):
    title = StringField('Title',validators = [Required()])
    description = TextAreaField('Description',validators = [Required()])
    
    submit = SubmitField('submit')

class SubscriptionForm(FlaskForm):
    email = StringField('Email',validators = [Required(),Email()])
    submit =  SubmitField('Submit')

    def validate_email(self,data_field):
        if Subscription.query.filter_by(email = data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_name(self,data_field):
        if Subscription.query.filter_by(name = data_field.data).first():
            raise ValidationError('That name is taken')     
