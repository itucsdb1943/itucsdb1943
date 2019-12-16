from classes.post import Post
from classes.comment import Comment
from classes.foundation import Foundation
from classes.blog import Blog
from classes.notices import Notice
import psycopg2 as dbapi2
from classes.veteriner import Veteriner
from classes.rate import *
from classes.foundationcontact import *
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


class Database:
    def __init__(self, url):
        self.url = url
        self.posts = {}
        self.last_post_key = 0
        self.foundations = {}
        self._last_foundation_key = 0
        self.blogs = {}
        self._last_blog_key = 0
		
    def add_post(self, post):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            if post.posttag is None and post.description is None:
                 query = """INSERT INTO Post(USERID, POSTDATE, PHOTOURL, TITLE  )  VALUES ('{0}','{1}','{2}','{3}' );""".format(post.userid,post.postdate,post.photo, post.title)
            elif post.posttag is None:
                query = """INSERT INTO Post(USERID, POSTDATE, PHOTOURL, DESCRIPTION, TITLE )  VALUES ('{0}','{1}','{2}','{3}', '{4}' );""".format(post.userid,post.postdate,post.photo, post.description, post.title)
            elif post.description is None:
                 query = """INSERT INTO Post(USERID, POSTDATE, PHOTOURL, TITLE, POSTTAG )  VALUES ('{0}','{1}','{2}','{3}', '{4}' );""".format(post.userid,post.postdate,post.photo,  post.title, post.posttag)
            else:
                 query = """INSERT INTO Post(USERID, POSTDATE, PHOTOURL, DESCRIPTION, TITLE, POSTTAG )  VALUES ('{0}','{1}','{2}','{3}', '{4}', '{5}' );""".format(post.userid,post.postdate,post.photo, post.description, post.title, post.posttag)
            cursor.execute(query)
            connection.commit()
            statement = """ SELECT POSTID FROM POST WHERE ( USERID = %s) AND (PHOTOURL = %s) AND (TITLE = %s) AND (POSTDATE = %s) """
            cursor.execute(statement, (post.userid, post.photo, post.title, post.postdate))
            obj = cursor.fetchone()
            post_key = obj[0]
        # self.last_post_key += 1
        # self.posts[self.last_post_key] = post
        return post_key
   
    def delete_post(self,post_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM POST WHERE POSTID = '{0}' """.format(post_key)
            cursor.execute(query)
            connection.commit()

    
    def get_post(self,post_key):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                query = """ SELECT * FROM POST WHERE POSTID = '{0}' """.format(post_key)
                cursor.execute(query)
                postid,userid,postdate,photourl,description,title,posttag = cursor.fetchone()
                post = Post(postid, userid, postdate, photourl, title, description = description, posttag = posttag)            
                return post
            return None

    def get_posts(self):
        posts = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM POST ORDER BY POSTDATE"""
            cursor.execute(query)
            for postid,userid,postdate,photourl,description,title,posttag in cursor:
                posts.append((postid , Post(postid, userid, postdate, photourl, title, description = description, posttag = posttag)))
        return posts
    def get_notices(self):
        notices = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """select noticeid,notice.userid,users.name,users.surname,animaltype,age,strain,gender,photourl,islost,description,contact,date,place from notice left join users on users.userid = notice.userid ORDER BY DATE"""
            cursor.execute(query)
            for noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place in cursor:
                notices.append((noticeID,Notice(noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place)))
        return notices
    def get_notice(self,noticeID):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """select noticeid,notice.userid,users.name,users.surname,animaltype,age,strain,gender,photourl,islost,description,contact,date,place from notice left join users on users.userid = notice.userid where noticeid = '{0}'""".format(noticeID)
            cursor.execute(query)
            noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place = cursor.fetchone()
            notice = Notice(noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place)
        return notice

    def add_comment(self,Comment):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO COMMENT(POSTID, USERID, DATE, COMMENT, POSTTYPE) VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(statement, (Comment.postid, Comment.userid, Comment.date, Comment.comment, Comment.posttype))

    def get_comments(self, posttype, postid):
        comments = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT USERS.NAME, USERS.SURNAME,COMMENT.COMMENT FROM COMMENT JOIN USERS
                                ON (COMMENT.USERID = USERS.USERID)
                            WHERE (POSTTYPE = %s) AND (POSTID = %s)
                            ORDER BY COMMENTID DESC"""
            cursor.execute(statement,(posttype,postid))
            connection.commit()
            for name, surname, comment in cursor:
                comments.append({"name": name, "surname": surname, "comment": comment}) 
        return comments

    def add_foundation(self, foundation):
        with dbapi2.connect(self.url) as connection:
            cursor = connection. cursor()
            
            statement = """INSERT INTO FOUNDATIONCONTACT ( FACEBOOK, TWITTER, INSTAGRAM, WEBSITE)
                        VALUES ( %s,%s,%s,%s);
                    """
            cursor.execute(statement, (foundation.facebook, foundation.twitter, foundation.instagram, foundation.website))
            query = """SELECT FOUNDID FROM FOUNDATIONCONTACT WHERE (FACEBOOK = %s)"""
            cursor.execute(query, (foundation.facebook,))
            nowid = cursor.fetchone()
            nowid = nowid[0]

            query = """INSERT INTO FOUNDATION (FOUNDID,PHOTO, DONATIONURL, ABOUT, FOUNDNAME, ADDRESS)
                    VALUES (%s, %s,%s,%s,%s,%s);
                    """
            cursor.execute(query, (nowid, foundation.photo, foundation.donationurl, foundation.about, foundation.foundname, foundation.address))


            foundation_key = cursor.lastrowid
        return foundation_key

    def delete_foundation(self, foundation_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FOUNDATION WHERE FOUNDID = '{0}'""".format(foundation_key)
            cursor.execute(query)
            connection.commit()

    def get_foundation(self, foundation_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT FOUNDATION.FOUNDID, PHOTO, DONATIONURL, ABOUT, FOUNDNAME, ADDRESS, FACEBOOK, TWITTER, INSTAGRAM, WEBSITE FROM FOUNDATION LEFT JOIN FOUNDATIONCONTACT ON (FOUNDATION.FOUNDID = FOUNDATIONCONTACT.FOUNDID) WHERE (FOUNDATION.FOUNDID = %s)"""
            cursor.execute(query, (foundation_key,))
            foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram, website = cursor.fetchone()
            foundation = Foundation(foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram, website)
            return foundation
        return None

    def get_foundations(self):
        foundations = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT FOUNDATION.FOUNDID, PHOTO, DONATIONURL, ABOUT, FOUNDNAME, ADDRESS, FOUNDATIONCONTACT.FACEBOOK, FOUNDATIONCONTACT.TWITTER, FOUNDATIONCONTACT.INSTAGRAM, FOUNDATIONCONTACT.WEBSITE FROM FOUNDATION LEFT JOIN FOUNDATIONCONTACT 
                    ON (Foundation.FOUNDID = FoundationContact.FOUNDID) """
            cursor.execute(query)
            connection.commit()
            for foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram, website in cursor:
                foundations.append((foundid, Foundation(foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram,website)))
        return foundations

    def update_foundation(self, foundid, about, donationurl):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE FOUNDATION 
                            SET ABOUT = %s,
                            DONATIONURL = %s
                            WHERE (FOUNDID =%s);
                        """
            cursor.execute(statement, (about,donationurl, foundid))
            connection.commit()
    def add_blog(self, blog):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO BLOG (USERID, BLOGTAG, TITLE, TEXT, LIKENUMBER, DISLIKENUMBER, PHOTO,POSTDATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, (blog.userid, blog.blogtag, blog.title, blog.text, blog.likeNum, blog.dislikeNum, blog.photo, blog.postdate))
            connection.commit()
            blog_key = cursor.lastrowid
        return blog_key
   
    def delete_blog(self, blog_key):
        with dbapi2.connect(self.url) as  connection:
            cursor = connection.cursor()
            query = """DELETE FROM BLOG WHERE BLOGID = '{0}' """.format(blog_key)
            cursor.execute(query)
            connection.commit()

    def blog_like(self, blog_key):
        with dbapi2.connect(self.url) as  connection:
            cursor = connection.cursor()
            statement = """UPDATE BLOG
                                SET LIKENUMBER = LIKENUMBER + 1
                                WHERE (BLOGID=%s)"""
            cursor.execute(statement, (blog_key,))
            connection.commit()

    def blog_dislike(self, blog_key):
        with dbapi2.connect(self.url) as  connection:
            cursor = connection.cursor()
            statement = """UPDATE BLOG
                                SET DISLIKENUMBER = DISLIKENUMBER + 1
                                WHERE (BLOGID=%s)"""
            cursor.execute(statement, (blog_key,))
            connection.commit()

    def get_cats(self):
        catblogs = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM BLOG WHERE BLOG.BLOGTAG = 'Cat'"""
            cursor.execute(statement)
            for blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate in cursor:
                catblogs.append((blogid, Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)))
            return catblogs
    
    def get_dogs(self):
        dogblogs = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM BLOG WHERE BLOG.BLOGTAG = 'Dog'"""
            cursor.execute(statement)
            for blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate in cursor:
                dogblogs.append((blogid, Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)))
            return dogblogs
    
    def get_birds(self):
        birdblogs = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM BLOG WHERE BLOG.BLOGTAG = 'Bird'"""
            cursor.execute(statement)
            for blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate in cursor:
                birdblogs.append((blogid, Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)))
            return birdblogs

    def get_other(self):
        otherblogs = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM BLOG WHERE BLOG.BLOGTAG = 'Other'"""
            cursor.execute(statement)
            for blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate in cursor:
                otherblogs.append((blogid, Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)))
            return otherblogs

    def get_blog(self, blog_key):
       with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM BLOG WHERE BLOGID = '{0}' """.format(blog_key)
            cursor.execute(query)
            blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate = cursor.fetchone()
            blog = Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)
            return blog
       return None
	
    def get_blogs(self):
        blogs = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM BLOG ORDER BY POSTDATE"""
            cursor.execute(query)
            for blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate in cursor:
                blogs.append((blogid, Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)))
        return blogs

    def update_blog(self, blogid, title, blogtag, text):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE BLOG
                            SET TITLE = %s, 
                            BLOGTAG = %s, 
                            TEXT = %s
                            WHERE BLOGID = %s;"""
            cursor.execute(statement, (title, blogtag, text, blogid))
    def create_initial_vets(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Çeliktepe mah. Münir Kemal cd. no:38', 'Kağıthane', '02425676755', 'Çeliktepe Pati Veteriner', 34 );
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Cikcilli mah. Gümüşler cd. no:52', 'Alanya', '02125152610', 'Cikcilli Veteriner', 7);
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Gürsel mah. Komşu cd. no:95','Kağıthane', '02127656578', 'Patisever Veteriner', 34);
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Yıldız mah. Abdülhamit cd. no:39', 'Beşiktaş','02128979908', 'Yıldız Veteriner', 34);
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Saray mah. Mehmet Çavuş sk. no:10','Alanya', '024253979828','Alaiye Veteriner', 7);"""
            cursor.execute(statement)
            connection.commit()
    
    def get_vets(self):
        with dbapi2.connect(self.url) as connection:
            vets = []
            cursor = connection.cursor()
            statement = """ SELECT VETID,DISTRICT,VETNAME, OVERALLSCORE, VOTENUM, CITY.CITYNAME FROM VET LEFT JOIN CITY
                            ON (VET.CITYID = CITY.CITYID) """
            
            cursor.execute(statement)
            connection.commit()
            for vetid,district, vetname, score, votenum, cityname  in cursor:
                vets.append({ "vetid":vetid, "vetname":vetname, "district": district, "cityname":cityname,"score": score, "votenum":votenum})
        return vets

    def get_vet(self, vetid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ SELECT VETID,ADDRESS,DISTRICT,SERVICERATE, PRICERATE, TELEPHONE, OVERALLSCORE, VETNAME, VOTENUM, CITYNAME
                            FROM VET LEFT JOIN CITY
                            ON(VET.CITYID = CITY.CITYID)
                            WHERE (VETID = %s)"""
            cursor.execute(statement,(vetid,))
            connection.commit()
            vetid, address, district, servicerate, pricerate, telephone, overallscore, vetname, votenum, cityname = cursor.fetchone()
            print("oddddd %s",cityname)
            vet = Veteriner(vetid, address, district, servicerate, pricerate, telephone, overallscore, vetname, votenum, cityname)
            print(vet.vetName)
            return vet
        return None

    def add_rate(self, rate):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO Rating(USERID, VETID, OVERALLSCORE, PRICERATE, SERVICERATE, COMMENT, DATE, TITLE)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(statement,(rate.userid, rate.vetid, rate.overallScore, rate.priceRate, rate.serviceRate, rate.comment, rate.date, rate.title))
            #Scores must be updated
            statement =    """ UPDATE Vet
                                SET OVERALLSCORE = ((OVERALLSCORE * VOTENUM) + (%s)) / (VOTENUM+1),
                                    PRICERATE = ((PRICERATE * VOTENUM) + (%s)) / (VOTENUM+1),
                                    SERVICERATE = ((SERVICERATE * VOTENUM) + (%s)) / (VOTENUM+1),
                                    VOTENUM = VOTENUM + 1
                                WHERE (VETID = %s);"""
            cursor.execute(statement, (rate.overallScore, rate.priceRate, rate.serviceRate, rate.vetid))

