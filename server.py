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
from classes.blog import *
from classes.foundation import *
from classes.foundationcontact import *
from datetime import datetime
now = datetime.now()

#For uploading photo
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/patigram')
UPLOAD_FOLDER_BLOG = join(dirname(realpath(__file__)), 'static/blog')
UPLOAD_FOLDER_FOUNDATION = join(dirname(realpath(__file__)), 'static/foundation')

ALLOWED_EXTENSIONS = {  'png', 'jpg', 'jpeg', 'gif'}


try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
         
import psycopg2
app = Flask(__name__)
app.register_blueprint(site)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_BLOG'] = UPLOAD_FOLDER_BLOG
app.config['UPLOAD_FOLDER_FOUNDATION'] = UPLOAD_FOLDER_FOUNDATION

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

@app.route("/logout")
def logout_page():
    session['logged_in'] = False
    next_page = request.args.get("next", url_for("home_page"))
    return redirect(next_page)

@app.route("/post")
def post_page():
    return "Post page"


@app.route("/blog", methods=["GET", "POST"])
def blog_page():
    db = current_app.config["db"]
    if request.method == "GET":
        blogs = db.get_blogs()
        return render_template("blog/blog.html", blogs=sorted(blogs))
    else:
        if "all" in request.form:
            blogs = db.get_blogs()
        elif "cat" in request.form:
            print("burda")
            blogs = db.get_cats()
        elif "dog" in request.form:
            blogs = db.get_dogs()
        elif "bird" in request.form:
            blogs = db.get_birds()
        elif "other" in request.form:
            blogs = db.get_other()
        return render_template("blog/blog.html", blogs=sorted(blogs))

@app.route("/blog/like/<int:blog_key>")
def blog_like(blog_key):
    db = current_app.config["db"]
    db.blog_like(blog_key)
    return redirect(url_for("blog_info_page",blog_key = blog_key))

@app.route("/blog/dislike/<int:blog_key>")
def blog_dislike(blog_key):
    db = current_app.config["db"]
    db.blog_dislike(blog_key)
    return redirect(url_for("blog_info_page", blog_key = blog_key))

 
@app.route("/blog/edit/<int:blog_key>", methods=["GET", "POST"])
def blog_edit(blog_key):
    if request.method == "GET":
        return render_template("blog/blogedit.html")
    else:
        db = current_app.config["db"]
        old_blog = db.get_blog(blog_key)
        form_titlerr = request.form.get("title", "").strip()
        # if len(form_titlerr) == 0 and "title" in request.form:
            # return render_template("blog/blogedit.html", error=1)
        
        form_title = request.form["title"]
        form_blogtag = request.form["blogtag"]
        form_text = request.form["text"]

        if "title" in request.form and "blogtag" in request.form and "text" in request.form:
            db.update_blog(blog_key, request.form["title"], request.form["blogtag"], request.form["text"])
        elif "title" in request.form and "blogtag" in request.form:
            db.update_blog(blog_key, request.form["title"], request.form["blogtag"], old_blog.text)
        elif "title" in request.form and "text" in request.form:
            db.update_blog(blog_key, request.form["title"], old_blog.blogtag, request.form["text"])
        elif "blogtag" in request.form and "text" in request.form:
            db.update_blog(blog_key, old_blog.title, request.form["blogtag"], request.form["text"])
        elif "title" in request.form:
            db.update_blog(blog_key, request.form["title"], old_blog.blogtag, old_blog.text)
        elif "blogtag" in request.form:
            db.update_blog(blog_key, old_blog.title, request.form["blogtag"], old_blog.text)
        elif "text" in request.form:
            db.update_blog(blog_key, old_blog.title, old_blog.blogtag, request.form["text"])
        return redirect(url_for("blog_info_page", blog_key = blog_key))


@app.route("/blog/<int:blog_key>")
def blog_info_page(blog_key):
    db = current_app.config["db"]
    blog = db.get_blog(blog_key)
    return render_template("blog/bloginfo.html", blog=blog)

@app.route("/blog/blogadd", methods=["GET","POST"])
def blog_add_page():
    if request.method == "GET":
        values = {"title":"", "text": ""}
        return render_template("blog/blogadd.html", values=values)
    else:
        valid = validate_blog_form(request.form)
        if not valid:
            return render_template("blog/blogadd.html", values = request.form)
        title = request.form.data['title']
        text = request.form.data["text"]
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
        blogtag = request.form["tag"]
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_BLOG'], filename))
            photo = filename
    

        user_id = 1
        blog_id = 4
        likeNum = 0
        dislikeNum = 0
        blog = Blog(blog_id, user_id, blogtag, title, text, likeNum, dislikeNum, photo,date_time)
        db = current_app.config["db"]
        blog_key = db.add_blog(blog)
        return redirect(url_for("blog_page", blog_key = blog_key))

def validate_blog_form(form):
	form.data = {}
	form.errors = {}
	
	form_title = form.get("title", "").strip()
	if len(form_title) == 0:
		form.errors["title"] = "Title can not be blank."
	else:
		form.data["title"] = form_title
	
	form_text = form.get("text")
	if len(form_text) == 0:
		form.errors["text"] = "Text can not be blank."
	else:
		form.data["text"] = form_text
	return len(form.errors) == 0
	


@app.route("/blog/blogdelete", methods = ["GET", "POST"])
def blogs_delete():
    db = current_app.config["db"]
    if request.method == "GET":
        blogs = db.get_blogs()
        return render_template("/blog/blogdelete.html", blogs=sorted(blogs))
    else:
        form_blog_keys = request.form.getlist("blog_keys")
        for form_blog_key in form_blog_keys:
            db.delete_blog(int(form_blog_key))
        return redirect(url_for("blog_page"))



@app.route("/findvet")
def findVet_page():
    db = current_app.config["db"]
    vets = db.get_vets()
    #db.create_initial_vets()
    for vet in vets:
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
    return render_template("findVet/vet_custom_page.html", vet=vet)

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
        userid = 1 # Should be handled
        rateid = 1 # Just for errors, not real value. Sql will give real rateid
        new_rate = Rate(rateid, userid, vetid, form_overall, form_price, form_service, form_comment, form_title, date_time)
        db.add_rate(new_rate)
        vet = db.get_vet(vet_key)
        vet.overallScore = int(vet.overallScore)
        vet.priceRate = int(vet.priceRate)
        vet.serviceRate = int(vet.serviceRate)
        return render_template("findVet/vet_custom_page.html", vet=vet)
        
@app.route("/foundation")
def foundation_page():
    db = current_app.config["db"]
    foundations = db.get_foundations()
    return render_template("foundation/foundation.html", foundations= (foundations)) 

@app.route("/foundation/edit/")
def foundation_edit():
    db = current_app.config["db"]
    foundations = db.get_foundations()
    return render_template("foundation/foundationedit.html", foundations=sorted(foundations))

@app.route("/foundation/foundationedit/<int:foundation_key>", methods=["GET","POST"])
def foundation_update(foundation_key):
    if request.method == "GET":
        return render_template("foundation/foundationupdate.html")
    else:
        db = current_app.config["db"]
        old_foundation = db.get_foundation(foundation_key)
        #form_about = request.form["about"]
        #form_donationurl = request.form["donationurl"]

        if "about" in request.form and "donationurl" in request.form:
            db.update_foundation(foundation_key, request.form["about"], request.form["donationurl"])
        elif "about" in request.form:
            db.update_foundation(foundation_key, request.form["about"], old_foundation.donationurl)
        elif "donationurl" in request.form:
            db.update_foundation(foundation_key, old_foundation.about, request.form["donationurl"])
        return redirect(url_for("foundation_update", foundation_key = foundation_key))

@app.route("/foundation/foundationadd", methods=["GET","POST"])
def foundation_add_page():
    if request.method == "GET":
        values = {"foundname":"", "about":""}
        return render_template("foundation/foundationadd.html", values=values)
    else:
        valid = validate_foundation_form(request.form)
        if not valid:
            return render_template("foundation/foundationadd.html", values =request.form)
        
        foundname = request.form["foundname"]
        donationurl = request.form["donationurl"]
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_FOUNDATION'], filename))
            photo = filename
        about = request.form["about"]
        address = request.form["address"]
        facebook =request.form["facebook"]
        twitter = request.form["twitter"]
        instagram = request.form["instagram"]
        website =request.form["website"]
        
        foundid = 4
        foundation = Foundation(foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram,website)
        db = current_app.config["db"]
        foundation_key = db.add_foundation(foundation)
        return redirect(url_for("foundation_page", foundation_key = foundation_key))

def validate_foundation_form(form):
    form.data = {}
    form.errors = {}
	
    form_foundname = form.get("foundname", "").strip()
    if len(form_foundname) == 0:
        form.errors["foundname"] = "Foundation name can not be blank."
    else:
        form.data["foundname"] = form_foundname
	
    form_about = form.get("about")
    if len(form_about) == 0:
        form.errors["about"] = "About can not be blank."
    else:
        form.data["about"] = form_about
    return len(form.errors) == 0

@app.route("/foundation/foundationdelete", methods=["GET", "POST"])
def foundation_delete():
    db = current_app.config["db"]
    if request.method == "GET":
        foundations = db.get_foundations()
        return render_template("/foundation/foundationdelete.html", foundations=(foundations))
    else:
        form_foundation_keys = request.form.getlist("foundation_keys")
        for form_foundation_key in form_foundation_keys:
            db.delete_foundation(int(form_foundation_key))
        return redirect(url_for("foundation_page"))

	
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
        date_time = now.strftime("%d/%m/%y %H:%M:%S")
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
    app.run(debug = True)
    session.pop('logged_in',None)
    #session['logged_in'] = False
    up.uses_netloc.append("postgres")
    url = up.urlparse(os.environ["postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"])
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
