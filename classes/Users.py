import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"


class Users(UserMixin):
    def __init__(self,id,name,surname,username,isVet,password,facebookLink,twitterLink,youtubeLink,instagramLink,websiteLink,registerTime):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = username
        self.isVet = False
        self.photoURL = ""
        self.password = password
        self.isLogin = True
        self.facebookLink = facebookLink
        self.twitterLink = twitterLink
        self.youtubeLink = youtubeLink
        self.instagramLink = instagramLink
        self.websiteLink = websiteLink
        self.registerTime = registerTime
        self.isAdmin = False
    
    def createUser(self,name,surname,email,photoURL,password,facebookLink,twitterLink,youtubeLink,instagramLink,websiteLink,registerTime,isVet):
        self.name = name
        self.surname = surname
        self.email = email
        self.photoURL = photoURL
        self.password = password
        self.facebookLink = facebookLink
        self.twitterLink = twitterLink
        self.youtubeLink = youtubeLink
        self.instagramLink = instagramLink
        self.websiteLink = websiteLink
        self.registerTime = registerTime
        self.isLogin = True
        if isVet == True:
            self.isVet = True
        else:
            self.isVet = False        
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM POST """
            cursor.execute(statement)
            print(cursor.fetchone())
    @property   
    def is_authenticated(self):    
        return True      

    @ property
    def is_anonymous(self):    
        return False

    @property
    def is_active(self):
        return True

def get_user(id):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        statement = """SELECT PASSWORD FROM USERS WHERE EMAIL = '{0}' """.format(id)        cursor.execute(statement)
        db = cursor.fetchone()
        if db is not None:
            password = db[0]
            statement = """select userid,name,surname,email,isvet,facebook,twitter,youtube,instagram,website from users left join socialmedia on users.userid = socialmedia.ownerid where email = '{0}'""".format(id)            cursor.execute(statement)
            db2 = cursor.fetchone()
            user = Users(db2[0],db2[1],db2[2],db2[3],db2[4],password,db2[5],db2[6],db2[7],db2[8],db2[9],"12.12.12")
            return user
        else:
            return None



import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin
url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"


class Users(UserMixin):
    def __init__(self,id,name,surname,username,isVet,password,facebookLink,twitterLink,youtubeLink,instagramLink,websiteLink,registerTime):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = username
        self.isVet = False
        self.photoURL = ""
        self.password = password
        self.isLogin = True
        self.facebookLink = facebookLink
        self.twitterLink = twitterLink
        self.youtubeLink = youtubeLink
        self.instagramLink = instagramLink
        self.websiteLink = websiteLink
        self.registerTime = registerTime
        self.isAdmin = False
       
       
    def createUser(self,name,surname,email,photoURL,password,facebookLink,twitterLink,youtubeLink,instagramLink,websiteLink,registerTime,isVet):
        self.name = name
        self.surname = surname
        self.email = email
        self.photoURL = photoURL
        self.password = password
        self.facebookLink = facebookLink
        self.twitterLink = twitterLink
        self.youtubeLink = youtubeLink
        self.instagramLink = instagramLink
        self.websiteLink = websiteLink
        self.registerTime = registerTime
        self.isLogin = True
        if isVet == True:
            self.isVet = True
        else:
            self.isVet = False        
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM POST """
            cursor.execute(statement)
            print(cursor.fetchone())
    @property
    def is_authenticated(self):
        return True 

    @ property
    def is_anonymous(self):
        return False
    
    @property
    def is_active(self):
        return True
        
def get_user(id):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        statement = """SELECT PASSWORD FROM USERS WHERE EMAIL = '{0}' """.format(id)
        cursor.execute(statement)
        db = cursor.fetchone()
        if db is not None:
            password = db[0]
            statement = """select userid,name,surname,email,isvet,facebook,twitter,youtube,instagram,website from users left join socialmedia on users.userid = socialmedia.ownerid where email = '{0}'""".format(id)
            cursor.execute(statement)
            db2 = cursor.fetchone()
            user = Users(db2[0],db2[1],db2[2],db2[3],db2[4],password,db2[5],db2[6],db2[7],db2[8],db2[9],"12.12.12")
            return user
        else:
            return None

