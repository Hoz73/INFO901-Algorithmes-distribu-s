from threading import Lock, Thread

from time import sleep

#from geeteventbus.subscriber import subscriber
#from geeteventbus.eventbus import eventbus
#from geeteventbus.event import event

#from EventBus import EventBus
from Bidule import Message, Token, MessageSynchronize, MessageAsynchronize
from Classes import Com

from pyeventbus3.pyeventbus3 import *

class Process(Thread):
    
    def __init__(self,name):
        Thread.__init__(self)
        self.setName(name)
        self.comm = Com(self.getName())

        #if self.getName() == "P2" :
        #    self.comm.createToken()
        
        self.alive = True
        self.start()
            

    #Méthode à conserver
    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            # if self.getName() == "P0":
            #     m1 = MessageAsynchronize(self.getName(),"P2","ceci est un test de brodcast")
            #     print(self.getName() + " send à : " + m1.getDestination())
                #self.comm.brodcast(m1)
                #self.comm.sendTo(m1,"P2")
                ############################# on synchronize ################
            
            # if loop == 0 and self.getName()=="P0":
            #     loop = 8
            # if loop == 0 and self.getName()=="P1":
            #     loop = 5
            # if loop == 10:
            #     self.comm.synchronize()
                ############################# on brodcast####################
                #self.brodcast(m1)
                ############################## on send ######################
                #self.sendTo(m1,"P2")
            ##################################### on Token ##################

            # if loop == 2:
            #     if self.getName() == "P1":
            #         self.comm.requestSC()
            #         sleep(1)
            #         print("je dois passer dans release")
            #         self.comm.releaseSC()
            #         print(" je suis release normalement")
            
            # if loop == 5:
            #     if self.getName() == "P2":
            #         self.comm.requestSC()
            #         sleep(3)
            #         print("je dois passer dans release")
            #         self.comm.releaseSC()
            #         print(" je suis release normalement")

            ############################# broadcastSyncéline #######################
            # if loop == 2 :
            #     m= MessageAsynchronize("P1","brodcast","uiiii")
            #     self.comm.broadcastSync("P1",m)
            
            ############################# send et recv sync #######################
            m= MessageAsynchronize("P1","P0","uiiii")
            if loop == 5 and self.getName() == "P1" :
                self.comm.sendToSync(m.getDestination(),m)
            if loop == 2 and  self.getName() == "P0" :
                self.comm.recvFromSync(m.getSource(),m)

            
            loop+=1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()


