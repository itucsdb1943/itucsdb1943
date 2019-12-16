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