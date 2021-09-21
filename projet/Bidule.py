class Message():
    def __init__(self, titre, source, destination, paylode):
        self.source = source
        self.destination = destination
        self.paylode = paylode
        self.titre = titre
        self.estamp = None

    def getTitre(self):
        return self.titre

    def getSource(self):
        return self.source
    
    def getDestination(self):
        return self.destination
    
    def getPaylode(self):
        return self.paylode

    def setEstamp(self,estamp):
        self.estamp = estamp

    def getEstamp(self):
        return self.estamp
    
    def setDestination(self,dest):
        self.destination = dest

class Token(Message):
    pass

class MessageSynchronize(Message):
    pass