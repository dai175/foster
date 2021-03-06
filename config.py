import os

SECRET_KEY = os.urandom(32)

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
                          'postgres://user:password@localhost:5432/foster'
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'static/images'

AUTH0_DOMAIN = 'foster-an-animal.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'foster'
CLIENT_ID = '4l2ZyAy8tb0i85R5CT32MaiUUt5dE0iD'
CALLBACK_URI = 'https://foster-an-animal.herokuapp.com/callback'

LOGIN_URI = 'https://{}/authorize?audience={}' \
            '&response_type=token&client_id={}&redirect_uri={}'. \
    format(AUTH0_DOMAIN, API_AUDIENCE, CLIENT_ID, CALLBACK_URI)
