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

@site.route("/register", methods=['GET','POST'])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = request.form
        name = form['name']
        surname = form['surname']
        email = form['email']
        password = form['password']
        hashed = hasher.hash(password)
        facebook = form['facebook']
        twitter = form['twitter']
        instagram = form['instagram']
        youtube = form['youtube']
        website = form['website']
        if form.get('isVet'):
            isVet = 1
        else:
            isVet = 0
        photoUrl = form['ck2']
        registerTime = now.strftime("%d/%m/%y %H:%M:%S")
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            try:
                statement = """INSERT INTO Users(NAME, SURNAME, EMAIL,ISVET,PASSWORD,PHOTO,REGISTERDATE)
                VALUES (%s,%s,%s,%s,%s,%s,%s); """
                cursor.execute(statement,(name,surname,email,isVet,hashed,photoUrl,registerTime))
            except:
                return render_template("register.html",message = "The email address is already used!")

        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """ SELECT USERID FROM USERS WHERE EMAIL = '{0}' """.format(email)
            cursor.execute(statement)
            userid = cursor.fetchone()[0]        
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO SOCIALMEDIA(OWNERID,FACEBOOK,TWITTER,INSTAGRAM,YOUTUBE,WEBSITE)
                            VALUES('{0}','{1}','{2}','{3}','{4}','{5}') """.format(userid,facebook,twitter,instagram,youtube,website)
            cursor.execute(statement)        
        next_page = request.args.get("next", url_for("login_page"))
        return redirect(next_page)

@site.route("/login", methods=['GET','POST'])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = request.form
        username = form['username']
        password = form['password']
        user = get_user(username)
        if user is not None:
            if hasher.verify(password, user.password):
                login_user(user,remember=True,force=True) 
                print(current_user)
                print("you logged")
                session['logged_in'] = True
                session['user_id'] = current_user.id
                print(session['user_id'])
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                print("you cant logged")
                flash("You cant logged in.")
                return render_template("login.html",message="You entered wrong password! Try Again")
        else:
            return render_template("login.html",message="User cannot be found. If you don't have an account, you can register")

