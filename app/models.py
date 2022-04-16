import logging
from sqlalchemy.exc import SQLAlchemyError
from app import db, login  # noqa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


logging.basicConfig(filename="errors.log")


@login.user_loader
def load_user(id):
    try:
        user = User.query.get(int(id))
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        logging.error(error)

    return user


class User(UserMixin, db.Model):  # type: ignore #noqa
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    favorite_players = db.relationship("Favorite", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, "sha256", 12)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Favorite(db.Model):  # type: ignore #noqa
    __tablename__ = "favorites"

    userID = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey("people.playerID"), primary_key=True)

    def __repr__(self):
        return "<Favorites {} {}>".format(self.userID, self.playerID)


class Pitching(db.Model):  # type: ignore #noqa
    __tablename__ = "pitching"

    ID = db.Column("ID", db.Integer, primary_key=True)
    playerID = db.Column("playerID", db.String(9), unique=True)
    yearID = db.Column("yearID", db.Integer)

    def __repr__(self):
        return "<Pitching {} {}>".format(self.playerID, self.yearID)


class PitchingAnalytics(db.Model):  # type: ignore #noqa
    __tablename__ = "pitchinganalytics"

    analytics_ID = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.String(255), unique=True)
    yearID = db.Column(db.Integer)
    stint = db.Column(db.Integer)
    teamID = db.Column(db.String(3))
    team_ID = db.Column(db.Integer)
    lgID = db.Column(db.String(2))
    TB = db.Column(db.Integer)
    TW = db.Column(db.Numeric)
    SS = db.Column(db.Numeric)
    TOB = db.Column(db.Integer)
    BA = db.Column(db.Numeric)
    PA = db.Column(db.Integer)
    RC = db.Column(db.Numeric)
    PARC = db.Column(db.Numeric)
    PARC27 = db.Column(db.Numeric)
    PARCA = db.Column(db.Numeric)

    def __repr__(self):
        return "<Pitching Analytics {}>".format(self.playerID)


class People(db.Model):  # type: ignore #noqa
    __tablename__ = "people"

    playerID = db.Column(db.String(9), primary_key=True)
    nameFirst = db.Column("nameFirst", db.String(255))
    nameLast = db.Column("nameLast", db.String(255))
    finalGameDate = db.Column("finalgame_date", db.Date())

    def __repr__(self):
        return "<People {}>".format(self.playerID)


class Analysis(db.Model):  # type: ignore # noqa
    __tablename__ = "analysis"  # required

    analysis_ID = db.Column(db.Integer, primary_key=True)  # required
    playerid = db.Column(db.String(9))
    yearID = db.Column(db.Integer)
    G = db.Column(db.Integer)
    AB = db.Column(db.Integer)
    R = db.Column(db.Integer)
    H = db.Column(db.Integer)
    B2 = db.Column("2B", db.Integer)
    B3 = db.Column("3B", db.Integer)
    HR = db.Column(db.Integer)
    RBI = db.Column(db.Integer)
    SB = db.Column(db.Integer)
    CS = db.Column(db.Integer)
    BB = db.Column(db.Integer)
    SO = db.Column(db.Integer)
    IBB = db.Column(db.Integer)
    HBP = db.Column(db.Integer)
    SH = db.Column(db.Integer)
    SF = db.Column(db.Integer)
    GIDP = db.Column(db.Integer)
    OBP = db.Column(db.Numeric)
    TB = db.Column(db.Integer)
    RC = db.Column(db.Numeric)
    RC27 = db.Column(db.Numeric)

    def __repr__(self):
        return "<analysis(player='%s',RC27='%s')>" % (self.playerid, self.RC27)

    def setRC27(self):
        if self.RC is None:
            self.setRC()
        outs = (
            self.AB
            - self.H
            + self.coalesce(self.CS)
            + self.coalesce(self.SH)
            + self.coalesce(self.SF)
            + self.coalesce(self.GIDP)
        )
        self.RC27 = 27 * self.RC / outs
        db.session.commit()

    def setRC(self):
        if self.OBP is None:
            self.setOBP()
        if self.TB is None:
            self.setTB()
        self.RC = self.OBP * self.TB

    def setOBP(self):
        onbase = self.H + self.BB + self.coalesce(self.HBP)
        pa = self.AB + self.BB + self.coalesce(self.HBP) + self.coalesce(self.SF)
        if pa == 0:
            self.OBP = 0
        else:
            self.OBP = onbase / pa

    def setTB(self):
        self.TB = self.H + self.B2 + 2 * self.B3 + 3 * self.HR

    def coalesce(self, x):
        if x is None:
            return 0
        else:
            return x
