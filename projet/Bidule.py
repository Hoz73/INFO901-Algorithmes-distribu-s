from abc import ABC, abstractmethod

class Message(ABC):
    def __init__(self, paylode):
        self.paylode = paylode
        self.estamp = None

    def getPaylode(self):
        return self.paylode

    def setEstamp(self,estamp):
        self.estamp = estamp

    def getEstamp(self):
        return self.estamp
    

class MessageAsynchronize(Message):
    def __init__(self, source, destination, paylode):
        super().__init__(paylode)
        self.source = source
        self.destination = destination
    
    def getSource(self):
        return self.source
    
    def getDestination(self):
        return self.destination

    def setDestination(self,dest):
        self.destination = dest
    
    def setSource(self,source):
        self.source = source

class Token():
    def __init__(self, destination):
        self.destination = destination
    
    def getDestination(self):
        return self.destination

    def setDestination(self,dest):
        self.destination = dest

class MessageSynchronize(Message):
    def __init__(self, source, paylode):
        self.source = source
        self.paylode = paylode

    def getSource(self):
        return self.source

    def getPaylode(self):
        return self.paylode

class MessageSystem(Message):
    def __init__(self, source, paylode):
        super().__init__(paylode)
        self.source = source
    
    def getSource(self):
        return self.source
    
    def setSource(self,source):
        self.source = source