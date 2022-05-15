# from turtle import title
from flask import render_template

from app.request import get_quote
from . import main
from ..request import get_quote



@main.route('/')
def index():
    title = 'P-BLOG'
    header = get_quote()

    return render_template('index.html',title=title,quote=header)




