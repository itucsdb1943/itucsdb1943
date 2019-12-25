Parts Implemented 3olpşşşy Bengisu Almıla Pınar
===============================

Patigram post issues like creation, deletion and update operations are implemented. Likes and comments for Patigram is implemented. Pages related to the FindVet are implemented, such as filtering veterinaries, rating veterinaries, updating veterinaries and ratings, and deleting veterinaries. Any function about FindVet and Patigram coded by me. Moreover, initilazion function which consists of queries creating tables and navbar except some alterations are implemented.

Post Table, Class & Functions 
-------------------------------------
Every user can share patigram posts and they can update or delete their posts.

Attributes of Post Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*POSTID SERIAL 
	Primary key of patigram post
*USERID INTEGER REFERENCES Users (USERID)
	The owner of the post
*POSTDATE VARCHAR(24)
    Post share date
*DESCRIPTION VARCHAR(255)
    Description of the post
*TITLE VARCHAR(27) NOT NULL
    Title of the post
*POSTTAG VARCHAR(20)
    Tag of the post which can be selected among dog, cat, bird and other.

Operations
^^^^^^^^^^
A class named Post is created for Patigram post operations.

Post Class
^^^^^
.. code-block:: python
    class Post:
        def __init__(self, postid, userid, postdate, photo, title, description=None, posttag=None):
            self.postid = postid
            self.userid = userid
            self.postdate = postdate
            self.photo = photo
            self.description = description
            self.title = title
            self.posttag = posttag

Create
^^^^^
Users can share posts from Add Patigram button in navbar. Posttag and description are not compulsory.

.. code-block:: python


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

Select
^^^^^
There are 3 select functions name get_post, get_posts and get_post_user. get_posts function which returns all posts is for displaying all posts in home page. get_post returns only one post for detail page. get_post_user function returns userid of that post to check whether current user owner of that post or not.

.. code-block:: python
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

    def get_post_user(self,post_key):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """SELECT USERID FROM POST
                        WHERE (POSTID = %s)"""
            cursor.execute(statement,(post_key,))
            user_ = cursor.fetchone()
            user_ = user_[0]
        return user_

Update
^^^^^

Users can change their post's title and description.

.. code-block:: python
    def update_patigram(self,postid,title,description):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ UPDATE POST
                            SET TITLE = %s,
                                DESCRIPTION = %s
                                WHERE (POSTID = %s);"""
            cursor.execute(statement,(title, description, postid))

Delete
^^^^^

Every user can delete only their own post by dint of delete_patigram function. Firstly, likes and comments related to the post are deleted because of reference issues. delete_post function is used in case of a user deletion by Alperen Cesur.

.. code-block:: python
        
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

    def delete_post(self,userid):
        with dbapi2.connect(self.url) as connection:
            posts = []
            cursor = connection.cursor()
            statement = """SELECT POSTID FROM POST WHERE USERID = '{0}'""".format(userid)
            cursor.execute(statement)
            for postid in cursor:
                self.delete_patigram(postid)

Comment Table, Class & Functions 
-------------------------------------
Comment table created for in case of that users want to make comments to the posts 

Attributes of Comment Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*COMMENTID SERIAL 
    Primary key for comment table
*POSTID INTEGER NOT NULL REFERENCES Post (POSTID)
    Foreign key to post table, indicates owner post
*USERID INTEGER REFERENCES Users (USERID)
    Foreign key to users table, indicates that who made comment
*DATE VARCHAR(24)
    Comment date
*COMMENT VARCHAR(70)
    Comment text
*POSTTYPE INTEGER NOT NULL 
    Posttype, 0 for patigram but comment is not used in other features yet

Operations
^^^^^^^^^^
Comment class id created to be used in necessary functions. Comment is only available for patigram.

.. code-block:: python
    class Comment:
        def __init__(self, commentid, postid, userid, date, comment, posttype ):
            self.commentid = commentid
            self.postid = postid 
            self.userid = userid
            self.date = date
            self.comment = comment
            self.posttype = posttype #0 for patigram


       
Create
^^^^^
Every user can comment to any post.

.. code-block:: python

    def add_comment(self,Comment):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO COMMENT(POSTID, USERID, DATE, COMMENT, POSTTYPE) VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(statement, (Comment.postid, Comment.userid, Comment.date, Comment.comment, Comment.posttype))

Select
^^^^^
Comments selected for listing in post detail page. Comment and users tables joined to get user's name and surname.

.. code-block:: python
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

Delete
^^^^^ 
Users can not delete their comments ,I delete comments when deleting post. This function is implemented for user deleting, so it is used by Alperen Cesur.  

.. code-block:: python
    def delete_user_comments(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM COMMENT WHERE USERID = '{0}' """.format(userid)
            cursor.execute(statement)


Likes Table, Class & Functions 
-------------------------------------
Likes table is created for liking posts, users can like or withdraw their like from post by hitting like button. Button color changes if they have already liked that post. 

Attributes of Likes Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*LIKEID SERIAL
    Primary key for comment table
*POSTID INTEGER REFERENCES Post (POSTID)
    Foreign key to post table, indicates the post which is liked
*WHOLIKED INTEGER REFERENCES Users (USERID)
    Foreign key to users table, indicates that who liked the post
*DATE VARCHAR(24)
    Like date

Operations
^^^^^^^^^^
       
Create
^^^^^
Every user can like any post, but only once.

.. code-block:: python

    def patigram_add_like(self, post_key, userid, date_time):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = """INSERT INTO LIKES (POSTID, WHOLIKED, DATE) 
                                VALUES(%s, %s, %s);"""
                cursor.execute(statement, (post_key, userid, date_time))


Select
^^^^^
patigram_get_like_num, patigram_is_user_liked functions are implemented. patigram_get_like_num function returns post's like number individually for home page and post detail page. patigram_is_user_liked returns whether current user is liked the post. This function is used in home page for every post separately.

.. code-block:: python
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

Delete
^^^^^ 
In patigram_delete_like and delete_user_likes functions likes are deleted. delete_user_likes function is implemented in case of deletion of a user. patigram_delete_like function is used for withdrawing likes.A post's likes will be deleted whenever post is deleted which is mentioned in post delete part.

.. code-block:: python
    def patigram_delete_like(self,postid,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ DELETE FROM LIKES
                            WHERE(POSTID = %s) AND (WHOLIKED = %s);"""
            cursor.execute(statement,(postid,userid))

    def delete_user_likes(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM LIKES WHERE WHOLIKED = '{0}' """.format(userid)
            cursor.execute(statement)





Vet Table, Class & Functions 
-------------------------------------
Users can find all veterinaries appended by admin in finVet page, they can find communication informations and scores of veterinaries.Moreover, veterinaries can be filtered by city.

Attributes of Vet Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*VETID SERIAL PRIMARY KEY,
    Primary key of the Vet
*ADDRESS VARCHAR(255) NOT NULL,
    Address of the Vet
*DISTRICT VARCHAR(20) NOT NULL,
    District of the Vet
*SERVICERATE FLOAT DEFAULT 0.0,
    Service rate of the Vet
*PRICERATE FLOAT DEFAULT 0.0,
    Price rate of the Vet
*TELEPHONE VARCHAR(15) NOT NULL UNIQUE,
    Telephone of the vet
*OVERALLSCORE FLOAT DEFAULT 0.0,
    Overall score of vet
*VETNAME VARCHAR(50) NOT NULL,
    Vet's name
*CITYID INTEGER REFERENCES CITY(CITYID),
    Reference key to the city table, vet's city license plate code
*VOTENUM INTEGER DEFAULT 0,
    Number of votes
*CHECK (((SERVICERATE >= 0.0) AND (SERVICERATE <= 10.0)) AND ((PRICERATE >= 0.0) AND (PRICERATE <= 10.0))  AND ((OVERALLSCORE >= 0.0) AND (OVERALLSCORE <= 10.0)))
    It is not a attribute, it controls that score will not exceed the limitations

Operations
^^^^^^^^^^
A class named Veteriner is created for Vet operations.

Veteriner Class
^^^^^
.. code-block:: python
    class Veteriner:
        def __init__ (self, vetid, address, district, serviceRate, priceRate, telephone, overallScore, vetName, voteNum, cityName):
            self.vetid = vetid
            self.address = address
            self.district = district
            self.serviceRate = serviceRate
            self.priceRate = priceRate
            self.telephone = telephone
            self.overallScore = overallScore
            self.vetName = vetName
            self.voteNum = voteNum
            self.cityName = cityName

Create
^^^^^
Users can not add veterinary, some veterinaries appended beginning of the program.

.. code-block:: python
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

Select
^^^^^
3 functions are implemented to select information from vet table. get_vets returns all vets in FindVet home page. get_selected_vets returns vets which are filtered by city in FindVet home page. get_vet returns one vet for detail page.

.. code-block:: python

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

Update
^^^^^
Vet's scores are updated when a rating is deleted or inserted,therefore codes can be seen from rating table's functions. 

Delete
^^^^^
Only admin named Bengisu Pınar whose userid equals 1 can delete veterinaries, when current user is admin in FindVet home page delete button will be appear for every veterinary.

.. code-block:: python
    
    def delete_vet(self,vet_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ delete from rating where (vetid = %s);
                            delete from vet where (vetid = %s);"""
            cursor.execute(statement, (vet_id, vet_id))
            connection.commit()



Rating Table, Class & Functions 
-------------------------------------
Rating table is created for evaluating veterinaries. Users can evaluate veterinaries only once, but they can change rating.

Attributes of Rating Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*RATEID SERIAL PRIMARY KEY,
    Primary key of the rating
*USERID INTEGER REFERENCES USERS(USERID),
    Owner of rating
*VETID INTEGER REFERENCES VET(VETID),
    rated veterinary
*OVERALLSCORE INTEGER NOT NULL,
    Overall score of the rate
*PRICERATE INTEGER NOT NULL,
    Price rate of the rate
*SERVICERATE INTEGER NOT NULL,
    Service rate of the rate
*COMMENT VARCHAR(255),
    Comment made by user 
*DATE VARCHAR(24) NOT NULL,
    Date of the rating
*TITLE VARCHAR(50) NOT NULL
    Title of the rating

Operations
^^^^^^^^^^
A class named Rate is created for Rating vet operations.

Rate Class
^^^^^
.. code-block:: python
    class Rate:
        def __init__(self, rateid, userid, vetid, overallScore, priceRate, serviceRate, comment, title, date):
            self.rateid = rateid
            self.userid = userid
            self.vetid = vetid
            self.overallScore = overallScore
            self.priceRate = priceRate
            self.serviceRate = serviceRate
            self.comment = comment
            self.title = title
            self.date = date

Create
^^^^^
Users can evaluate veterinaries by adding rate. Rate's scores were restricted in [0,5] interval by range input elements.

.. code-block:: python

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


Select
^^^^^
Evaluations made before are displayed in vet custom page, all ratings are pulled for  the vet in get_rates function. 
.. code-block:: python

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

Update
^^^^^
    Users can change their rating comments.

    ..code-block:: python

    def update_rating(self,vetid,userid,comment,date):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE RATING
                            SET COMMENT = %s,
                                DATE = %s
                            WHERE (USERID = %s) AND (VETID = %s);"""
            cursor.execute(statement,(comment, date, userid, vetid))
            connection.commit()


Delete
^^^^^
Users can not delete their ratings. But if they try to add second rating to the same vet, their old rate will be deleted and new one will be added. delete_user_rating function is used when a user is deleted from database.

.. code-block:: python

    def delete_user_rating(self,userid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM RATING WHERE USERID = '{0}' """.format(userid)
            cursor.execute(statement)


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



City Table, Class & Functions 
-------------------------------------
City table is created for keeping city integer in Vet table as city license plate code.

Attributes of City Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*CITYID INTEGER PRIMARY KEY
    plate code of the city, primary key of to the City table
*CITYNAME VARCHAR(30)
    Name of the city

Operations
^^^^^^^^^^
This table is used for filtering veterinaries and to acquire city name from plate code.


Create
^^^^^
This table should be consist of all 81 cities in Turkey, but necessary cities are inserted since veterinaries which are appended did not comprise all cities.

.. code-block:: python
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

Select
^^^^^
Two functions are implemented named get_vet_cities and get_cityname. get_cityname function used for obtain cityname from plate get. get_vet_cities function is implemented for filtering, this functions returns cities with one condition; at least one veterinary have to be found in every city returned.
.. code-block:: python

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
    