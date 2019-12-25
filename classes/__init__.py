
import psycopg2 as dbapi2


CREATE_QUERIES = [
                        """
                        CREATE TABLE Users (
                            USERID SERIAL PRIMARY KEY,
                            NAME VARCHAR(40) NOT NULL,
                            SURNAME VARCHAR(40) NOT NULL,
                            EMAIL VARCHAR(80),
                            ISVET INTEGER NOT NULL,
                            PHOTO VARCHAR(255),
                            PASSWORD VARCHAR(120),
                            REGISTERDATE VARCHAR(40)
                        )

                        """,
                        
                        """
                        CREATE TABLE IF NOT EXISTS  Post (
                            POSTID SERIAL PRIMARY KEY,
                            USERID INTEGER REFERENCES Users (USERID),
                            POSTDATE VARCHAR(24),
                            PHOTOURL VARCHAR(255) NOT NULL,
                            DESCRIPTION VARCHAR(255),
                            TITLE VARCHAR(27) NOT NULL,
                            POSTTAG VARCHAR(20)
                        )
                        """,

                        

                        """                 
                        CREATE TABLE IF NOT EXISTS  Likes(
                            LIKEID SERIAL PRIMARY KEY,
                            POSTID INTEGER REFERENCES Post (POSTID),
                            WHOLIKED INTEGER REFERENCES Users (USERID),
                            DATE VARCHAR(24)
                        )
                        """,
                        """
                        CREATE TABLE IF NOT EXISTS CITY(
                            CITYID INTEGER PRIMARY KEY,
                            CITYNAME VARCHAR(30)
                        )
)                       """,
                        """
                        CREATE TABLE IF NOT EXISTS Vet(
                            VETID SERIAL PRIMARY KEY,
                            ADDRESS VARCHAR(255) NOT NULL,
                            DISTRICT VARCHAR(20) NOT NULL,
                            SERVICERATE FLOAT DEFAULT 0.0,
                            PRICERATE FLOAT DEFAULT 0.0,
                            TELEPHONE VARCHAR(15) NOT NULL UNIQUE,
                            OVERALLSCORE FLOAT DEFAULT 0.0,
                            VETNAME VARCHAR(50) NOT NULL,
                            CITYID INTEGER REFERENCES CITY(CITYID),
                            VOTENUM INTEGER DEFAULT 0,
                            CHECK (((SERVICERATE >= 0.0) AND (SERVICERATE <= 10.0)) AND ((PRICERATE >= 0.0) AND (PRICERATE <= 10.0))  AND ((OVERALLSCORE >= 0.0) AND (OVERALLSCORE <= 10.0)))
                        )
                        """,

                         """
                        CREATE TABLE IF NOT EXISTS  Rating(
                            RATEID SERIAL PRIMARY KEY,
                            USERID INTEGER REFERENCES USERS(USERID),
                            VETID INTEGER REFERENCES VET(VETID),
                            OVERALLSCORE INTEGER NOT NULL,
                            PRICERATE INTEGER NOT NULL,
                            SERVICERATE INTEGER NOT NULL,
                            COMMENT VARCHAR(255),
                            DATE VARCHAR(24) NOT NULL,
                            TITLE VARCHAR(50) NOT NULL
                        )
                        """,
                        """
                                                        
                        CREATE TABLE IF NOT EXIST Blog (
                            BLOGID SERIAL PRIMARY KEY,
                            USERID INTEGER REFERENCES Users (USERID),
                            BLOGTAG VARCHAR(20),
                            TITLE VARCHAR(100) NOT NULL,
                            TEXT VARCHAR(255) NOT NULL,
                            LIKENUMBER INTEGER DEFAULT 0,
                            DISLIKENUMBER INTEGER DEFAULT 0,
                            POSTDATE DATE
                        )
                        """,
			
			            """
                        CREATE TABLE IF NOT EXIST Notice (
                            NOTICEID SERIAL PRIMARY KEY,
                            USERID INTEGER REFERENCES Users (USERID),
                            ANIMALTYPE VARCHAR(10),
                            AGE INTEGER NOT NULL,
                            STRAIN VARCHAR(20),
                            GENDER VARCHAR(10),
                            PHOTOURL VARCHAR(255),
                            ISLOST INTEGER NOT NULL,
                            DESCRIPTION VARCHAR(255),
                            CONTACT VARCHAR(100),
                            DATE VARCHAR(100),
                            PLACE VARCHAR(80)
                        )
			            """,
			
                        """ 

                        CREATE TABLE IF NOT EXIST FoundationContact(
                            FOUNDID SERIAL PRIMARY KEY,
                            FACEBOOK VARCHAR(255),
                            TWITTER VARCHAR(255),
                            INSTAGRAM VARCHAR(255),
                            YOUTUBE VARCHAR(255),
                            WEBSITE VARCHAR(255)
                        )
                        """,
			
                        """ 
                        CREATE TABLE IF NOT EXIST Foundation (
                            FOUNDID INTEGER FOREIGN KEY REFERENCES FondationContact(FOUNDID),
                            PHOTO VARCHAR(255),
                            DONATIONURL VARCHAR(255),
                            ABOUT VARCHAR(255) NOT NULL,
                            FOUNDNAME VARCHAR(50) NOT NULL,
                            ADDRESS VARCHAR(100),
                            PRIMARY KEY(FOUNDID)
                        )
                        """,
			
			
                        """
                        CREATE TABLE IF NOT EXIST Notification(
                            NOTIFICATIONID SERIAL PRIMARY KEY,
                            POSTID  INTEGER NOT NULL,
                            USERID INTEGER REFERENCES USERS(USERID),
                            OWNERID INTEGER REFERENCES USERS(USERID),
                            CONTENT VARCHAR(200),
                            POSTTYPE INTEGER NOT NULL,
                            NOTIFICATIONTIME VARCHAR(20) NOT NULL,
                            NOTTYPE INTEGER NOT NULL,
                            ISSEEN INTEGER DEFAULT 0,    
                        )
                        """,

                        """
                        CREATE TABLE IF NOT EXIST Comment(
                            COMMENTID SERIAL PRIMARY KEY,
                            POSTID INTEGER NOT NULL REFERENCES Post (POSTID),
                            USERID INTEGER REFERENCES Users (USERID),
                            DATE VARCHAR(24),
                            COMMENT VARCHAR(70),
                            POSTTYPE INTEGER NOT NULL 
                        )
                        """,

                        """
                        
                        CREATE TABLE IF NOT EXIST SocialMedia(
                            OWNERID INTEGER REFERENCES Users(USERID),
                            FACEBOOK VARCHAR(255),
                            TWITTER VARCHAR(255),
                            INSTAGRAM VARCHAR(255),
                            YOUTUBE VARCHAR(255),
                            WEBSITE VARCHAR(255),
                            PRIMARY KEY (OWNERID)
                        )

                        """
                			
			
]


# def initialize(url):
#     with dbapi2.connect(url) as connection:
#         cursor = connection.cursor()
#         for statement in CREATE_QUERIES:
#             cursor.execute(statement)
#         cursor.close()

