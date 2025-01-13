import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.yahoo_api import Info
from app.data import Data

class Ativo:
    def __init__(self, ativo, custodia = None, categoria = None, codigo = None, quantidade = None, data = None, valor = None):
        if isinstance(ativo, dict):
            self.nome = ativo["nome"]
            self.custodia = ativo["custodia"]
            self.categoria = ativo["categoria"]
            self.codigo = ativo.get("codigo", None)
            self.quantidade = ativo["quantidade"]
            if isinstance(ativo["data"], str):
                self.data = Data(compra = { 
                    ativo["data"] : {
                        "quantidade": ativo["quantidade"],
                        "valor": ativo["valor"]
                        }
                    })
            elif isinstance(ativo["data"], dict):
                self.data = Data(compra = ativo["data"]["compra"], venda = ativo["data"]["venda"]) 
        elif isinstance(ativo, str):
            self.nome = ativo
            self.custodia = custodia
            self.categoria = categoria
            self.codigo = codigo
            self.quantidade = quantidade
            if isinstance(data, str):
                self.data = self.data = Data(compra = { 
                    data : {
                        "quantidade": quantidade,
                        "valor": valor
                        }
                    })
        if self.codigo is not None:
            self.info = Info(self.codigo)
            if self.info.getCurrency() == "USD":
                self.conversao = Info("BRL=X")
        
    def compra(self, quantidade, data, valor = None):
        self.quantidade += quantidade
        if valor is None:
            self.data.add(data, quantidade, self.info.getValue(data))
        else:
            self.data.add(data, quantidade, valor)
    
    def venda(self, quantidade, data, valor = None):
        self.quantidade -= quantidade
        if valor is None:
            self.data.add(data, quantidade, self.info.getValue(data), compra = False)
        else:
            self.data.add(data, quantidade, valor, compra = False)

    def getNome(self):
        return self.nome

    def getCustodia(self):
        if self.custodia is None:
            return "Nao identificada"
        return self.custodia
    
    def getCodigo(self):
        return self.codigo
    
    def getQuantidade(self):
        return self.quantidade
    
    def getData(self):
        return self.data
    
    def getValor(self):
        if self.codigo is not None:
            if self.conversao:
                return self.info.getValue()*self.conversao.getValue()
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
        if self.categoria is None:
            return "Nao identificada"
        return self.categoria
    
    def getPrecoMedio(self):
        quantidadeTotal = 0
        precoAcumulado = 0
        info = self.data.get()
        for data in info["compra"]:
            quantidadeTotal += info["compra"][data]["quantidade"]
            precoAcumulado += info["compra"][data]["valor"]
        
        return precoAcumulado/quantidadeTotal

    def getLucro(self):
        precoMedio = self.getPrecoMedio()
        return (self.info.getValue() - precoMedio)*self.quantidade
    
    def get(self):
        ativo = {
            "nome": self.nome,
            "custodia": self.custodia,
            "categoria": self.categoria,
            "codigo": self.codigo,
            "quantidade": self.quantidade,
            "data": self.data.get(),
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