import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ativo import Ativo
from app.data import Data

class Portfolio:
    def __init__(self, portfolio):
        self.ativos = portfolio["ativos"] # lista com todos os ativos
        self.estrategia = portfolio["estrategia"]

    def getAtivo(self,name,custody):
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            if ativoProcurado.getNome() == name and ativoProcurado.getCustodia() == custody:
                return ativoProcurado
        
        return None

    def getPatrimonio(self):
        patrimonioAcumulado = 0
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            patrimonioAcumulado += ativoProcurado.getPrecoAtual()
        
        return patrimonioAcumulado
    
    def getPatrimonioInvestido(self):
        patrimonioAcumulado = 0
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            patrimonioAcumulado += ativoProcurado.getPrecoMedio()*ativoProcurado.getQuantidade()
        
        return patrimonioAcumulado
    
    def getPortfolio(self):
        portifolio = {
            "ativos": self.ativos,
            "estrategia": self.estrategia,
        }
        return portifolio
    
    # Fazer de um jeito mais inteligente no qual tem uma funcao que faz o switch para cada um dos textos e se 
    # tiver mais de um incrementa o filtro
    def getAllAtivoBy(self,text=None,type="name"):
        listAtivos = []
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            if text is None:
                listAtivos.append(ativoProcurado)
            elif ativoProcurado.getNome() == text and type == "name":
                listAtivos.append(ativoProcurado)
            elif ativoProcurado.getCustodia() == text and type == "custody":
                listAtivos.append(ativoProcurado)
            elif ativoProcurado.getCategoria() == text and type == "categoria":
                listAtivos.append(ativoProcurado)
        return listAtivos
    
    def getAtivosValueBy(self,text=None,type="name"):
        listAtivo = self.getAllAtivoBy(text)
        dicby = {}
        for ativo in listAtivo:
            precoAtual = ativo.getPrecoAtual()
            if type == "name":
                nome = ativo.getNome()
                dicby[nome] = dicby.get(nome,0) + precoAtual
            elif type == "categoria":
                categoria = ativo.getCategoria()
                dicby[categoria] = dicby.get(categoria,0) + precoAtual
            elif type == "custodia":
                custodia = ativo.getCustodia()
                dicby[custodia] = dicby.get(custodia,0) + precoAtual
        return dicby
    
    def setAtivo(self,name,custody,ativo):
        for pos in range(0,len(self.ativos)):
            ativoProcurado = Ativo(self.ativos[pos])
            if ativoProcurado.getNome() == name and ativoProcurado.getCustodia() == custody:
                self.ativos[pos] = ativo

    def addAtivoPortfolio(self,ativo):
        updateAtivo = self.getAtivo(ativo.getNome(),ativo.getCustodia())
        if updateAtivo is not None:
            ativoData = ativo.getData().get()
            for data in ativoData["compra"]:
                updateAtivo.compra(ativoData["compra"][data]["quantidade"],data,ativoData["compra"][data]["valor"])
            for data in ativoData["venda"]:
                updateAtivo.venda(ativoData["venda"][data]["quantidade"],data,ativoData["venda"][data]["valor"])
            self.setAtivo(ativo.getNome(),ativo.getCustodia(),updateAtivo.get())
            
            return 
        self.ativos.append(ativo.get())
    

