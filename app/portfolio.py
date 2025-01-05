from ativo import Ativo

class Portfolio:
    def __init__(self, portfolio):
        self.ativos = portfolio["ativos"] # lista com todos os ativos
        self.estrategia = portfolio["estrategia"]

    def getAtivo(self,name):
        for ativo in self.ativos:
            ativoProcurado = Ativo(ativo)
            if ativoProcurado.getNome() == name:
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