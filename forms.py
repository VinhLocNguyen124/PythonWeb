from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

class SignUpForm(FlaskForm):
    inputFirstName = StringField('First Name',
        [DataRequired(message="Please enter your first name!")])
    inputLastName = StringField('Last Name',
        [DataRequired(message="Please enter your last name!")])
    inputEmail = StringField('Email Address',
        [Email(message="Not a valid email address!"),
        DataRequired(message="Please enter your email address!")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Please enter your password"),
        EqualTo('inputConfirmPassword',message="Password doesnt match!")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')

    # [Email(message="Not a valid email address!"),

class SignInForm(FlaskForm):
    inputEmail = StringField('Email Address',
        [Email(message="Not a valid email address!"),
        DataRequired(message="Please enter your email address!")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Please enter your password")])
    submit = SubmitField('Sign In')

class ProjectForm(FlaskForm):
    inputProjectName = StringField('Project Name',
        [DataRequired(message="Please enter project name!")])
    submit = SubmitField('Save Project')

class TaskForm(FlaskForm):
    inputDescription = StringField('Task Description',
        [DataRequired(message="Please enter ur task content!")])
    inputPriority = SelectField('Priority', coerce = int)
    submit = SubmitField('Save Task')


