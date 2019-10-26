from flask import Flask


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Home page"

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

@app.route("/announcements")
def announcement_page():
    return "announcement page"

@app.route("/announcements/add")
def announcementAdd_page():
    return "announcement add page"


if __name__ == "__main__":
    app.run()
