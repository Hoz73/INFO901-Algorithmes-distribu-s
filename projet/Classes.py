import queue
from pyeventbus3.pyeventbus3 import *
from time import sleep
from Bidule import Message, Token, MessageSynchronize

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
        while lock != False:
            sleep(1)
            print("incClock : le semaphort n'est pas disponible")
        self.lock = True
        self.horloge += 1
        self.lock = False
            
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

    @subscribe(threadMode = Mode.PARALLEL, onEvent=Message)
    def OnReceive(self,event):
        if self.getPName() != event.getSource():
            if(event.getDestination() == "brodcast" or self.getPName() == event.getDestination()):
                self.modifyHorlogeOnEvent(event)
                self.appendBOL(event)
    
    @subscribe(threadMode = Mode.PARALLEL, onEvent=Token)
    def onToken(self,event):
        if (self.getPName() == event.getDestination()) :
            if self.state == "request":
                self.state = "SC"
                while(self.state != "release"):
                    print(self.getPName()+" je suis en SC")
                    sleep(1)
            event.setDestination(self.next(event.getDestination()))
            self.sendToToken(event)

    def next(self,dest):
        return "P"+str((int(dest[1]) + 1)%3)
    
    def requestSC(self):
        self.state = "request"
        while self.statue != "SC":
            sleep(1)

    def releaseSC(self):
        self.state = "release"

    def appendBOL(self,element):
        self.queue.put(element)
    
    def getBOL(self):
        return self.queue.get()
    
    def sizeBOL(self):
        self.queue.qsize()

    def emptyBOL(self):
        self.queue.empty()

    def modifyHorlogeOnEvent(self,event):
        while self.lock != False:
            sleep(1)
            print("modifyHorloge : le semaphore n'est pas disponible")
        self.lock = True
        self.horloge = self.horloge if self.horloge > event.getEstamp() else event.getEstamp()
        self.incClock()
        self.lock = False

    def createToken(self):
        t = Token(None,None,"P1",None)
        self.sendToToken(t)

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageSynchronize)
    def onSynchronize(self,event):
        if self.getName() != event.getSource():
            print("je fais + 1")
            self.countSyn +=1
            

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageSynchronize)
    def onSynchronize(self,event):
        if self.getName() != event.getSource():
            print("je fais + 1")
            self.countSyn +=1

    def synchronize(self):
        m3 = MessageSynchronize(None,self.getPName(),None,"Message synchronized")
        PyBus.Instance().post(m3)
        print(self.getName() + " send")
        while self.countSyn != self.nbProc -1 :
            print(self.countSyn)
            sleep(1)
        print("MessageSynchronize done")

    def broadcastSync(self,message,source):
        pass

    def sendToSync(self,message,dest):
        pass
