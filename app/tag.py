
class Tag():
    def __init__(self,tagName = None, tagColor = None, tag = None):
        if tag is None:
            self.tag = tagName
            self.color = tagColor
        else :
            self.tag = tag["name"]
            self.color = tag["color"]

    def __str__(self):
        return f"{{'name': '{self.tag}','color':[{self.color[0]},{self.color[1]},{self.color[2]}]}}"

    def getName(self):
        return self.tag
    
    def getColor(self):
        return self.color
    
    def setColot(self, newColor):
        self.color = newColor

    def get(self):
        tagDic = {
            'name' : self.tag,
            'color': self.color
        }
        return tagDic
    