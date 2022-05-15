# from turtle import title
from crypt import methods
from flask import render_template

from app.request import get_quote
from . import main
from ..request import get_quote
from flask_login import login_required



@main.route('/')
def index():
    title = 'P-BLOG'
    header = get_quote()

    return render_template('index.html',title=title,quote=header)

@main.route('/blog/new',methods=["GET","POST"])
@login_required
def new_blog():

    return render_template('new_blog.html')


