import json
import os

class Reader:

    @staticmethod
    def _readDb(filePath):
        if not os.path.exists(filePath) or os.path.getsize(filePath) == 0:
            return {}
        
        with open(filePath, "r") as arquivo:
            dados = json.load(arquivo)
        return dados

    @staticmethod
    def _writeDb(filePath, dados):
        with open(filePath, "w") as arquivo:
            json.dump(dados, arquivo)
        return True