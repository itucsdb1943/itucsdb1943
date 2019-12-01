
from flask import Flask, render_template,request,session
import psycopg2 as dbapi2
from flask import current_app
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


from datetime import datetime

now = datetime.now()
import os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
         
import psycopg2
app = Flask(__name__)
app.register_blueprint(site)

lm = LoginManager()

@lm.user_loader
def load_user(id):
    return get_user(id)

url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"


db = Database()
db.add_post(Post( 1, 1, "19.11.2019", "alp.jpeg", "Deneme alp's foto ", description="Cektirdigim bir vesikalik fotografim"))
db.add_post(Post( 2, 1, "19.11.2019", "saziskom.jpg", "Deneme sazis's foto ", description="Saziye'nin fotografini 1 yil once cekmistim ama artik bana kendini kucaklatmiyor minik siskocuk. Satoktan sonra iyice agresiflesti"))
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
    if post is None:
        abort(404)
    return render_template("patigram/patigram_custom.html", post=post)

@app.route("/patigram")
def patigram_page():
    db = current_app.config["db"]
    posts = db.get_posts()
    return render_template("patigram/patigram.html", posts=sorted(posts, reverse=True))

@app.route("/patigram/add", methods=["GET","POST"])
def patigram_add_page():
    if request.method == "GET":
        return render_template("patigram/patigramAdd.html")
    else:
        form_photo = request.form["photo"]
        form_title = request.form["title"]
        form_description = request.form["description"]
        form_tag = request.form["tag"]
        date_time = now.strftime("%d/%m/%y")
        user_id = 1
        post_id = 3
        post = Post(post_id,user_id,date_time,form_photo,form_title,description=form_description if form_description else None, tag=form_tag if form_tag else None)
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
