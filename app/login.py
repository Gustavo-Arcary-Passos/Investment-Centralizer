import os
from reader import Reader
from investments import Investment

class Login(Reader):
    base = os.path.join(os.getcwd(), "db","login.json")

    @staticmethod
    def createLogin(user, password):
        dados = Login._readDb(Login.base)
        if dados.get(user, None) is not None:
            return False
        dados[user] = password
        return Login._writeDb(Login.base, dados)

    @staticmethod
    def getUserDb(user):
        dados = Login._readDb(Login.base)
        return dados.get(user, None)

    @staticmethod
    def checkPassword(user, password):
        userDb = Login.getUserDb(user)
        if userDb == password:
            return True
        return False
    
    @staticmethod
    def checkUser(user):
        userDb = Login.getUserDb(user)
        if userDb is None:
            return False
        return True
    
    @staticmethod
    def checkLogin(user, password):
        if Login.checkUser(user) and Login.checkPassword(user, password):
            return True
        return False
    
    @staticmethod
    def deleteLogin(user, password):
        dados = Login._readDb(Login.base)
        if Login.checkLogin(user, password):
            del dados[user]
            Login._writeDb(Login.base, dados)
            return True
        return False
    
    @staticmethod
    def getAllUsers():
        return Login._readDb(Login.base)
    
print(Login.getAllUsers())