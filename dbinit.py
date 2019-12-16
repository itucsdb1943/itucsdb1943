import os
import sys
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
import sys
from datetime import datetime as dt
from os.path import dirname, join, realpath

import psycopg2 as dbapi2
from flask import (Blueprint, Flask, current_app, flash, redirect,
                   render_template, request, session, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from passlib.apps import custom_app_context as pwd_context
from passlib.hash import pbkdf2_sha256 as hasher
from werkzeug.utils import secure_filename
from classes.comment import *
from classes.Database import Database
from classes.forms import *
from classes.post import *
from classes.rate import *
from classes.Users import *
from views import site
from datetime import datetime as dt
from datetime import datetime
try:
    from urllib.parse import urlparse as up
except ImportError:
     from urlparse import urlparse as up

now = datetime.now()

app = Flask(__name__)
from flask import (Blueprint, Flask, current_app, flash, redirect,
                   render_template, request, session, url_for)
import psycopg2 as dbapi2
import server
lm = LoginManager()

INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    "INSERT INTO DUMMY VALUES (42)",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    app.secret_key = 'super secret key'
    lm.init_app(app)
    lm.login_view = "login_page"
    if url is None:
        sys.exit(1)
    initialize(url)
