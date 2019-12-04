class Comment:
    def __init__(self, commentid, postid, userid, date, comment, posttype ):
        self.commentid = commentid
        self.postid = postid 
        self.userid = userid
        self.date = date
        self.comment = comment
        self.posttype = posttype #patigram için 0 olacak, bu objeyi başka kullanacak olan ne için hangi değeri alacağını belirtsin!
        