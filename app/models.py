from app import db, login  # noqa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):  # type: ignore #noqa
    __tablename__ = "user"

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
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # player_id = db.Column(db.Integer, db.ForeignKey('people.playerid'))

    def __repr__(self):
        return "<User {}>".format(self.username)


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
