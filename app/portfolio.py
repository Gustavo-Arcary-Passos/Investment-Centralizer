import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ativo import Ativo
from app.data import Data
from app.tag import Tag
from app.estrategia import Estrategia

class Portfolio:
    def __init__(self, portfolio):
        self.ativos = portfolio["ativos"] # lista com todos os ativos
        self.estrategia = portfolio["estrategia"]
        self.tags = portfolio["tags"]

    def getAtivo(self,name,custody):
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            if ativoProcurado.getNome() == name and ativoProcurado.getCustodia() == custody:
                return ativoProcurado
        
        return None

    def getAtivoIndex(self,name,custody):
        for index in range(0,len(self.ativos)):
            ativo = self.ativos[index]
            ativoProcurado = Ativo(ativo)
            if ativoProcurado.getNome() == name and ativoProcurado.getCustodia() == custody:
                return ativoProcurado, index
        
        return None, None
    
    def getAllAtivos(self):
        return self.ativos
    
    def getAllEstrategy(self):
        return self.estrategia

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
            "tags": self.tags,
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
    
    def getTags(self):
        print(f"Get tags: {self.tags}")
        return self.tags
    
    def addTag(self,pos,tagName,tagColor):
        self.tags[pos] = {
            "name": "",
            "color": []
        }
        self.tags[pos]["name"] = tagName
        self.tags[pos]["color"] = tagColor

    def setTag(self, newTags, deleteTag = None):
        print(f"Set tags: {newTags}")
        self.tags = newTags
        print("Verifica se precisa remover tag de algum ativo")
        if deleteTag is not None:
            for i in range(len(self.ativos)):
                ativoProcurado = Ativo(self.ativos[i])
                ativoProcurado.deleteTag(deleteTag)
                self.ativos[i] = ativoProcurado.get() 
    
    def setAtivo(self,name,custody,ativo):
        for pos in range(0,len(self.ativos)):
            ativoProcurado = Ativo(self.ativos[pos])
            if ativoProcurado.getNome() == name and ativoProcurado.getCustodia() == custody:
                self.ativos[pos] = ativo

    def addAtivoPortfolio(self,ativo):
        print("addAtivoPortfolio")
        updateAtivo = self.getAtivo(ativo.getNome(),ativo.getCustodia())
        if updateAtivo is not None:
            print("update")
            ativoData = ativo.getData().get()
            for data in ativoData["compra"]:
                updateAtivo.compra(ativoData["compra"][data]["quantidade"],data,ativoData["compra"][data]["valor"])
            for data in ativoData["venda"]:
                updateAtivo.venda(ativoData["venda"][data]["quantidade"],data,ativoData["venda"][data]["valor"])
            self.setAtivo(ativo.getNome(),ativo.getCustodia(),updateAtivo.get())
            
            return 
        print("dont update")
        self.ativos.append(ativo.get())

    def editAtivoPortfolio(self,name,custody,ativoInfo):
        print("editAtivoPortfolio")
        ativoAntigo,index = self.getAtivoIndex(name,custody)
        if ativoAntigo is None:
            print("Novo")
            self.addAtivoPortfolio(ativoInfo)
            return
        dic = ativoAntigo.getData().get()
        print(dic)
        for data in dic["compra"]:
            ativoInfo.compra(dic["compra"][data]["quantidade"],data,dic["compra"][data]["valor"])

        for data in dic["venda"]:
            ativoInfo.venda(dic["venda"][data]["quantidade"],data,dic["venda"][data]["valor"])
        print(ativoInfo)
        del self.ativos[index]
        print("Update")
        self.addAtivoPortfolio(ativoInfo)

    def addEstrategia(self,estrategiaName, estrategiaDic):
        self.estrategia[estrategiaName] = estrategiaDic

    def delEstrategia(self,estrategiaName):
        del self.estrategia[estrategiaName]

    def getMatchTagsAtivo(self, ativo, tags):
        matchTags = []
        for tag in tags:
            if ativo.haveTag(tags[tag]):
                matchTags.append(tags[tag]['name'])

        return matchTags

    def getEstrategiaData(self,estrategiaName):
        print("getEstrategiaData")
        estrategiaData = {}
        print(estrategiaName)
        print(self.estrategia[estrategiaName])
        estrategia = Estrategia(estrategiaName,self.estrategia[estrategiaName])
        quantidade = estrategia.getQuantidadePerTag()
        valores = {chave: int(valor) for chave, valor in quantidade.items()}

        total = sum(valores.values())
        percentuais = {chave: (valor / total) * 100 for chave, valor in valores.items()} if total > 0 else {}
        filtros = estrategia.getTagsFiltro()
        print("estrategia.getTagsFiltro()")
        comparacao = estrategia.getTagsComparacao()
        print("estrategia.getTagsComparacao()")
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            filtrosTags = self.getMatchTagsAtivo(ativoProcurado,filtros)
            if len(filtrosTags) == len(filtros):
                comparacaoTags = self.getMatchTagsAtivo(ativoProcurado,comparacao)
                if len(comparacaoTags) > 1:
                    continue
                if comparacaoTags[0] not in estrategiaData:
                    estrategiaData[comparacaoTags[0]] = [0]
                estrategiaData[comparacaoTags[0]][0] += ativoProcurado.getPrecoAtual()
                estrategiaData[comparacaoTags[0]].append(percentuais[comparacaoTags[0]])

        return estrategiaData
