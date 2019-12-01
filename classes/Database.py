from classes.post import Post
from classes.foundation import Foundation
from classes.blog import Blog
import psycopg2 as dbapi2



class Database:
    def __init__(self, url):
        self.url = url
        self.posts = {}
        self.last_post_key = 0
        self.foundations = {}
        self._last_foundation_key = 0
        self.blogs = {}
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
	
    def add_foundation(self, foundation):
        self.last_foundation_key += 1
        self.movies[self._last_foundation_key] = foundation
        return self._last_foundation_key
		
    def delete_foundation(self, foundation_key):
        if foundation_key in self.foundations:
            del self.foundations[foundation_key]
	
    def get_foundation(self, foundation_key):
        foundation = self.foundations.get(foundation_key)
        if foundation is None:
            return None
        foundation_ = Foundation(foundation.foundID, foundation.photo, foundation.donationURL, foundation.facebookLink, foundation.twitterLink, foundation.youtubeLink, foundation.instagramLink, foundation.about, foundation.name)
        return foundation_
	
    def get_foundation(self):
        foundations = []
        for foundation_key, foundation in self.foundations.items():
            foundation_ = Foundation(foundation.self, foundation.foundID, foundation.photo, foundation.donationURL, foundation.facebookLink, foundation.twitterLink, foundation.youtubeLink, foundation.instagramLink, foundation.about, foundation.name)
            foundations.append((foundation_key, foundation_))
        return foundations

    def add_blog(self, blog):
        self._last_blog_key += 1
        self.blogs[self.last_blog_key] = blog
        return self.last_blog_key
   
    def delete_blog(self, blogn_key):
        if blog_key in self.blogs:
            del self.blogs[blog_key]
    
    def get_blog(self, blog_key):
        blog = self.blogs.get(blog_key)
        if blog is None:
            return None
        blog_ = Blog(blog.blogID, blog.userID, blog.tag, blog.title, blog.text, blog.likeNum, blog.dislikeNum, blog.postedDate)
        return blog_
	
    def get_blogs(self):
        blogs = []
        for blog_key, blog in self.blogs.items():
            blog_ = Blog(blog.blogID, blog.userID, blog.tag, blog.title, blog.text, blog.likeNum, blog.dislikeNum, blog.postedDate)
            blogs.append((blog_key, blog_))
        return blogs
