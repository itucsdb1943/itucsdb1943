class Post:
    def __init__(self, postid, userid, postdate, photo, title, description=None, posttag=None):
        self.postid = postid
        self.userid = userid
        self.postdate = postdate
        self.photo = photo
        self.description = description
        self.title = title
        self.posttag = posttag

