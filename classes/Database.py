from classes.post import Post

class Database:
    def __init__(self):
        self.posts = {}
        self.last_post_key = 0
    
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
            posts.append(post_key, post)
        return posts

