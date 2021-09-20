from mpi4py import MPI
import math
import sys
import time

comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()

def DiffusionAnneau(sender, msg):

    lastNode = (sender + size -1)%size
    nextNode = (me + 1)%size
    prevNode = (me - 1 + size)%size
    buf = [msg]
    if me == sender:
        comm.send(buf, dest=nextNode, tag=99)
        print("im the sender "+str(me)+", i sent "+str(buf))
    elif me != lastNode:
        comm.recv(source=prevNode, tag=99)
        print("im the reciver "+str(me)+", i recived from "+str(prevNode))
        comm.send(buf, dest=nextNode, tag=99)
        print("im the reciver "+str(me)+", i sent to "+str(nextNode))
    else:
        comm.recv(source=prevNode, tag=99)
        print("im the last "+str(me)+", i recive from "+str(prevNode))

def scatter(sender):

    if me == sender:
        buf = ["0","1","2","3","4","5","6","7"]
        tabDec =[]
        nbElement = len(buf)//(size-1)
        debut = 0
        fin = nbElement
        for i in range(1,size-1):
            tabDec.append(buf[debut:fin])
            debut = fin
            fin = debut + nbElement
        tabDec.append(buf[debut:len(buf)+1])
        index = 0
        for i in range(0, size):
            if i != me:
                comm.send(tabDec[index], dest=i, tag=99)
                index += 1      
    else:
        msg = comm.recv(source=sender, tag=99)
        print("I'm "+str(me)+": i recived  from "+ str(sender))
        print(msg)

#non testé
def scatterProf(sender):

    buf = ["0","1","2","3","4","5","6","7"]
    nbElem = len(buf)
    chunks = nbElem//size
    rest = nbElem - chunks * (size-1)
    if me == sender:
        for i in range(1,size-1):
            comm.send(buf[i*chunks:(i+1)*chunks],dest=i,tag=99)
            comm.send(buf[(size-1)*chunks:],dest=size-1,tag=99)
            print(buf[0:chunks])
    else:
        msg = comm.recv(source=sender, tag=99)
        print(msg)


def Gather(reciver):

    if me == reciver:
        res = []
        for i in range(0,size):
            if i != reciver:
                msg = comm.recv(source=i, tag=99)
                res.append(msg)
                print(res)
            else:
                res.append(i)
                print(res)
        print('je suis le noeuds '+ str(me))
    else:
        comm.send(me,dest=reciver, tag=99)

#non testé
def GeatherProf(reciver):

    tab = ["0","1","2","3","4","5","6","7"]
    if me == reciver:
        bigtab = tab[:]
        for i in range(0,size):
            if me != reciver:
                msg = comm.recv(source=i, tag=99)
                bigtab += msg
        print(bigtab)
    else:
        comm.send(me,dest=reciver, tag=99)


def AllGather():

    for i in range(0,size):
        Gather(i)

class Message:
    msg = ""
    step = None

    def __init__(self, msg, step, fr):
        self.msg = msg
        self.step = step
        self.fr = fr


def broadcast_hypercube(fr, msg):

    higher_step = math.ceil(math.log2(size))
    message = None
    if fr == me:
        message = Message(msg, 0, me)
    else:
        message = comm.recv(source=MPI.ANY_SOURCE)
        print(f"Worker {me} message {message.msg} received from {message.fr} ")
    for i in range(message.step, higher_step):
        next = (me + 2 ** i) % size
        if next < size:
            comm.send(Message(message.msg, i+1, me), next)


def scatterRemi():
    
    if (me == 0):
        dataVec = ["0", "1", "2", "3", "4", "5", "6"]
        nbElem = len(dataVec)
        chunks = (len(dataVec)//size)

        print("myData : ")
        print(dataVec[0:chunks])
        print("I'm <"+str(me)+">: send ")
        for i in range (1, size-1):
            comm.send(dataVec[i*chunks:(i+1)*chunks], dest=i, tag=99)
        comm.send(dataVec[(size-1)*chunks:nbElem], dest=size-1, tag=99)
    else:
        buf = comm.recv(source=0, tag=99)
        print("I'm <"+str(me)+">: receive ")
        print(buf)

#non testé
def gatherNiko(_to):
    mydata = ["0", "1", "2", "3", "4", "5", "6"]
    if(me == _to):
        data = mydata
        for i in range(0, size):
            if (me != i):
                data += comm.recv(source=i, tag=42)
                print("<"+str(me)+"> recieved from <"+str(i)+"> : "+data)
        print("\nMessage gathered : " + data)

#non testé
def manageToken():
    state ="" # à changer
    if me == 0:
        token ="" #newToken
        comm.send(token,dest=(me+1)%size)
    while(1):
        token = comm.recv(source=(me-1)%size)
        if state =="request":
            state = "SC"
            while state != "release":
                time.sleep() # à donner une valeur
        comm.send(token,dest=(me+1)%size)
        state = "null"

#non testé
def requestSC():
    state ="request"
    while(state != "SC"):
        time.sleep() # à donner une valeur

if __name__ == "__main__":
    #DiffusionAnneau(0, "ui")
    #Gather(0)
    #AllGather()
    #scatter(3)
    #broadcast_hypercube(0, "uiiiiiii")
    #scatterRemi()
    gatherNiko(0)
