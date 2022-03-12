from crypt import methods
from app import app
from flask import render_template, flash, redirect
from app.forms import PrimarySearchForm


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = PrimarySearchForm()
    if form.validate_on_submit():
        print(form.user_query.data)
    return render_template("index.html", form=form)
