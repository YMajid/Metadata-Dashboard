import os
from run import app
from flask import render_template, url_for, flash, redirect


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/tables")
def home():
    return render_template('tables.html')