from dotenv import dotenv_values


class Config(object):
    SECRET_KEY = "myamazinglycomplexsecretkeythatnoonewilleverguess"
    SQLALCHEMY_DATABASE_URI = dotenv_values(".env.CONNECTION_STRING")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TESTING = True
