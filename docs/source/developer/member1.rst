Parts Implemented by Alperen Cesur
===============================
To make authentication and authorization flask-login and users class are implemented. To add notice property to website, notice class implemented. Also notifications class is added to add notifications property to website.

Users Table, Class & Functions
-------------------------------------

To make authentication and authorization, users class is implemented.

Attributes of Users Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*USERID SERIAL PRIMARY KEY
      Primary key of the user
*NAME VARCHAR(40) NOT NULL
      Name of the user
*SURNAME VARCHAR(40) NOT NULL
      Surname of the user
*EMAIL VARCHAR(80)
      Email adress of the user
*ISVET INTEGER NOT NULL
      Is the user is veterinary or not? If yes, isvet = 1
*PHOTO VARCHAR(255)
      Photo url of the user
*PASSWORD VARCHAR(120)
      Hashed password of the user
*REGISTERDATE VARCHAR(40)
      Register Date of the user


Operations
^^^^^^^^^^

Users class created to make user operations.

Users Class
^^^^^^^^^^^
.. code-block:: python

      class Users(UserMixin):
          def __init__(self,id,name,surname,username,isVet,password,facebookLink,twitterLink,youtubeLink,instagramLink,websiteLink,registerTime,photoURL):
              self.id = id
              self.name = name
              self.surname = surname
              self.email = username
              self.isVet = False
              self.photoURL = photoURL
              self.password = password
              self.isLogin = True
              self.facebookLink = facebookLink
              self.twitterLink = twitterLink
              self.youtubeLink = youtubeLink
              self.instagramLink = instagramLink
              self.websiteLink = websiteLink
              self.registerTime = registerTime
              self.isAdmin = False

Create
^^^^^^^^

To create new user, user make register operation and the information of the user is create into database

.. code-block:: python

      def register_page():
         registerTime = now.strftime("%d/%m/%y %H:%M:%S")
         with dbapi2.connect(url) as connection:
              cursor = connection.cursor()
              try:
                 statement = """INSERT INTO Users(NAME, SURNAME, EMAIL,ISVET,PASSWORD,PHOTO,REGISTERDATE)
                 VALUES (%s,%s,%s,%s,%s,%s,%s); """
                 cursor.execute(statement,(name,surname,email,isVet,hashed,photoUrl,registerTime))
              except:
                 return render_template("register.html",message = "The email address is already used!")


Also password is hashed before the save into database.

.. code-block:: python

password = form['password']
hashed = hasher.hash(password)



Select
^^^^^^^^^^^
Select operation is used to get detail information of the user in profile page.

.. code-block:: python

      def get_user_detail(self,userid):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """select name,surname,email,isvet,facebook,twitter,youtube,instagram,website,registerdate,photo from users left join socialmedia on users.userid = socialmedia.ownerid where userid = '{0}'""".format(userid)
            cursor.execute(statement)
            db = cursor.fetchone()
            user = Profile(db[0],db[1],db[2],db[3],db[4],db[5],db[6],db[7],db[8],db[9],db[10])
         return user


Also select operation is used to check password of the user in the login operation.

.. code-block:: python

      def get_user(id):
         with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """SELECT PASSWORD FROM USERS WHERE EMAIL = '{0}' """.format(id)
            cursor.execute(statement)
            db = cursor.fetchone()


Update
^^^^^^^^^^^

Update operation is used to change avatar of the user.

.. code-block:: python

      def update_user_photo(self,userid,url):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE USERS SET PHOTO = '{0}' WHERE USERID = '{1}' """.format(url,userid)
            cursor.execute(statement)

Delete
^^^^^^^^^^^^
Delete operation is used to delete all of the information about the user. Before that, all of the references are deleted about this user.

.. code-block:: python

      def delete_user(self,userid):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM USERS WHERE USERID = '{0}'""".format(userid)
            cursor.execute(statement)



Notice Table, Class & Functions
-------------------------------------

Notice class is created to make operations with notices.

Attributes of Notice Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*NOTICEID SERIAL PRIMARY KEY
   Primary key of the notice
*USERID INTEGER REFERENCES Users (USERID)
   A foreign key refers to Users table. Creator of the notice
*ANIMALTYPE VARCHAR(10)
   Type of the animal which is in notice ( cat, dog etc.)
*AGE INTEGER NOT NULL
   Age of the animal which is in notice
*STRAIN VARCHAR(20)
   Strain of the animal which is in notice (Golden, British etc.)
*GENDER VARCHAR(10)
   Gender of the animal which is in notice (Girl or boy)
*PHOTOURL VARCHAR(255)
   URL of the Photo the notice
*ISLOST INTEGER NOT NULL
   Is notice for Lost pet or finding pet notice? If Lost notice, isLost = 1
*DESCRIPTION VARCHAR(255)
   Description,title of the notice
*CONTACT VARCHAR(100)
   Contact information of the notice owner ( telephone number)
*DATE VARCHAR(100)
   Created day of the notice
*PLACE VARCHAR(80)
   Place of the pet which is in the notice



Operations
^^^^^^^^^^

Notice class
^^^^^^^^^^^^^

.. code-block:: python

      class Notice:
         def __init__(self,noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place):
            self.noticeID = noticeID
            self.name = name
            self.surname = surname
            self.userID = userID
            self.animalType = animalType
            self.age = age
            self.strain = strain
            self.gender = gender
            self.photoURL = photoURL
            self.isLost = isLost
            self.description = description
            self.contact = contact
            self.date = date
            self.place = place


Create
^^^^^^^^^^
Notice is added according to user input.

.. code-block:: python

      def add_notice(self,title,place,animalType,gender,strain,age,photoUrl,isLost,contact,date,userID):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO NOTICE(USERID,ANIMALTYPE,AGE,STRAIN,GENDER,PHOTOURL,ISLOST,DESCRIPTION,CONTACT,DATE,PLACE)
                               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(userID,animalType,age,strain,gender,photoUrl,isLost,title,contact,date,place))

Select
^^^^^^^^^

To get all of the notice, get_notices function is used.

.. code-block:: python

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


To get detail of only one notice, get_notice function is used.

.. code-block:: python

      def get_notice(self,noticeID):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """select noticeid,notice.userid,users.name,users.surname,animaltype,age,strain,gender,photourl,islost,description,contact,date,place from notice left join users on users.userid = notice.userid where noticeid = '{0}'""".format(noticeID)
            cursor.execute(query)
            noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place = cursor.fetchone()
            notice = Notice(noticeID,userID,name,surname,animalType,age,strain,gender,photoURL,isLost,description,contact,date,place)
         return notice

Update
^^^^^^^^

Update operation is used to update description and date of the notice.

.. code-block:: python

      def update_notice(self,noticeid,title,date):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE NOTICE SET DESCRIPTION = '{0}', DATE = '{1}' WHERE NOTICEID = '{2}' """.format(title,date,noticeid)
            cursor.execute(statement)

Delete
^^^^^^^^^
Before the delete user, notices of the user are deleted.

.. code-block:: python

      def delete_notices(self,userid):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM NOTICE WHERE USERID = '{0}'""".format(userid)
            cursor.execute(statement)


Notification Table, Class & Functions
-------------------------------------


Attributes of Notification Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*NOTIFICATIONID SERIAL PRIMARY KEY
   Primary key of the notification.
*USERID INTEGER REFERENCES USERS(USERID)
   A foreign key refers to Users table. This user who is the make action.
*OWNERID INTEGER REFERENCES USERS(USERID)
   A foreign key refers to Users table. This user owner of the notification
*CONTENT VARCHAR(200)
   If the notification type is comment,  content of comment is Held in here.
*POSTTYPE INTEGER NOT NULL
   Type of the post.  0:Blog, 1:Patigram, 3:Notice
*NOTIFICATIONTIME VARCHAR(20) NOT NULL
   Time of the notification
*NOTTYPE INTEGER NOT NULL
   Type of notification. 0:Like, 1:Comment, 2:Add, 3:Delete
*ISSEEN INTEGER DEFAULT 0
   Is the notification seen from the user?


Operations
^^^^^^^^^^

Notification class created to make notification operations.

Notification Class
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

      class Notificition:
         def __init__(self,notificationID,userName,userSurname,postTitle,notificationType,notificationTime,isSeen,postType,description,content):
            self.notificitionID = notificationID
            self.userName = userName
            self.userSurname = userSurname
            self.postTitle = postTitle
            self.notificationType = notificationType    #0:Begeni, 1:Yorum, 2:Eklendi, 3:Silindi
            self.notificationTime = notificationTime
            self.isSeen = isSeen
            self.postType = postType    #0:Blog, 1:Patigram, 2:Forum, 3:Ilan
            self.description = description
            self.content = content

Create
^^^^^^^
To add notification add_notification is used.

.. code-block:: python

      def add_notification(self,postType,postTitle,notType,userID,ownerID,content,time):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """ INSERT INTO NOTIFICATION(TITLE,NOTIFICATIONTIME,USERID,OWNERID,POSTTYPE,NOTTYPE,CONTENT)
                              VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(postTitle,time,userID,ownerID,postType,notType,content))

Select
^^^^^^^

To get all notifications of the logined user, get_notifications function is user.

.. code-block:: python

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
               notifications.append((notificationID,Notificition(notificationID,name,surname,title,notType,notificationTime,isSeen,postType,description,content)))
         return notifications


Update
^^^^^^^

After user see the notifications, all of IsSeen attributes updated to 1 of user's notifications.

.. code-block:: python

      def notification_seen(self,userid):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """UPDATE NOTIFICATION SET ISSEEN = 1  WHERE OWNERID = '{0}' """.format(userid)
            cursor.execute(statement)


Delete
^^^^^^^^
Before deleting user, all of the notifications of the user is deleted.

.. code-block:: python

      def delete_notifications(self,userid):
         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM NOTIFICATION WHERE OWNERID = '{0}' OR USERID = '{0}'""".format(userid)
            cursor.execute(statement)
