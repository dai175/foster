import os

SECRET_KEY = os.urandom(32)

SQLALCHEMY_DATABASE_URI = 'postgres://user:password@localhost:5432/foster'
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'static/images'

LOGIN_URI = 'https://{}/authorize?audience={}' \
            '&response_type=token&client_id={}&redirect_uri={}'. \
    format('foster-an-animal.auth0.com',
           'foster',
           '4l2ZyAy8tb0i85R5CT32MaiUUt5dE0iD',
           'http://localhost:8080/login-results'
           )

LOGOUT_URI = 'http://localhost:8080/logout'
