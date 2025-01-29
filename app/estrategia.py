
class Estrategia():
    def __init__(self, nome, estrategia = None):
        print("Estrategia")
        self.estrategyName = nome
        self.tagsFiltro = estrategia["TagsFiltro"]
        self.tagsComparacao = estrategia["TagsComparacao"]
        self.quantidadePerTag = estrategia["Quantidade"]
        pass

    def getNome(self):
        return self.estrategyName
    
    def getTagsFiltro(self):
        return self.tagsFiltro
    
    def getTagsComparacao(self):
        return self.tagsComparacao
    
    def getQuantidadePerTag(self):
        return self.quantidadePerTag