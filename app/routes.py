from flask import redirect, render_template, url_for, flash, request, session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from app import app, db
from werkzeug.urls import url_parse
from flask_login import current_user, login_required, login_user, logout_user
from app.models import Favorite, Pitching, User, PitchingAnalytics, People
from app.forms import LoginForm, RegistrationForm, PlayerSearchForm
import logging

# We're going to use Python's logging to ahndle any errors
logging.basicConfig(filename="errors.log")

# **********
# INDEX PAGE
# **********
@app.route("/", methods=["GET", "POST"])  # noqa: E302
@app.route("/index", methods=["GET", "POST"])
def index():
    # Player Search by Name Form
    form = PlayerSearchForm()

    # Check that a valid form has been submitted
    if form.validate_on_submit():
        # Gather, trim, and split the search into a firstname and lastname
        search_query = form.player_search.data.split(" ")
        fName = search_query[0].strip().lower()
        lName = search_query[1].strip().lower()

        # Search by first and last name - recover the playerid
        try:
            playerID = (
                People.query.filter_by(nameFirst=fName, nameLast=lName).first().playerID
            )
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logging.error(error)

        if playerID and playerID is not None:
            # If we have a playerid, search the pitchinganalytics table by the playerid
            try:
                players = PitchingAnalytics.query.filter_by(playerID=playerID).all()
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                logging.error(error)

            # Return the page with the necessary data to display
            return render_template(
                "index.html",
                players=players,
                nameFirst=fName,
                nameLast=lName,
                form=form,
            )

    # If there is no search, provide random default player pitching analytics.
    # NOTE: We query the pitching table to reduce the liklihood that we don't
    # have pitchingAnalytics for the response, then querying the People table
    # to obtain the first & last name.
    try:
        randPlayerId = (
            Pitching.query.filter(Pitching.yearID >= "1974")
            .order_by(func.rand())
            .first()
            .playerID
        )
        randPerson = People.query.filter_by(playerID=randPlayerId).first()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        logging.error(error)

    fName = randPerson.nameFirst
    lName = randPerson.nameLast

    # Ensure we have a valid query result
    if randPlayerId and randPlayerId is not None:
        # Query for the Pitching Analytics data
        try:
            randomPitchingStats = PitchingAnalytics.query.filter_by(
                playerID=randPlayerId
            ).all()
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logging.error(error)

        # If our data returns empty, provide a base case of Nolan Ryan
        if randomPitchingStats == []:
            # Try to query for pitching stats, catch any errors
            try:
                randomPitchingStats = PitchingAnalytics.query.filter_by(
                    playerID="ryanno01"
                ).all()
            except SQLAlchemyError as e:
                error = str(e.__dict__["orig"])
                logging.error(error)

            fName = "Nolan"
            lName = "Ryan"

        return render_template(
            "index.html",
            form=form,
            nameFirst=fName,
            nameLast=lName,
            players=randomPitchingStats,
        )

    # Return a blank page with the search form
    return render_template(
        "index.html",
        form=form,
    )


# **************
# FAVORITES PAGE
# **************
@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    # Calculate POSTs first to eliminate unecessary data accesses
    if request.method == "POST":
        try:
            user = Favorite(
                userID=session["_user_id"], playerID=request.form["player_id"]
            )
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logging.error(error)

        return redirect(url_for("index"))

    try:
        user_favorite_players = Favorite.query.filter_by(
            userID=session["_user_id"]
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        logging.error(error)

    fav_player_ids = []

    for idx in range(len(user_favorite_players)):
        fav_player_ids.append(user_favorite_players[idx].playerID)

    try:
        fav_players = People.query.filter(People.playerID.in_(fav_player_ids)).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        logging.error(error)

    # If arguments have been passed via URL params, display the data
    # NOTE: Query params are passed in via URL query string & used to query the database
    if request.args:
        playerid = request.args["playerid"]
        fName = request.args["firstName"]
        lName = request.args["lastName"]
        try:
            player = PitchingAnalytics.query.filter_by(playerID=playerid).all()
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logging.error(error)
        return render_template(
            "favorites.html",
            player_data=player,
            firstName=fName,
            lastName=lName,
            favorites=fav_players,
        )
    return render_template(
        "favorites.html",
        favorites=fav_players,
    )


# ******************
# REGISTRATION ROUTE
# ******************
@app.route("/register", methods=["GET", "POST"])
def register():
    # If user is alreayd logged in, return the user to the home page
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    # Determine if a valid form has been submitted
    if form.validate_on_submit():
        # Try to query for the user & add to db, catch any errors
        try:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logging.error(error)

        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


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
        # Try to query for the user, catch any errors
        try:
            user = User.query.filter_by(username=form.username.data).first()
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logging.error(error)

        # If no user found or the password is incorrect,
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
            next_page = url_for("favorites")

        return redirect(next_page)

    # Else, return login.html
    return render_template("login.html", form=form)


# ************
# LOGOUT ROUTE
# ************
# Logout user route; must be logged in to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
