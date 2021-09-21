from threading import Lock, Thread

from time import sleep

#from geeteventbus.subscriber import subscriber
#from geeteventbus.eventbus import eventbus
#from geeteventbus.event import event

#from EventBus import EventBus
from Bidule import Message, Token, BrodcastMessage, MessageSynchronize
from Classes import Com

from pyeventbus3.pyeventbus3 import *

class Process(Thread):
    
    def __init__(self,name):
        Thread.__init__(self)
        self.horloge = 0
        self.setName(name)
        self.comm = Com(self.getName())

        self.statue= None
        PyBus.Instance().register(self, self)
        if self.getName == "P2" :
            self.comm.createToken()
        
        self.alive = True
        self.start()
            

    #Méthode à conserver
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

    def stop(self):
        self.alive = False
        self.join()


