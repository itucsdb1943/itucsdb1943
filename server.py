import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from flask import Flask, render_template,request,session

from flask import Flask, render_template,request,session
import psycopg2 as dbapi2
from flask import current_app, redirect, Flask,url_for
from views import site
from flask_login import LoginManager,login_required,current_user
from classes.post import *
from classes.Database import Database
from flask_login import logout_user
from passlib.apps import custom_app_context as pwd_context
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from classes.Users import *
from classes.forms import *
from classes.comment import *
from classes.rate import *

from datetime import datetime
now = datetime.now()

#For uploading photo
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/patigram')
ALLOWED_EXTENSIONS = {  'png', 'jpg', 'jpeg', 'gif'}




try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
         
import psycopg2
app = Flask(__name__)
app.register_blueprint(site)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.app_context()
lm = LoginManager()

@lm.user_loader
def load_user(id):
    return get_user(id)

url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"

db = Database(url)
app.config["db"] = db

@app.route("/")
def home_page():
    print("geldik buralara")
    return render_template("home.html")

@app.route("/logout")
def logout_page():
    session['logged_in'] = False
    next_page = request.args.get("next", url_for("home_page"))
    return redirect(next_page)

@app.route("/post")
def post_page():
    return "Post page"

@app.route("/blog")
def blog_page():
    return render_template("blog/blog.html")

@app.route("/blog/bloginfo")
def blog_info_page():
	return render_template("blog/bloginfo.html")

@app.route("/blog/add")
def blog_add_page():
	return "add blog"

@app.route("/findvet")
def findVet_page():
    db = current_app.config["db"]
    vets = db.get_vets()
    #db.create_initial_vets()
    for vet in vets:
        print(vet["cityname"])
        score = vet["score"]
        score = score * 20
        vet["score"] = score
    return render_template("findVet/findVet.html", vets=vets)

@app.route("/findVet/<int:vet_key>")
def vet_custom_page(vet_key):
    db = current_app.config["db"]
    vet = db.get_vet(vet_key)
    vet.overallScore = int(vet.overallScore)
    vet.priceRate = int(vet.priceRate)
    vet.serviceRate = int(vet.serviceRate)
    # print(vet.vetName)
    rates = db.get_rates(vet_key)
    return render_template("findVet/vet_custom_page.html", vet=vet,rates=rates)

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
        userid = 12 # Should be handled
        rateid = 1 # Just for errors, not real value. Sql will give real rateid
        new_rate = Rate(rateid, userid, vetid, form_overall, form_price, form_service, form_comment, form_title, date_time)
        
        db.add_rate(new_rate)
        vet = db.get_vet(vet_key)
        print(vet.overallScore)
        vet.overallScore = int(vet.overallScore)
        vet.priceRate = int(vet.priceRate)
        vet.serviceRate = int(vet.serviceRate)
        rates = db.get_rates(vet_key)
        return render_template("findVet/vet_custom_page.html", vet=vet, rates=rates, success="Success")
@app.route("/foundation")
def foundation_page():
    return render_template("foundation/foundation.html")

@app.route("/notice")
def notice_page():
    db = current_app.config["db"]
    notices = db.get_notices()    
    return render_template("notices.html",notices = sorted(notices, reverse=True))

@app.route("/notice/<int:noticeID>")
def noticeDetail_page(noticeID):
    db = current_app.config["db"]
    notice = db.get_notice(noticeID)
    return render_template("noticeDetail.html",notice=notice) 

@app.route("/notice/add")
def announcementAdd_page():
    return "announcement add page"

@app.route("/forum")
def forum_page():
    return "Forum page"

@app.route("/forum/add")
def forum_add_page():
    return "Forum add page"

@app.route("/patigram/like/<int:post_key>")
def patigram_like(post_key):
    db =current_app.config["db"]
    userid = 1 # get from session
    date_time = now.strftime("%d/%m/%y %H:%M:%S")
    db.patigram_add_like(post_key, userid, date_time)
    return redirect(url_for("patigram_page"))

@app.route("/patigram/likedel/<int:post_key>")
def patigram_delete_like(post_key):
    db = current_app.config["db"]
    userid = 1; #get from session
    db.patigram_delete_like(post_key, userid)
    return redirect(url_for("patigram_page"))


@app.route("/patigram/<int:post_key>")
def patigram_custom_page(post_key):
    db = current_app.config["db"]
    post = db.get_post(post_key)
    patigram_post_type = 0
    likenum = db.patigram_get_like_num( post_key)
    now_user = 1 # Handle
    post_user = db.get_post_user(post_key)
    isusers_post = 2
    if now_user == post_user:
        isusers_post = 1
    else:
        isusers_post = 0
    post.userid = db.get_user_name(post.userid)
    comments = db.get_comments(patigram_post_type,post_key)
    if post is None:
        abort(404) #This should be defined
    return render_template("patigram/patigram_custom.html", post=post, comments = comments, is_user_post = isusers_post, likenum = likenum)

@app.route("/patigram", methods=["GET", "POST"])
def patigram_page():
    patigrams = []
    if request.method == "GET":
        db = current_app.config["db"]
        posts = db.get_posts()
        userNow = 1 #Handled in session
        for postkey,post in posts:
            post.userid = db.get_user_name(post.userid)
            isliked = db.patigram_is_user_liked(post.postid, userNow)
            print(isliked)
            getlike = db.patigram_get_like_num(post.postid)
            patigrams.append((postkey,(post,getlike,isliked)))
        return render_template("patigram/patigram.html", patigrams=sorted(patigrams, reverse=True))
    else:
        form_comment = request.form["comment"]
        userid = 1 # This should be handled
        commentid = 1 # Just for errors
        form_postid = request.form["add"]    
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        post_type = 0
        db = current_app.config["db"]
        db.add_comment(Comment(commentid, form_postid, userid, date_time, form_comment, post_type))
        return redirect(url_for("patigram_custom_page", post_key=form_postid))

@app.route("/patigram/delete/<int:post_key>")
def patigram_delete(post_key):
    db = current_app.config["db"]
    db.delete_patigram(post_key)
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
        user_id = 1
        post_id = 3 # I don't use it, just for errors
        post = Post(post_id,user_id,date_time,form_photo,form_title,description=form_description if form_description else None, posttag=form_tag if form_tag else None)
        db = current_app.config["db"]
        post_key = db.add_post(post)
        return redirect(url_for("patigram_custom_page", post_key=post_key))

@app.route("/notifications")
def notifications_page():
    return render_template("notifications.html")

@app.route("/notification/add")
def notification_add_page():
    return "not add"



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    lm.init_app(app)
    lm.login_view = "login_page"
    app.run(debug=True)
    print("geldik buralara3")
    session.pop('logged_in',None)
    #session['logged_in'] = False
    up.uses_netloc.append("postgres")
    print("geldik buralara3")
    url = up.urlparse(os.environ["postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"])
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
