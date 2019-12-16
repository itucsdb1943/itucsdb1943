# coding=utf-8
import os

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

from classes.Notification import *
from classes.Profile import *
from flask import session
try:
    from urllib.parse import urlparse as up
except ImportError:
     from urlparse import urlparse as up
url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"


class Database:
    def __init__(self, url):
        self.url = url
        self.posts = {}
        self.last_post_key = 0
        self.foundations = {}
        self._last_foundation_key = 0
        self.blogs = {}
        self._last_blog_key = 0
        self.last_blog_key = 0

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
   
    def delete_notifications(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM NOTIFICATION WHERE OWNERID = '{0}' OR USERID = '{0}'""".format(userid)
            cursor.execute(statement)
    def delete_notices(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM NOTICE WHERE USERID = '{0}'""".format(userid)
            cursor.execute(statement)
    
    def delete_socialMedia(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM SOCIALMEDIA WHERE OWNERID = '{0}' """.format(userid)
            cursor.execute(statement)
    
    def get_post(self,post_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM POST WHERE POSTID = '{0}' """.format(post_key)
            cursor.execute(query)
            postid,userid,postdate,photourl,description,title,posttag = cursor.fetchone()
            post = Post(postid, userid, postdate, photourl, title, description = description, posttag = posttag)            
            return post
        return None

    def delete_user_comments(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM COMMENT WHERE USERID = '{0}' """.format(userid)
            cursor.execute(statement)
    
    def delete_user_likes(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM LIKES WHERE WHOLIKED = '{0}' """.format(userid)
            cursor.execute(statement)
    def delete_user_rating(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM RATING WHERE USERID = '{0}' """.format(userid)
            cursor.execute(statement)


    def delete_post(self,userid):
        with dbapi2.connect(self.url) as connection:
            posts = []
            cursor = connection.cursor()
            statement = """SELECT POSTID FROM POST WHERE USERID = '{0}'""".format(userid)
            cursor.execute(statement)
            for postid in cursor:
                self.delete_patigram(postid)
            
            
            

    def get_posts(self):
        posts = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM POST ORDER BY POSTDATE"""
            cursor.execute(query)
            for postid,userid,postdate,photourl,description,title,posttag in cursor:
                posts.append((postid , Post(postid, userid, postdate, photourl, title, description = description, posttag = posttag)))
        return posts
    
    def delete_patigram(self,postid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ delete from comment
                                WHERE POSTID = %s;
                                DELETE FROM LIKES
                                WHERE POSTID = %s;
                                DELETE FROM POST
                                WHERE POSTID = %s;"""
            cursor.execute(statement, (postid,postid,postid))

    def update_patigram(self,postid,title,description):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ UPDATE POST
                            SET TITLE = %s,
                                DESCRIPTION = %s
                                WHERE (POSTID = %s);"""
            cursor.execute(statement,(title, description, postid))


    def get_post_user(self,post_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT USERID FROM POST
                        WHERE (POSTID = %s)"""
            cursor.execute(statement,(post_key,))
            user_ = cursor.fetchone()
            user_ = user_[0]
        return user_

    def patigram_add_like(self, post_key, userid, date_time):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO LIKES (POSTID, WHOLIKED, DATE) 
                            VALUES(%s, %s, %s);"""
            cursor.execute(statement, (post_key, userid, date_time))
    
    def patigram_get_like_num(self, postid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ SELECT COUNT(POSTID) FROM LIKES
                            WHERE POSTID = %s;"""
            cursor.execute(statement,(postid,))
            likeN = cursor.fetchone()
            likeNum = likeN[0]
            like = int(likeNum)
        return like
    
    def patigram_delete_like(self,postid,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ DELETE FROM LIKES
                            WHERE(POSTID = %s) AND (WHOLIKED = %s);"""
            cursor.execute(statement,(postid,userid))

    def patigram_is_user_liked(self, postid, userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT DATE FROM LIKES
                            WHERE (WHOLIKED = %s) AND (POSTID = %s)"""
            cursor.execute(statement,(userid, postid))
            date = cursor.fetchone()
            # date = date[0]
            print(date)
            if date is None:
                return 0
            else:
                return 1


    def get_notices(self,Lost):
        notices = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """select noticeid,notice.userid,users.name,users.surname,animaltype,age,strain,gender,photourl,islost,description,contact,date,place from notice left join users on users.userid = notice.userid ORDER BY DATE"""
            cursor.execute(query)
            for noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place in cursor:
                if isLost == Lost:
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
    
    def get_notifications(self):
        notifications = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT NOTIFICATION.NOTIFICATIONID,USERS.NAME, USERS.SURNAME, NOTIFICATION.POSTTYPE, NOTIFICATION.NOTIFICATIONTIME, NOTIFICATION.ISSEEN,NOTIFICATION.CONTENT, NOTIFICATION.NOTTYPE,NOTIFICATION.TITLE FROM NOTIFICATION LEFT JOIN USERS ON NOTIFICATION.USERID = USERS.USERID WHERE NOTIFICATION.OWNERID = {0} ORDER BY NOTIFICATIONTIME""".format(session['user_id'])
            cursor.execute(query)
            for notificationID,name,surname,postType,notificationTime,isSeen,content,notType,title in cursor:                
                if postType == 1: #Patigram
                    if notType == 3:
                        title = ""
                    else:                            
                        if notType == 0:       
                            description = """Your Patigram Post named "{0}" is liked by {1} {2}.""".format(title,name,surname)
                        elif notType == 1:
                            description = """Your Patigram Post named "{0}" is commented by {1} {2}.""".format(title,name,surname)
                        elif notType == 2:
                            description = """Your Patigram Post named "{0}" is shared successfully.""".format(title)
                        else:
                            description = """Your Patigram Post named "{0}" is deleted successfully.""".format(title)
                if postType == 3: #Notice
                    description = """Your Notice named "{0}" is shared successfully""".format(title)
                if postType == 0: #Blog
                    if notType == 0:
                        description = """Your blog named "{0}" is liked by {1} {2}.""".format(title,name,surname)
                    elif notType == 2:
                        description = """Your blog named "{0}" is shared successfully.""".format(title) 
                print(description)
                notifications.append((notificationID,Notificition(notificationID,name,surname,title,notType,notificationTime,isSeen,postType,description,content)))
        return notifications
                
            
    def add_comment(self,Comment):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO COMMENT(POSTID, USERID, DATE, COMMENT, POSTTYPE) VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(statement, (Comment.postid, Comment.userid, Comment.date, Comment.comment, Comment.posttype))
        
    def add_notification(self,postType,postTitle,notType,userID,ownerID,content,time):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO NOTIFICATION(TITLE,NOTIFICATIONTIME,USERID,OWNERID,POSTTYPE,NOTTYPE,CONTENT) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(postTitle,time,userID,ownerID,postType,notType,content))
    
    def add_notice(self,title,place,animalType,gender,strain,age,photoUrl,isLost,contact,date,userID):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO NOTICE(USERID,ANIMALTYPE,AGE,STRAIN,GENDER,PHOTOURL,ISLOST,DESCRIPTION,CONTACT,DATE,PLACE)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(userID,animalType,age,strain,gender,photoUrl,isLost,title,contact,date,place))
            self.add_notification(3,title,2,userID,userID,"",date)
    
    def get_comments(self, posttype, postid):
        comments = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT USERS.NAME, COMMENT.USERID,USERS.SURNAME,COMMENT.COMMENT FROM COMMENT JOIN USERS
                                ON (COMMENT.USERID = USERS.USERID)
                            WHERE (POSTTYPE = %s) AND (POSTID = %s)
                            ORDER BY COMMENTID DESC;"""
            cursor.execute(statement,(posttype,postid))
            connection.commit()
            for name, userid, surname, comment in cursor:
                comments.append({"name": name, "userid":userid, "surname": surname, "comment": comment}) 
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
            query = """DELETE FROM FOUNDATIONCONTACT WHERE FOUNDID = '{0}'""".format(foundation_key)
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
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Saray mah. Mehmet Çavuş sk. no:10','Alanya', '024253979828','Alaiye Veteriner', 7);
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Kırcalı mah. Şehzade sk. no:33', 'Merkez', '03585698005', 'Şehzade Pati Veteriner', 5 );
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Hastane mah. Düzaltı cd. no:2', 'Meram', '06473849516', 'Meram Patileri Veteriner', 42);
                            INSERT INTO Vet(ADDRESS, DISTRICT, TELEPHONE, VETNAME, CITYID) VALUES ('Merkez mah. Kaptan Ali cd. no:61','Ortahisar', '06147904544', 'Mavi Bordo Veteriner', 61);"""
            cursor.execute(statement)
            connection.commit()
    def create_initial_cities(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO CITY VALUES(1, 'Adana'); 
                        INSERT INTO CITY VALUES(7, 'Antalya');
                        INSERT INTO CITY VALUES(34, 'İstanbul'); 
                        INSERT INTO CITY VALUES(35, 'İzmir');
                        INSERT INTO CITY VALUES(5, 'Amasya'); 
                        INSERT INTO CITY VALUES(61, 'Trabzon');
                        INSERT INTO CITY VALUES(43, 'Kütahya'); 
                        INSERT INTO CITY VALUES(42, 'Konya'); 
                        INSERT INTO CITY VALUES(6, 'Ankara');
                        INSERT INTO CITY VALUES(10, 'Bursa');"""
            cursor.execute(statement)
            connection.commit()

    def get_vet_cities(self):
        with dbapi2.connect(self.url) as connection:
            cities = []
            cursor = connection.cursor()
            statement = """SELECT DISTINCT CITY.CITYID, CITY.CITYNAME FROM VET LEFT JOIN CITY 
                            ON (VET.CITYID = CITY.CITYID) 
                            ORDER BY CITY.CITYID ASC;"""
            cursor.execute(statement)
            connection.commit()
            for cityid, city_name in cursor:
                cities.append((cityid, city_name))
            return cities
    
    def get_cityname(self, cityid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT CITYNAME FROM CITY
                            WHERE (CITYID = %s)"""
            cursor.execute(statement, (cityid,))
            connection.commit()
            city_name = cursor.fetchone()
            city_name = city_name[0]
            return city_name
    def get_user_detail(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """select name,surname,email,isvet,facebook,twitter,youtube,instagram,website,registerdate,photo from users left join socialmedia on users.userid = socialmedia.ownerid where userid = '{0}'""".format(userid)            
            cursor.execute(statement)
            db = cursor.fetchone()            
            user = Profile(db[0],db[1],db[2],db[3],db[4],db[5],db[6],db[7],db[8],db[9],db[10])
        return user
    def notification_seen(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE NOTIFICATION SET ISSEEN = 1  WHERE OWNERID = '{0}' """.format(userid)
            cursor.execute(statement)
    def update_user_photo(self,userid,url):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE USERS SET PHOTO = '{0}' WHERE USERID = '{1}' """.format(url,userid)
            cursor.execute(statement)
    
    def update_notice(self,noticeid,title,date):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE NOTICE SET DESCRIPTION = '{0}', DATE = '{1}' WHERE NOTICEID = '{2}' """.format(title,date,noticeid)
            cursor.execute(statement)

    def delete_vet(self,vet_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ delete from rating where (vetid = %s);
                            delete from vet where (vetid = %s);"""
            cursor.execute(statement, (vet_id, vet_id))
            connection.commit()
    def get_vets(self):
        with dbapi2.connect(self.url) as connection:
            vets = []
            cursor = connection.cursor()
            statement = """ SELECT VETID,DISTRICT,VETNAME, OVERALLSCORE, VOTENUM, CITY.CITYNAME FROM VET LEFT JOIN CITY
                            ON (VET.CITYID = CITY.CITYID)"""
            
            cursor.execute(statement)
            connection.commit()
            for vetid,district, vetname, score, votenum, cityname  in cursor:
                vets.append({ "vetid":vetid, "vetname":vetname, "district": district, "cityname":cityname,"score": score, "votenum":votenum})
        return vets

    def get_selected_vets(self, selectedid):
        with dbapi2.connect(self.url) as connection:
            vets = []
            cursor = connection.cursor()
            statement = """ SELECT VETID,DISTRICT,VETNAME, OVERALLSCORE, VOTENUM, CITY.CITYNAME FROM VET LEFT JOIN CITY
                            ON (VET.CITYID = CITY.CITYID)
                            WHERE ( VET.CITYID = %s) """
            
            cursor.execute(statement,(selectedid,))
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
    
    def delete_rate(self, userid, vetid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor() 
            statement = """ SELECT OVERALLSCORE, PRICERATE, SERVICERATE FROM RATING
                            WHERE (USERID = %s) AND (VETID = %s)""" 
            cursor.execute(statement,(userid, vetid)) 
            overall, price, service = cursor.fetchone()

            statement = """DELETE FROM RATING
                            WHERE (USERID = %s) AND (VETID = %s);"""   
            cursor.execute(statement,(userid, vetid))
            statement=""" SELECT VOTENUM FROM VET
                        WHERE (VETID = %s)"""
            cursor.execute(statement,(vetid,))
            voteN = cursor.fetchone()
            vote = voteN[0]
            vot = int(vote)
            print(vot)
            if vot is 1:
                statement = """ UPDATE VET
                            SET OVERALLSCORE = 0,
                                PRICERATE = 0,
                                SERVICERATE = 0,
                                VOTENUM = 0
                                WHERE (VETID = %s);"""
                cursor.execute(statement,(vetid,))
            else:
                statement =    """ UPDATE Vet
                                    SET OVERALLSCORE = ((OVERALLSCORE * VOTENUM) - %s) / (VOTENUM-1),
                                        PRICERATE = ((PRICERATE * VOTENUM) - %s) / (VOTENUM-1),
                                        SERVICERATE = ((SERVICERATE * Vet.VOTENUM) - %s) / (VOTENUM-1),
                                        VOTENUM = VOTENUM - 1
                                    WHERE (VETID = %s);"""
                cursor.execute(statement, (overall, price, service, vetid))

    def add_rate(self, rate):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM RATING
                            WHERE (USERID = %s) AND (VETID = %s)"""
            cursor.execute(statement,(rate.userid, rate.vetid))
            if cursor.fetchone() is not None:
                print("none değilmiş")
                self.delete_rate(rate.userid, rate.vetid)       
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

    def get_user_name(self, userid):
        with dbapi2.connect(self.url) as connection:            
            cursor = connection.cursor()
            statement = """SELECT name, surname FROM USERS
                            WHERE (USERID = %s)"""
            cursor.execute(statement, (userid,))
            name, surname = cursor.fetchone()
            user_ = name + " " + surname
            return user_

    def get_rates(self,vetid):
        rates = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT rating.userid, rateid, name, surname, vetid,  overallScore, priceRate, serviceRate, comment, date, title FROM RATING LEFT JOIN USERS
                            ON (RATING.USERID = USERS.USERID)
                            WHERE (VETID = %s)"""
            cursor.execute(statement, (vetid,))
            
            for userid, rateid, name, surname, vetid, overallScore, priceRate, serviceRate, comment, date, title in cursor:
                user = name + " " + surname
                rates.append((userid, (Rate(rateid, user, vetid, overallScore, priceRate, serviceRate, comment, title, date))))
        return rates

    def update_rating(self,vetid,userid,comment,date):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE RATING
                            SET COMMENT = %s,
                                DATE = %s
                           WHERE (USERID = %s) AND (VETID = %s);"""
            cursor.execute(statement,(comment, date, userid, vetid))
            connection.commit()
    def delete_user(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM USERS WHERE USERID = '{0}'""".format(userid)
            cursor.execute(statement)

if __name__ == "__main__":
    # session.pop('logged_in',None)
    #session['logged_in'] = False
    #up.uses_netloc.append("postgres")
    print("geldik buralara3")
    url = up.urlparse(os.environ["postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"])
    conn = dbapi2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )