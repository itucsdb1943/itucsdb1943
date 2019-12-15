from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request,flash,session,abort
from datetime import datetime as dt
from flask_login import LoginManager,login_user,login_required,current_user
from datetime import datetime
now = datetime.now()
from flask_login import logout_user
from passlib.apps import custom_app_context as pwd_context
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from classes.Users import *

site = Blueprint('site', __name__)
url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"



