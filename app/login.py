import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.reader import Reader
from app.investments import Investment

class Login(Reader):
    base = os.path.join(os.getcwd(), "db","login.json")

    @classmethod
    def getFilePath(cls):
        return cls.base

    @staticmethod
    def createLogin(user, password, filePath = None):
        filePath = filePath or Login.getFilePath()
        dados = Login._readDb(filePath)
        if dados.get(user, None) is not None:
            return False
        dados[user] = password
        Investment.createInvestment(user)
        return Login._writeDb(filePath, dados)

    @staticmethod
    def getUserDb(user, filePath = None):
        filePath = filePath or Login.getFilePath()
        dados = Login._readDb(filePath)
        return dados.get(user, None)

    @staticmethod
    def checkPassword(user, password, filePath = None):
        userDb = Login.getUserDb(user, filePath)
        if userDb == password:
            return True
        return False
    
    @staticmethod
    def checkUser(user, filePath = None):
        userDb = Login.getUserDb(user, filePath)
        if userDb is None:
            return False
        return True
    
    @staticmethod
    def checkLogin(user, password, filePath = None):
        if Login.checkUser(user, filePath) and Login.checkPassword(user, password, filePath):
            return True
        return False
    
    @staticmethod
    def logging(user, password, filePath = None):
        if Login.checkLogin(user, password, filePath):
            return Login.getUserDb(user, filePath)
        return None 
    
    @staticmethod
    def deleteLogin(user, password, filePath = None):
        filePath = filePath or Login.getFilePath()
        dados = Login._readDb(filePath)
        if Login.checkLogin(user, password,filePath):
            del dados[user]
            Login._writeDb(filePath, dados)
            return True
        return False
    
    @staticmethod
    def getAllUsers(filePath = None):
        filePath = filePath or Login.getFilePath()
        return Login._readDb(filePath)
    
    @staticmethod
    def updateUserLogin(user,password,newPassword, filePath = None):
        filePath = filePath or Login.getFilePath()
        if not Login.checkPassword(user,password,filePath):
            return False
        dados = Login._readDb(filePath)
        dados[user] = newPassword
        Login._writeDb(filePath,dados)
        return True