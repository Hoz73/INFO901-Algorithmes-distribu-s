from uuid import uuid4

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

class BrodcastMessage():
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
        
class Token():
    def __init__(self,dest):
        self.dest = dest

    def genereteToken(self):
        return uuid4()

    def getDest(self):
        return self.dest

    def setDest(self,dest):
        self.dest = dest

class MessageSynchronize():
    def __init__(self,source,message,nbProcess):
        self.source = source
        self.estamp = None
        self.message = message
        self.nbProcess = nbProcess

    def getSource(self):
        return self.source

    def getNbProcess(self):
        return self.nbProcess
    def setNbProcess(self, nb):
        self.nbProcess = nb