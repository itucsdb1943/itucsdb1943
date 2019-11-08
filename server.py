from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/post")
def post_page():
    return "Post page"

@app.route("/post/add")
def postAdd_page():
    return "add post page"

@app.route("/blog")
def blog_page():
    return "blog page"

@app.route("/findvet")
def findVet_page():
    return "veteriner finding page"

@app.route("/foundation")
def foundation_page():
    return "foundation page"

@app.route("/notice")
def notice_page():
    return render_template("notifications.html")

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
