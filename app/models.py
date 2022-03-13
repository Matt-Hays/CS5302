from app import db


# class User(db.Model):  # type: ignore # noqa
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))

#     def __repr__(self):
#         return "<User {}>".format(self.username)

class Analysis(db.Model): # type: ignore # noqa
	__tablename__ = "analysis" # required

	analysis_ID = db.Column(db.Integer,primary_key=True) # required
	playerid = db.Column(db.String(9))
	yearID = db.Column(db.Integer)
	G = db.Column(db.Integer)
	AB = db.Column(db.Integer)
	R = db.Column(db.Integer)
	H = db.Column(db.Integer)
	B2 = db.Column(db.Integer)
	B3 = db.Column(db.Integer)
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
		return "<analysis(player='%s',RC27='%s')>" % (self.playerid,self.RC27)

	def setRC27(self):
		if self.RC is None:
			self.setRC()	
		outs=self.AB-self.H+self.coalesce(self.CS)+self.coalesce(self.SH)+self.coalesce(self.SF)+self.coalesce(self.GIDP)
		self.RC27 = 27 * self.RC/outs
		db.session.commit()

	def setRC(self):
		if self.OBP is None:
			self.setOBP()
		if self.TB is None:
			self.setTB()
		self.RC = self.OBP * self.TB

	def setOBP(self):
		onbase = self.H+self.BB+self.coalesce(self.HBP)
		pa = self.AB+self.BB+self.coalesce(self.HBP)+self.coalesce(self.SF)
		if pa == 0:
			self.OBP = 0
		else:
			self.OBP = onbase/pa

	def setTB(self):
		self.TB = self.H+self.B2+2*self.B3+3*self.HR

	def coalesce(self,x):
		if x is None:
			return 0
		else:
			return x

