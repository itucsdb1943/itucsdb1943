# coding=utf-8
import os
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

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')



#For uploading photo
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/patigram')
ALLOWED_EXTENSIONS = {  'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER_NOTICE = join(dirname(realpath(__file__)), 'static/notice')

app = Flask(__name__)
app.register_blueprint(site)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_NOTICE'] = UPLOAD_FOLDER_NOTICE 
app.app_context()

lm = LoginManager()

@lm.user_loader
def load_user(id):
    return get_user(id)

url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"
 
db = Database(url)
app.config["db"] = db

@app.route("/delete")
def delete_user():
    db.delete_notifications(session['user_id'])
    db.delete_notices(session['user_id'])
    db.delete_socialMedia(session['user_id'])
    db.delete_user_comments(session['user_id'])
    db.delete_user_likes(session['user_id'])
    db.delete_post(session['user_id'])
    db.delete_user_rating(session['user_id'])
    db.delete_user(session['user_id'])
    session['logged_in'] = False
    next_page = request.args.get("next", url_for("home_page"))
    return redirect(next_page)

@app.route("/")
def home_page():
    return render_template("home.html")
@app.route("/login", methods=['GET','POST'])
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
                session['logged_in'] = True
                session['user_id'] = user.id
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

@app.route("/register", methods=['GET','POST'])
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
        # next_page = request.args.get("next", url_for("login_page"))
        return redirect(url_for("login_page"))

@app.route("/logout")
def logout_page():
    session['logged_in'] = False
    next_page = request.args.get("next", url_for("home_page"))
    return redirect(next_page)

@app.route("/post")
def post_page():
    return "Post page"

@app.route("/profile")
def profile_page():
    user = db.get_user_detail(session['user_id'])
    return render_template("profile.html",user = user)

@app.route("/profile/<int:userid>")
def other_profile_page(userid):
    user = db.get_user_detail(userid)
    return render_template("othersProfile.html",user = user)

@app.route("/blog")
def blog_page():
    return render_template("blog/blog.html")

@app.route("/blog/bloginfo")
def blog_info_page():
	return render_template("blog/bloginfo.html")

@app.route("/blog/add")
def blog_add_page():
	return "add blog"

@app.route("/findvet", methods=["GET", "POST"])
def findVet_page():
    if session['logged_in'] == False:
       return redirect(url_for("login_page"))
    else:        
        db = current_app.config["db"]
        # db.create_initial_cities() 
        # db.create_initial_vets() # This function should be used after deleting all vets
        now_user = session['user_id']
        if request.method == "GET":
            vets = db.get_vets()
            #db.create_initial_vets()
            for vet in vets:
                print(vet["cityname"])
                score = vet["score"]
                score = score * 20
                vet["score"] = score
            cities = db.get_vet_cities()
            return render_template("findVet/findVet.html", vets=vets,cities=cities if cities else None, now_user = now_user)
        else:
            form_id = request.form["city_select"]
            if form_id == "0":
                vets = db.get_vets()
                selected_city = 0
            else:
                selected_city = db.get_cityname(form_id)
                vets = db.get_selected_vets(form_id)
                for vet in vets:
                    print(vet["cityname"])
                    score = vet["score"]
                    score = score * 20
                    vet["score"] = score
                cities = db.get_vet_cities()
            return render_template("findVet/findVet.html", vets=vets,  cities=cities  if cities else None, selected_city=selected_city, now_user = now_user)


@app.route("/findVet/<int:vet_key>", methods=["GET","POST"])
def vet_custom_page(vet_key):
    db = current_app.config["db"]
    if request.method == "POST":
        form_comment = request.form["comment"]
        now_id = request.form["add"]
        now_id = session['user_id']
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        db.update_rating(vet_key, now_id, form_comment,date_time)

    now_user = session['user_id']
    vet = db.get_vet(vet_key)
    vet.overallScore = int(vet.overallScore)
    vet.priceRate = int(vet.priceRate)
    vet.serviceRate = int(vet.serviceRate)
    # print(vet.vetName)
    rates = db.get_rates(vet_key)
    return render_template("findVet/vet_custom_page.html", vet=vet,rates=rates, now_user = now_user)


@app.route("/findVet/delete/<int:vet_id>")
def delete_vet(vet_id):
    db = current_app.config["db"]
    db.delete_vet(vet_id)
    return redirect(url_for("findVet_page"))

@app.route("/findVet/evaluation/<int:vet_key>",methods=["GET","POST"])
def vet_evaluation_page(vet_key):
    db = current_app.config["db"]
    if request.method == "GET":
        vet = db.get_vet(vet_key)
        vet.overallScore = int(vet.overallScore)
        vet.priceRate = int(vet.priceRate)
        vet.serviceRate = int(vet.serviceRate)
        return render_template("findVet/vet_evaluation_page.html", vet=vet)
    else:
        form_title = request.form["title"]
        form_comment = request.form["comment"]
        form_overall = request.form["overallScore"]
        form_price = request.form["priceRate"]
        form_service = request.form["serviceRate"]
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        vetid = vet_key 
        userid = session['user_id']
        rateid = 1 # Just for errors, not real value. Sql will give real rateid
        new_rate = Rate(rateid, userid, vetid, form_overall, form_price, form_service, form_comment, form_title, date_time)
        
        db.add_rate(new_rate)
        vet = db.get_vet(vet_key)
        print(vet.overallScore)
        vet.overallScore = int(vet.overallScore)
        vet.priceRate = int(vet.priceRate)
        vet.serviceRate = int(vet.serviceRate)
        rates = db.get_rates(vet_key)
        return render_template("findVet/vet_custom_page.html", vet=vet, rates=rates, success="Success",now_user = userid)
@app.route("/foundation")
def foundation_page():
    return render_template("foundation/foundation.html")

@app.route("/notice/lost")
def notice_page():
    db = current_app.config["db"]
    notices = db.get_notices(1)    
    return render_template("notices.html",notices = sorted(notices, reverse=True),header="Lost Pet Notices")

@app.route("/notice/owner")
def owner_notice_page():
    db = current_app.config["db"]
    notices = db.get_notices(0)    
    return render_template("notices.html",notices = sorted(notices, reverse=True),header="Find Owner Notices")

@app.route("/notice/<int:noticeID>")
def noticeDetail_page(noticeID):
    db = current_app.config["db"]
    notice = db.get_notice(noticeID)
    print(notice.photoURL)
    return render_template("noticeDetail.html",notice=notice)

@app.route("/notice/edit/<int:noticeid>",methods=["GET", "POST"])
def notice_edit_page(noticeid):
    if request.method == "GET":    
        return render_template("noticeEdit.html")
    else:
        form = request.form
        title = form['name']
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        print(date_time)
        db.update_notice(noticeid,title,date_time)
        next_page = request.args.get("next", url_for("notice_page"))
        return redirect(next_page)



@app.route("/notice/add", methods=['GET','POST'])
def noticeAdd_page():
    if request.method == "GET":        
        return render_template("noticeAdd.html")
    else:
        errors = {}
        form = request.form
        file = request.files["image"]
        if file.filename == '':           
            errors["file"] = "An image is necessary for notice, please give one."
            return  render_template("patigram/patigramAdd.html", errors=errors)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_NOTICE'], filename))
            form_photo = filename
        
        photoUrl = "../static/notice/" + form_photo
        title = form['title']
        animalType = form['animalType']
        place = form['place']
        gender = form['gender']
        strain = form['strain']        
        age = request.form.get('age')
        agee = int(age)
        isLost = request.form['tag']
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        contact = form['phone']
        db.add_notice(title,place,animalType,gender,strain,agee,photoUrl,isLost,contact,date_time,session['user_id'])
        return render_template("noticeAdd.html")
 
@app.route("/forum")
def forum_page():
    return "Forum page"

@app.route("/forum/add")
def forum_add_page():
    return "Forum add page"

@app.route("/patigram/like/<int:post_key>")
def patigram_like(post_key):
    db =current_app.config["db"]
    userid = session['user_id']
    date_time = now.strftime("%d/%m/%y %H:%M:%S")
    db.patigram_add_like(post_key, userid, date_time)
    post = db.get_post(post_key)
    db.add_notification(1,post.title,0,userid,post.userid,"",date_time)
    return redirect(url_for("patigram_page"))

@app.route("/patigram/likedel/<int:post_key>")
def patigram_delete_like(post_key):
    db = current_app.config["db"]
    userid = session['user_id']
    db.patigram_delete_like(post_key, userid)
    return redirect(url_for("patigram_page"))


@app.route("/patigram/<int:post_key>")
def patigram_custom_page(post_key):
    db = current_app.config["db"]
    post = db.get_post(post_key)
    patigram_post_type = 0
    likenum = db.patigram_get_like_num( post_key)
    now_user = session['user_id']
    post_user = db.get_post_user(post_key)
    is_user_post = 2
    #now_user = now_user[0]

    print(type(now_user))
    print(type(post_user))
    if int(now_user) == post_user:
        is_user_post = 1
    else:
        is_user_post = 0
    print(is_user_post)
    post.userid = db.get_user_name(post.userid)
    comments = db.get_comments(patigram_post_type,post_key)
    if post is None:
        abort(404) #This should be defined
    userid = post_user
    return render_template("patigram/patigram_custom.html", post=post, comments = comments, is_user_post = is_user_post, likenum = likenum, userid=userid)

@app.route("/patigram", methods=["GET", "POST"])
def patigram_page():
    patigrams = []
    if request.method == "GET":
        db = current_app.config["db"]
        posts = db.get_posts()
        userNow = session['user_id']
        for postkey,post in posts:
            post.userid = db.get_user_name(post.userid)
            isliked = db.patigram_is_user_liked(post.postid, userNow)
            print(isliked)
            getlike = db.patigram_get_like_num(post.postid)
            patigrams.append((postkey,(post,getlike,isliked)))
        return render_template("patigram/patigram.html", patigrams=sorted(patigrams, reverse=True))
    else:
        form_comment = request.form["comment"]
        userid = session['user_id']
        commentid = 1 # Just for errors
        form_postid = request.form["add"]    
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        post_type = 0
        db = current_app.config["db"]
        db.add_comment(Comment(commentid, form_postid, userid, date_time, form_comment, post_type))
        post = db.get_post(form_postid)
        db.add_notification(1,post.title,1,userid,post.userid,form_comment,date_time)
        return redirect(url_for("patigram_custom_page", post_key=form_postid))

@app.route("/patigram/delete/<int:post_key>")
def patigram_delete(post_key):
    db = current_app.config["db"]
    post = db.get_post(post_key)
    db.delete_patigram(post_key)
    userid = session['user_id']
    date_time = now.strftime("%d/%m/%y %H:%M:%S")
    db.add_notification(1,post.title,3,userid,userid,"",date_time)

    return redirect(url_for("patigram_page"))

@app.route("/patigram/update/<int:post_key>", methods =["GET", "POST"])
def patigram_update(post_key):
    if request.method == "GET":
        return render_template("patigram/patigramUpdate.html", post_key = post_key)
    else:
        db = current_app.config["db"]
        old_post = db.get_post(post_key)
        # is_title = request.form["title"]
        # is_desc = request.form["description"]
        form_titlerr =  request.form.get("title_sentence", "").strip()
        if len(form_titlerr) == 0 and "title" in request.form:
            return render_template("patigram/patigramUpdate.html", error = 1)

        form_title = request.form["title_sentence"]
        form_description = request.form["description_sentence"]
        if "title" in request.form and "description" in request.form:
            db.update_patigram(post_key, request.form["title_sentence"], request.form["description_sentence"])
            print("a")
        elif "title" in request.form:
            db.update_patigram(post_key, request.form["title_sentence"], old_post.description)
            print("ab")
        elif "description" in request.form:
            db.update_patigram(post_key, old_post.title, request.form["description_sentence"])
            print("abc")
        return redirect(url_for("patigram_custom_page", post_key = post_key))
# Checking extensions of loaded file
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/patigram/add", methods=["GET","POST"])
def patigram_add_page():
    if request.method == "GET":
        return render_template("patigram/patigramAdd.html")
    else:
        errors = {}

        file = request.files["image"]

        if file.filename == '':
            errors["file"] = "An image is necessary for patigram post, please give one."
            return  render_template("patigram/patigramAdd.html", errors=errors)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            form_photo = filename
        form_title =  request.form.get("title", "").strip()
        if len(form_title) == 0:
            errors["title"] = "You should give a title to patigram post, please give one."
            return  render_template("patigram/patigramAdd.html", errors=errors)
        form_title = request.form['title']

        form_description = request.form["description"]
        form_tag = request.form["tag"]

        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        user_id = session['user_id']
        post_id = 3 # I don't use it, just for errors
        post = Post(post_id,user_id,date_time,form_photo,form_title,description=form_description if form_description else None, posttag=form_tag if form_tag else None)
        db = current_app.config["db"]
        post_key = db.add_post(post)
        db.add_notification(1,form_title,2,user_id,user_id,"",date_time)
        return redirect(url_for("patigram_custom_page", post_key=post_key))

@app.route("/notifications")
def notifications_page():
    notifications = db.get_notifications()
    db.notification_seen(session['user_id'])
    return render_template("notifications.html",notifications = sorted(notifications, reverse=True))

@app.route("/avatar", methods=["GET","POST"])
def change_avatar():
    if request.method == "GET":
        return render_template("avatarChange.html")
    else:
        form = request.form
        photoUrl = form['ck2']
        print(photoUrl)
        db.update_user_photo(session['user_id'],photoUrl)
        return redirect(url_for("profile_page"))


@app.route("/notification/add")
def notification_add_page():
    return "not add"

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    app.run(debug=True)
    