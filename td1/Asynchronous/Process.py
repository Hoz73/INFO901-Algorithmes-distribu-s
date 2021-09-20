from threading import Lock, Thread

from time import sleep

#from geeteventbus.subscriber import subscriber
#from geeteventbus.eventbus import eventbus
#from geeteventbus.event import event

#from EventBus import EventBus
from Bidule import Message, Token, BrodcastMessage, MessageSynchronize

from pyeventbus3.pyeventbus3 import *

class Process(Thread):
    
    def __init__(self,name):
        Thread.__init__(self)
        self.horloge = 0
        self.setName(name)

        self.statue= None
        PyBus.Instance().register(self, self)

        self.nbProc = 3
        self.alive = True
        self.start()

        self.countSyn =0
        
    @subscribe(threadMode = Mode.PARALLEL, onEvent=Message)
    def process(self, event): 
        self.onBroadcast(event)
        #self.onRecive(event)
            

    def brodcast(self,message):
        self.horloge +=1
        message.setEstamp(self.horloge)
        PyBus.Instance().post(message)

    @subscribe(threadMode = Mode.PARALLEL, onEvent=BrodcastMessage)
    def onBroadcast(self,event):
        if self.getName() != event.getSource():
            self.horloge = self.horloge if self.horloge > event.getEstamp() else event.getEstamp()
            self.horloge +=1
            print(self.getName() + ' Source : ' + event.getSource()+ ', Destination :'+event.getDestination()+', Paylode :'+event.getPaylode()+ ", Horlog : " +str(self.horloge))

    def sendTo(self,message,to):
        self.horloge +=1
        message.setEstamp(self.horloge)
        message.setDestination(to)
        PyBus.Instance().post(message)

    @subscribe(threadMode = Mode.PARALLEL, onEvent=Message)
    def onRecive(self,event):
        if self.getName() == event.getDestination():
            self.horloge = self.horloge if self.horloge > event.getEstamp() else event.getEstamp()
            self.horloge +=1 
            print(self.getName() + ' Source : ' + event.getSource()+ ', Destination :'+event.getDestination()+', Paylode :'+event.getPaylode()+ ", Horlog : " +str(self.horloge))
            return event.getPaylode()
    
    @subscribe(threadMode = Mode.PARALLEL, onEvent=Token)
    def onToken(self,event):
        if self.getName() == event.getDest() :
            if self.statue == "request":
                self.statue = "SC"
                while(self.statue != "release"):
                    print("je suis SC")
                    sleep(1)
                print("sorti")
            event.setDest(self.next(event.getDest()))
            self.sendToToken(event)

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageSynchronize)
    def onSynchronize(self,event):
        if self.getName() != event.getSource():
            print("je fais + 1")
            self.countSyn +=1
            


    def synchronize(self):
        m3 = MessageSynchronize(self.getName(),"message synchronized", 0)
        PyBus.Instance().post(MessageSynchronize(self.getName(),"message synchronized", 0))
        print(self.getName() + " send")
        while self.countSyn != self.nbProc -1 :
            print(self.countSyn)
            sleep(1)
        print("MessageSynchronize done")


    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P1":
                m1 = Message("test pour dire bonjour", "P1", "rémi", "coucou toi")
                m2 = Message("test2", "P1", "Momo", "hello toi")
                print(self.getName() + " send: " + m1.getTitre())
                ############################# on synchronize ################
            
            if loop == 0 and self.getName()=="P0":
                print('uiii')
                loop = 9
            if loop == 0 and self.getName()=="P1":
                print('uiiiiiiiii')
                loop = 5
            if loop == 10:
                self.synchronize()
                ############################# on brodcast####################
                #self.brodcast(m1)
                ############################## on send ######################
                #self.sendTo(m1,"P2")
            ##################################### on Token ##################
            # if self.getName() == 'P0' and loop==0:
            #     t = Token("P1")
            #     #token = t.genereteToken()
            #     self.sendToToken(t)

            # if loop == 2:
            #     if self.getName() == "P1":
            #         self.request()
            #         sleep(1)
            #         print("je dois passer dans release")
            #         self.release()
            #         print(" je suis release normalement")
            
            # if loop == 5:
            #     if self.getName() == "P2":
            #         self.request()
            #         sleep(3)
            #         print("je dois passer dans release")
            #         self.release()
            #         print(" je suis release normalement")
            ############################# on synchronize #######################
            
            loop+=1
        print(self.getName() + " stopped")

    def next(self,dest):
        return "P"+str((int(dest[1]) + 1)%3)
        
    def sendToToken(self,token):
        self.horloge += 1
        PyBus.Instance().post(token)

    def request(self):
        self.statue = "request"
        print(self.statue)
        while(self.statue != "SC"):
            print(self.statue)
            sleep(1)

    def release(self):
        self.statue = "release"
        print(self.statue)

    def stop(self):
        self.alive = False
        self.join()


