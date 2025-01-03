import json
import os

class Login:
    base = os.path.join(os.getcwd(), "db","login.json")
    
    @staticmethod
    def _readDb():
        if not os.path.exists(Login.base) or os.path.getsize(Login.base) == 0:
            return {}
        
        with open(Login.base, "r") as arquivo:
            dados = json.load(arquivo)
        return dados

    @staticmethod
    def _writeDb(dados):
        with open(Login.base, "w") as arquivo:
            json.dump(dados, arquivo)
        return True

    @staticmethod
    def createLogin(user, password):
        dados = Login._readDb()
        if dados.get(user, None) is not None:
            return False
        dados[user] = password
        return Login._writeDb(dados)

    @staticmethod
    def getUserDb(user):
        dados = Login._readDb()
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
        dados = Login._readDb()
        if Login.checkLogin(user, password):
            del dados[user]
            Login._writeDb(dados)
            return True
        return False