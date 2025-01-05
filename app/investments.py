import os
from reader import Reader

class Investment(Reader):
    base = os.path.join(os.getcwd(), "db","investment.json")

    @staticmethod
    def createInvestment(user):
        dados = Investment._readDb(Investment.base)
        if dados.get(user, None) is not None:
            return False
        dados[user] = {}
        Investment._writeDb(Investment.base, dados)

    @staticmethod
    def getAllInvestments():
        return Investment._readDb(Investment.base)
    
    @staticmethod
    def getUserInvestment(user):
        dados = Investment._readDb(Investment.base)
        return dados.get(user, None)

    @staticmethod
    def deleteUserInvestment(user):
        dados = Investment._readDb(Investment.base)
        if dados.get(user, None) is not None:
            del dados[user]
        Investment._writeDb(Investment.base, dados)