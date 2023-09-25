from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from store.models import Customer
class RegisterForm(FlaskForm):
    #note the naming of the func, it must be of form: validate_nameoffield
    def validate_email(self,email_check):
        email = Customer.query.filter_by(email=email_check.data).first()
    #we check if there is a user with a specific email already
        if email:
            raise ValidationError("User with email already exists")
    name = StringField(label='Your name', validators=[Length(min=1, max=600),DataRequired()])
    email = StringField(label='email',validators=[Email(),DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6),DataRequired()])
    amount_in_acc =  IntegerField(label='Current amount',validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password',validators=[EqualTo('password'),DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    email = StringField(label='enteremail',validators=[Email(),DataRequired()])
    password = PasswordField(label='enterpassword', validators=[DataRequired()])
    submit = SubmitField(label="Log in")


class BuyProductForm(FlaskForm):
    submit = SubmitField(label="Buy Product")

class CartForm(FlaskForm):
    submit = SubmitField(label="Add to cart")

class SearchForm(FlaskForm):
    name = StringField(label = 'enter a brand,type or specific product')
    submit = SubmitField(label="Search")
