import os
from dashboard import app, dashboard_db
from flask import render_template, url_for, flash, redirect


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/tables")
def tables():
    return render_template('tables.html', title='Tables')

@app.route("/about")
def about():
    return render_template('about.html', title='About')
