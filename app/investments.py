import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.reader import Reader
from app.portfolio import Portfolio

class Investment(Reader):
    base = os.path.join(os.getcwd(), "db","investment.json")

    @classmethod
    def getFilePath(cls):
        return cls.base

    @staticmethod
    def createInvestment(user, filePath = None):
        filePath = filePath or Investment.getFilePath()
        dados = Investment._readDb(filePath)
        if dados.get(user, None) is not None:
            return False
        dados[user] = {
            "ativos": [],
            "estrategia": {}
        }
        Investment._writeDb(filePath, dados)

    @staticmethod
    def getAllInvestments(filePath = None):
        filePath = filePath or Investment.getFilePath()
        return Investment._readDb(filePath)
    
    @staticmethod
    def getUserInvestment(user, filePath = None):
        filePath = filePath or Investment.getFilePath()
        dados = Investment._readDb(filePath)
        return dados.get(user, None)

    @staticmethod
    def deleteUserInvestment(user, filePath = None):
        filePath = filePath or Investment.getFilePath()
        dados = Investment._readDb(filePath)
        if dados.get(user, None) is not None:
            del dados[user]
        Investment._writeDb(filePath, dados)

    @staticmethod
    def updateUserInvestment(user,userPortfolio, filePath = None):
        filePath = filePath or Investment.getFilePath()
        dados = Investment._readDb(filePath)
        dados[user] = userPortfolio.getPortfolio()
        Investment._writeDb(filePath, dados)