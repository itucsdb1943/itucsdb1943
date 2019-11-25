from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request,flash,session,abort
from datetime import datetime as dt
from flask_login import LoginManager,login_user,login_required,current_user
from flask_login import logout_user
from passlib.apps import custom_app_context as pwd_context
import psycopg2 as dbapi2

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
        hashedPassword = pwd_context.encrypt(password)
        facebook = form['facebook']
        twitter = form['twitter']
        instagram = form['instagram']
        youtube = form['youtube']
        website = form['website']
        isVet = form['isVet']
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO Users(NAME, SURNAME, EMAIL,ISVET,PASSWORD)
            VALUES (%s,%s,%s,1,%s); """
            cursor.execute(statement,(name,surname,email,hashedPassword))
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """ SELECT USERID FROM USERS WHERE EMAIL = '{0}' """.format(email)
            cursor.execute(statement)
            userid = cursor.fetchone()[0]        
            print(userid)
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO SOCIALMEDIA(OWNERID,FACEBOOK,TWITTER,INSTAGRAM,YOUTUBE,WEBSITE)
                            VALUES('{0}','{1}','{2}','{3}','{4}','{5}') """.format(userid,facebook,twitter,instagram,youtube,website)
            cursor.execute(statement)        
        return render_template("register.html")