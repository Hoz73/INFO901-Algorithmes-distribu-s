import queue
from pyeventbus3.pyeventbus3 import *
from time import sleep
from Bidule import Message, Token, MessageSynchronize, MessageAsynchronize

class Com():
    def __init__(self, pName):
        self.horloge = 0
        self.state = None
        self.lock = False
        self.pName = pName
        self.queue = queue.Queue()
        self.countSyn = 0
        self.nbProc = 3
        PyBus.Instance().register(self, self)

    def setHorloge(self,horloge):
        self.horloge = horloge

    def getHorloge(self):
        return self.horloge
    
    def getPName(self):
        return self.pName
    
    def incClock(self):
        while (self.lock != False):
            sleep(1)
            print("incClock : le semaphore n'est pas disponible")
        print("incClock : j'ai le semaphore")
        self.lock = True
        self.horloge += 1
        self.lock = False
        print("incClock : je donne le semaphore")
            
    def sendTo(self,message,to):
        self.incClock()
        message.setEstamp(self.horloge)
        message.setDestination(to)
        PyBus.Instance().post(message)

    def sendToToken(self,token):
        PyBus.Instance().post(token)

    def brodcast(self,message):
        self.incClock()
        message.setEstamp(self.horloge)
        PyBus.Instance().post(message)

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageAsynchronize)
    def OnReceive(self,event):
        if self.getPName() != event.getSource():
            if(event.getDestination() == "brodcast" or self.getPName() == event.getDestination()):
                self.modifyHorlogeOnEvent(event)
                self.appendBOL(event)
                #print("je suis "+ self.getPName() + ", BOL :"+str(self.getBOL().getSource()))
    
    @subscribe(threadMode = Mode.PARALLEL, onEvent=Token)
    def onToken(self,event):
        if (self.getPName() == event.getDestination()) :
            if self.state == "request":
                #print(self.getPName() +" : Je prends la section critique")
                self.state = "SC"
                while(self.state != "release"):
                    print(self.getPName()+" je suis en SC")
                    sleep(1)
            event.setDestination(self.next(event.getDestination()))
            sleep(3)
            self.sendToToken(event)

    def next(self,dest):
        return "P"+str((int(dest[1]) + 1)%3)
    
    def requestSC(self):
        self.state = "request"
        
        while self.state != "SC":
            sleep(1)

    def releaseSC(self):
        self.state = "release"

    def appendBOL(self,element):
        self.queue.put(element)
    
    def getBOL(self):
        return self.queue.get()
    
    def sizeBOL(self):
        return self.queue.qsize()

    def emptyBOL(self):
        self.queue.empty()

    def modifyHorlogeOnEvent(self,event):
        while self.lock != False:
            sleep(1)
            print("modifyHorloge : le semaphore n'est pas disponible")
        print("modifyHorloge : j'ai le semaphore")
        self.lock = True
        self.horloge = self.horloge if self.horloge > event.getEstamp() else event.getEstamp()
        self.horloge +=1
        self.lock = False
        print("modifyHorloge : je donne le semaphore")

    def createToken(self):
        t = Token("P0")
        self.sendToToken(t)

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageSynchronize)
    def onSynchronize(self,event):
        if self.getPName() != event.getSource():
            self.countSyn +=1
            

    def synchronize(self):
        m3 = MessageSynchronize(self.getPName(),"Message synchronized")
        PyBus.Instance().post(m3)
        while self.countSyn != self.nbProc -1 :
            sleep(1)
        print(self.getPName() + " est synchronized")

    def broadcastSync(self,source,message):
        if self.getPName() != source :
            print(self.getPName()+" : je recoie")
            while self.sizeBOL() == 0 :
                print(self.getPName()+ ", "+str(self.sizeBOL()))
                sleep(1)
            elem = self.getBOL()
            if elem.getSource() == source :
                message.setSource(self.getPName())
                self.sendTo(message,source)
            print("size " +  str(self.sizeBOL()))
            while self.sizeBOL() == 0 :
                sleep(1)
            print(self.getPName() + " est débloqué !!!")
        else:
            print(self.getPName()+" : je brodcast")
            self.brodcast(message)
            while self.sizeBOL() != self.nbProc - 1 :
                sleep(1)
            self.brodcast(message)
            print(self.getPName() + " broadcastSync reussi !!!")

    def sendToSync(self,dest,message):
        if self.getPName() != dest:
            self.sendTo(message,dest)
            while self.sizeBOL() == 0:
                sleep(1)
            print(self.getPName() + " : est débloqué en tant que sender")
    
    def recvFromSync(self,source,message):
        if self.getPName() != source:
            print(str(self.sizeBOL()))
            while self.sizeBOL() == 0:
                print("j'attends de recevoir un message")
                sleep(1)
            if self.getBOL().getSource() == source :
                message.setSource(self.getPName())
                self.sendTo(message,source)
                print(self.getPName() + " recois + débloqué")
