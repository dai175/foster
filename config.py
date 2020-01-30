import os

SECRET_KEY = os.urandom(32)

SQLALCHEMY_DATABASE_URI = 'postgres://user:password@localhost:5432/foster'
SQLALCHEMY_TRACK_MODIFICATIONS = False
