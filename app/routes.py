from app import app
from flask import render_template, flash, redirect
from app.forms import PrimarySearchForm
from app.models import Analysis


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = PrimarySearchForm()
    if form.validate_on_submit():
        results = Analysis.query.filter_by(playerid=form.user_query.data).all()
        return render_template("index.html", form=form, results=results)
    return render_template("index.html", form=form)
