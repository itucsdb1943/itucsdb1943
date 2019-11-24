import psycopg2 as dbapi2

url = "postgres://rgkksygg:BO8pGAZa6BqFR84mF43EMNNljm3jRnM5@rogue.db.elephantsql.com:5432/rgkksygg"


class Users():
    def __init__(self):
        self.id = 0
        self.name = ""
        self.surname = ""
        self.email = ""
        self.isVet = False
        self.photoURL = ""
        self.password = ""
        self.isLogin = False
        self.facebookLink = ""
        self.twitterLink = ""
        self.youtubeLink = ""
        self.instagramLink = ""
        self.websiteLink = ""
        self.registerTime = ""
    
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
        

        


