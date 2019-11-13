from flask import Flask, render_template
import psycopg2 as dbapi2
from flask import current_app


import os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
         
import psycopg2
app = Flask(__name__)
url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"

@app.route("/")
def home_page():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM POST """
        cursor.execute(statement)
        print(cursor.fetchone())
    return render_template("home.html")

@app.route("/post")
def post_page():
    return "Post page"

@app.route("/post/add")
def postAdd_page():
    return "add post page"

@app.route("/blog")
def blog_page():
    return render_template("blog/blog.html")

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
def forumAdd_page():
    return "Forum add page"

@app.route("/patigram")
def patigram_page():
    return render_template("patigram/patigram.html")

@app.route("/patigram/add")
def patigramAdd_page():
    return "Patigram add page"


@app.route("/notifications")
def notifications_page():
    return render_template("notifications.html")

if __name__ == "__main__":
    app.run(debug = True)
    up.uses_netloc.append("postgres")
    url = up.urlparse(os.environ["postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"])
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
