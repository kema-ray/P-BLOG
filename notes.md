auth=>forms
# from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
# from wtforms.validators import InputRequired,Email,EqualTo,Length
# from ..models import User

# class RegistrationForm(FlaskForm):
#     email = StringField('Your Email Address',validators=[InputRequired(),Email()])
#     username = StringField('Enter your username',validators = [InputRequired(),Length(min=5,max=20)])
#     password = PasswordField('Password',validators = [InputRequired(), EqualTo('password_confirm',
#     message = 'Passwords must match')])
#     password_confirm = PasswordField('Confirm Passwords',validators = [InputRequired()])
#     submit = SubmitField('Sign Up')

#     def validate_email(self,data_field):
#         if User.query.filter_by(email =data_field.data).first():
#             raise ValidationError('There is an account with that email')

#     def validate_username(self,data_field):
#         if User.query.filter_by(username = data_field.data).first():
#             raise ValidationError('That username is taken')

# class LoginForm(FlaskForm):
#     email = StringField('Your Email Address',validators=[InputRequired(),Email()])
#     password = PasswordField('Password',validators =[InputRequired()])
#     remember = BooleanField('Remember me')
#     submit = SubmitField('Sign In')
views.py=>auth
# from flask import render_template,redirect,url_for,flash,request
# from . import auth
# from flask_login import login_user,logout_user,login_required
# from ..models import User
# from .forms import RegistrationForm,LoginForm
# from .. import db

# @auth.route('/register',methods = ["GET","POST"])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(email = form.email.data, username = form.username.data,password = form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('auth.login'))
    
#     title = "New Account"
#     return render_template('auth/register.html',registration_form = form)

# @auth.route('/login',methods=['GET','POST'])
# def login():
#     login_form = LoginForm()
#     if login_form.validate_on_submit():
#         user = User.query.filter_by(email = login_form.email.data).first()
#         if user is not None and user.verify_password(login_form.password.data):
#             login_user(user,login_form.remember.data)
#             return redirect(request.args.get('next') or url_for('main.index'))

#         flash('Invalid username or Password')

#     title = "Blog login"
#     return render_template('auth/login.html',login_form = login_form,title=title)

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("main.index"))

base.html
{% extends 'bootstrap/base.html'%}
{% block navbar %}
    {% include 'navbar.html' %}
{% endblock %}
{% block styles%}
    {{ super() }}
    <link rel="stylesheet" href="{{url_for('static',filename='css/style.css')}}">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css"
    integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
{% endblock %}

## requests
import urllib.request,json
from . models import Quote

base_url='http://quotes.stormconsultancy.co.uk/random.json'

def get_quote():
    get_quote_url = base_url.format()
    with urllib.request.urlopen(get_quote_url) as url:
        quotes = url.read()
        get_quote_response = json.loads(quotes)
        quote_object = None
        if get_quote_response:
            quote=get_quote_response.get('quote')
            author=get_quote_response.get('author')
            quote_object = Quote(quote,author)
            print(quote_object)

    return quote_object

# app.init
from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bootstrap = Bootstrap()
db =  SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    #initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    #registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    return app