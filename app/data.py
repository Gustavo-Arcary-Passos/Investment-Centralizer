
class Data:
    def __init__(self, compra = {}, venda = {}):
        self.compra = compra
        self.venda = venda

    def get(self):
        data = {
            "compra" : self.compra,
            "venda" : self.venda
        }
        return data
    
    def add(self, data, quantidade, valor, compra = True):
        if compra:
            self.compra[data] = {"quantidade": quantidade, "valor": valor}
        else:
            self.venda[data] = {"quantidade": quantidade, "valor": valor}
    

