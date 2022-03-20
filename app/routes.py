from flask import redirect, render_template, url_for, flash, request
from app import app, db
from werkzeug.urls import url_parse

# from wtforms.validators import DataRequired
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User

from app.forms import LoginForm, RegistrationForm


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/players")
def players():
    return render_template("players.html", title="Players Page")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Redirect if the user is authenticated already
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    # If form data passes validation, find the requested user
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # If no user found or the assword is incorrect,
        # return to login page with flashed message
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        # If all validations pass, login the user
        login_user(user, remember=form.remember_me.data)

        # If user attempted an authroized route prior to login,
        # return user to that route after successful login
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page) != "":
            next_page = url_for("secret")

        return redirect(next_page)

    # Else, return login.html
    return render_template("login.html", title="Login Page", form=form)


# Logout user route; must be logged in to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Protected route example
@app.route("/secret")
@login_required
def secret():
    return render_template("secret.html", title="Secret Page")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)
