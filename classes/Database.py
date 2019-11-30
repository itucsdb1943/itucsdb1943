from classes.post import Post
from classes.foundation import Foundation
from classes.blog import Blog

class Database:
    def __init__(self):
        self.posts = {}
        self.last_post_key = 0
        self.foundations = {}
        self._last_foundation_key = 0
        self.blogs = {}
        self.last_blog_key = 0
		
    def add_post(self, post):
        self.last_post_key += 1
        self.posts[self.last_post_key] = post
        return self.last_post_key
   
    def delete_post(self,post_key):
        if post_key in self.posts:
            del self.posts[post_key]
    
    def get_post(self,post_key):
        if post_key in self.posts:
            post_ = self.posts.get(post_key)
            post = Post(post_.postid, post_.userid, post_.postdate, post_.photo, post_.title, description = post_.description, posttag = post_.posttag)
            return post
        else:
            return None

    def get_posts(self):
        posts = []
        for post_key,post_ in self.posts.items():
            post = Post(post_.postid, post_.userid, post_.postdate, post_.photo, post_.title, description = post_.description, posttag = post_.posttag)
            posts.append((post_key, post))
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
