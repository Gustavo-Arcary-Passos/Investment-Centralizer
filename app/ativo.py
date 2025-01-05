from yahoo_api import Info

class Ativo:
    def __init__(self, ativo):
        self.nome = ativo["nome"]
        self.custodia = ativo["custodia"]
        self.categoria = ativo["categoria"]
        self.codigo = ativo.get("codigo", None)
        self.quantidade = ativo["quantidade"]
        self.data = ativo["data"] # dicionario com dias de compra e venda do ativo, com valor de fechamento do dia
        if self.codigo is not None:
            self.info = Info(self.codigo)
        
    def compra(self, quantidade, data, valor = None):
        self.quantidade += quantidade
        self.data["compra"][data]["quantidade"] = quantidade
        if valor is None:
            self.data["compra"][data]["valor"] = self.info.getValue(data)
        else:
            self.data["compra"][data]["valor"] = valor
    
    def venda(self, quantidade, data, valor = None):
        self.quantidade -= quantidade
        self.data["venda"][data]["quantidade"] = quantidade
        if valor is None:
            self.data["venda"][data]["valor"] = self.info.getValue(data)
        else:
            self.data["compra"][data]["valor"] = valor

    def getNome(self):
        return self.nome

    def getCustodia(self):
        return self.custodia
    
    def getCodigo(self):
        return self.codigo
    
    def getQuantidade(self):
        return self.quantidade
    
    def getValor(self):
        if self.codigo is not None:
            return self.info.getValue()
        return None
    
    def getPrecoAtual(self):
        valor = self.getValor()
        if valor is None:
            precoAcumulado = self.quantidade
        else:
            precoAcumulado = valor * self.quantidade
        return precoAcumulado
    
    def getCategoria(self):
        return self.categoria
    
    def getPrecoMedio(self):
        quantidadeTotal = 0
        precoAcumulado = 0
        for data in self.data["compra"]:
            quantidadeTotal += data["quantidade"]
            precoAcumulado += data["valor"]
        
        return precoAcumulado/quantidadeTotal

    def getLucro(self):
        precoMedio = self.getPrecoMedio()
        return (self.info.getValue() - precoMedio)*self.quantidade
    
    def getAtivo(self):
        ativo = {
            "nome": self.nome,
            "custodia": self.custodia,
            "categoria": self.categoria,
            "codigo": self.codigo,
            "quantidade": self.quantidade,
            "data": self.data,
        }

        return ativo
    
    def setNome(self, nome):
        self.nome = nome

    def setCustodia(self, custodia):
        self.nome = custodia

    def setCodigo(self, codigo):
        self.codigo = codigo
    
    def setQuantidade(self, quantidade):
        self.quantidade = quantidade

    def setCategoria(self, categoria):
        self.categoria = categoria

# aaplInfo = {
#     "nome" : "Apple",
#     "custodia": "Rico",
#     "codigo": "AAPL",
#     "quantidade": 3.5,
#     "data": "2023-12-15"
# }
# aapl = Ativo(aaplInfo)
# print(aapl.getLucro())