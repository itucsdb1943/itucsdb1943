Parts Implemented by İlknur Çelik
================================
The creating, selecting, updating, deleting operations of blog page were implemented. Foundation and foundation contact's creating, selecting, updating and deleting operations were implemented. 

Blog Table, Class & Functions
------------------------------
Users can add, delete, update the blogs.

Attributes of Blog Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* BLOGID SERIAL PRIMARY KEY
    Primary key of blog
* USERID INTEGER REFERENCES Users(USERID)
    User who posted blog
* BLOGTAG VARCHAR(20)
    Tag of the blog
* TITLE VARCHAR(100) NOT NULL
    Title of the blog
* TEXT TEXT NOT NULL
    Text of the blog
* LIKENUMBER INTEGER DEFAULT 0
    Like number of blog
* DISLIKE NUMBER INTEGER DEFAULT 0
    Dislike number of blog
* PHOTO VARCHAR(100)
    Photo of blog
* POSTDATE VARCHAR(24)
    Posted date of blog

Operations
^^^^^^^^^^
A Blog class was created to operate Blog operations.

Create
^^^^^^^
Blog class was used as constructor for adding new blog. 

.. code-block:: python

	class Blog:
		def __init__(self, blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate):
			self.blogid = blogid
			self.userid = userid
			self.blogtag = blogtag 
			self.title = title
			self.text = text
			self.likeNum = likeNum
			self.dislikeNum = dislikeNum
			self.photo = photo
			self.postdate = postdate

Entered informations were added to the database and Blog class.

.. code-block:: python

    def add_blog(self, blog):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO BLOG (USERID, BLOGTAG, TITLE, TEXT, LIKENUMBER, DISLIKENUMBER, PHOTO,POSTDATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(query, (blog.userid, blog.blogtag, blog.title, blog.text, blog.likeNum, blog.dislikeNum, blog.photo, blog.postdate))
            connection.commit()
            blog_key = cursor.lastrowid
        return blog_key

Select
^^^^^^^
There are 2 select functions. get_blog function returns the related blog's informations in the blog information page. get_blogs function returns all blogs in the blog home page.

.. code-block:: python

    def get_blog(self, blog_key):
       with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM BLOG WHERE BLOGID = '{0}' """.format(blog_key)
            cursor.execute(query)
            blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate = cursor.fetchone()
            blog = Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)
            return blog
       return None
       
.. code-block:: python

    def get_blogs(self):
        blogs = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM BLOG ORDER BY POSTDATE"""
            cursor.execute(query)
            for blogid,userid,blogtag,title,text,likeNum,dislikeNum,photo,postdate in cursor:
                blogs.append((blogid, Blog(blogid, userid, blogtag, title, text, likeNum, dislikeNum, photo,postdate)))
        return blogs


Update
^^^^^^^
Users can update title, tag and text of the blog.

.. code-block:: python

    def update_blog(self, blogid, title, blogtag, text):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE BLOG
                            SET TITLE = %s, 
                            BLOGTAG = %s, 
                            TEXT = %s
                            WHERE BLOGID = %s;"""
            cursor.execute(statement, (title, blogtag, text, blogid))

Delete
^^^^^^
Users can delete the blogs. 

.. code-block:: python

    def delete_blog(self, blog_key):
        with dbapi2.connect(self.url) as  connection:
            cursor = connection.cursor()
            query = """DELETE FROM BLOG WHERE BLOGID = '{0}' """.format(blog_key)
            cursor.execute(query)
            connection.commit()


Fondation and FoundationContact Table, Class & Functions
--------------------------------------------------------
Users can add, update, delete foundations.

Attributes of FoundationContact Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* FOUNDID SERIAL PRIMARY KEY
    Primary key of foundation contact table
* FACEBOOK VARCHAR(255)
    Facebook account of foundation
* TWITTER VARCHAR(255)
    Twitter account of foundation
* INSTAGRAM VARCHAR(255)
    Instagram account of foundation
* WEBSITE VARCHAR(255)
    Website account of foundation
* YOUTUBE VARCHAR(255)
    Youtube account of foundation

Attributes of Foundation Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* FOUNATIONID SERIAL PRIMARY KEY
    Primary key of foundation
* FOUNDID INTEGER REFERENCES FOUNDATIONCONTACT (FOUNDID)
    Foreign key of foundation which references to foundationcontact table
* PHOTO VARCHAR(255)
    Photo of foundation
* DONATIONURL VARCHAR(255)
    Donation URL of foundation
* ABOUT VARCHAR (255) NOT NULL
    About text of foundation
* FOUNDNAME VARCHAR(50) NOT NULL
    Foundation name
* ADDRESS VARCHAR(100)
    Address of foundation

Operations
^^^^^^^^^^
To able to create, select, update and delete foundations a class and functions were added.

Create
^^^^^^
Foundation class was used as constructor for adding new foundation.

.. code-block:: python

	class Foundation():
	    def __init__(self, foundid, photo, donationurl, about, foundname, address, facebook, twitter,instagram, website):
		self.foundid = foundid
		self.photo = photo
		self.donationurl = donationurl
		self.about = about
		self.foundname = foundname
		self.address = address
		self.facebook = facebook
		self.twitter = twitter
		self.instagram = instagram
		self.website = website

Entered informations were added to the database and Foundation class by adding separately the Foundation and FoundationContact tables.

.. code-block:: python

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
Select
^^^^^^
There are 2 selecting functions: get_foundation and get_foundations. Join operation was used for both two functions. get_foundation is used for select only one foundation

.. code-block:: python

    def get_foundation(self, foundation_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """SELECT FOUNDATION.FOUNDID, PHOTO, DONATIONURL, ABOUT, FOUNDNAME, ADDRESS, FACEBOOK, TWITTER, INSTAGRAM, WEBSITE FROM FOUNDATION LEFT JOIN FOUNDATIONCONTACT ON (FOUNDATION.FOUNDID = FOUNDATIONCONTACT.FOUNDID) WHERE (FOUNDATION.FOUNDID = %s)"""
            cursor.execute(query, (foundation_key,))
            foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram, website = cursor.fetchone()
            foundation = Foundation(foundid, photo, donationurl, about, foundname, address, facebook, twitter, instagram, website)
            return foundation
        return None

get_foundations is used for select all foundations 

.. code-block:: python
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

Update
^^^^^^
Users can update foundation's about text and donation URL.

.. code-block:: python

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

Delete
^^^^^^
Users can delete foundations.
.. code-block:: python

    def delete_foundation(self, foundation_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FOUNDATION WHERE FOUNDID = '{0}'""".format(foundation_key)
            cursor.execute(query)
            query = """DELETE FROM FOUNDATIONCONTACT WHERE FOUNDID = '{0}'""".format(foundation_key)
            cursor.execute(query)
            connection.commit()
