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

lm = LoginManager()

@lm.user_loader
def load_user(id):
    return get_user(id)

url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"


db = Database(url)
app.config["db"] = db

@app.route("/")
def home_page():
    print(current_user)
    return render_template("home.html")

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
    return "veteriner finding page"

@app.route("/foundation")
def foundation_page():
    return render_template("foundation/foundation.html")

@app.route("/notice")
def notice_page():
    return render_template("profile.html")

@app.route("/notice/add")
def announcementAdd_page():
    return "announcement add page"

@app.route("/forum")
def forum_page():
    return "Forum page"

@app.route("/forum/add")
def forum_add_page():
    return "Forum add page"

@app.route("/patigram/<int:post_key>")
def patigram_custom_page(post_key):
    db = current_app.config["db"]
    post = db.get_post(post_key)
    patigram_post_type = 0
    comments = db.get_comments(patigram_post_type,post_key)
    if post is None:
        abort(404) #This should be defined
    return render_template("patigram/patigram_custom.html", post=post, comments = comments)

@app.route("/patigram", methods=["GET", "POST"])
def patigram_page():
    if request.method == "GET":
        db = current_app.config["db"]
        posts = db.get_posts()
        return render_template("patigram/patigram.html", posts=sorted(posts, reverse=True))
    else:
        form_comment = request.form["comment"]
        userid = 1 # This should be handled
        commentid = 1 # Just for errors
        form_postid = request.form["add"]    
        date_time = now.strftime("%d/%m/%y/%H/%M/%S")
        post_type = 0
        db = current_app.config["db"]
        db.add_comment(Comment(commentid, form_postid, userid, date_time, form_comment, post_type))
        return redirect(url_for("patigram_custom_page", post_key=form_postid))



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
        # if request.form["cat"] is not None:
        #     form_tag = "cat"
        # elif request.form["dog"]:
        #     form_tag = "dog"
        # elif request.form["bird"]:
        #     form_tag = "bird"
        # else:
        #     form_tag = "other"

        date_time = now.strftime("%d/%m/%y/%H/%M/%S")
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
    app.run(debug = True)
    up.uses_netloc.append("postgres")
    url = up.urlparse(os.environ["postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"])
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
