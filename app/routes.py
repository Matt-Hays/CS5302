from flask import redirect, render_template, url_for, flash, request, session
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from werkzeug.urls import url_parse
from flask_login import current_user, login_required, login_user, logout_user
from app.models import Favorite, User, PitchingAnalytics, People
from app.forms import LoginForm, RegistrationForm, PlayerSearchForm

# **********
# INDEX PAGE
# **********


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    # Player Search by Name Form
    form = PlayerSearchForm()

    # Check that a form has been submitted
    if form.validate_on_submit():
        # Gather, trim, and split the search into a firstname and lastname
        search_query = form.player_search.data.split(" ")
        fName = search_query[0].strip().lower()
        lName = search_query[1].strip().lower()
        # Search by first and last name - recover the playerid
        playerID = (
            People.query.filter_by(nameFirst=fName, nameLast=lName).first().playerID
        )

        if playerID is not None:
            # If we have a playerid, search the pitchinganalytics table by the playerid
            players = PitchingAnalytics.query.filter_by(playerID=playerID).all()
            # Return the page with the necessary data to display
            return render_template(
                "index.html",
                players=players,
                nameFirst=fName,
                nameLast=lName,
                form=form,
            )

    # Return a blank page with the search form
    return render_template(
        "index.html",
        form=form,
    )


# ************
# PLAYERS PAGE
# ************
@app.route("/players")
def players():
    return render_template("players.html", title="Players Page")


# **********
# LOGIN PAGE
# **********
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
            next_page = url_for("account")

        return redirect(next_page)

    # Else, return login.html
    return render_template("login.html", title="Login Page", form=form)


# ************
# LOGOUT ROUTE
# ************
# Logout user route; must be logged in to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ************
# ACCOUNT PAGE
# ************
# Protected route example
@app.route("/account")
@login_required
def account():
    favorite_players = Favorite.query.filter_by(userID=session["_user_id"]).all()
    return render_template(
        "account.html", title="Secret Page", favorites=favorite_players
    )


# ******************
# REGISTRATION ROUTE
# ******************
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        # BEGIN TRANSACTION #

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            print(error)

        # END TRANSACTION #
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# ***************
# FAVORITES ROUTE
# ***************
@app.route("/favorites", methods=["POST"])
@login_required
def favorites():
    user = Favorite(userID=session["_user_id"], playerID=request.form["player_id"])

    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        print(error)

    return redirect(url_for("index"))
