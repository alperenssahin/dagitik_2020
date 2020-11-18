#!/usr/bin/python3
import socket
import random
import threading
import uuid
import sys

class Worker(threading.Thread):
    def __init__(self,thread_ID,clientsocket):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.thread_ID = str(thread_ID)
    def run(self):
        print("thread started : " + self.thread_ID)
        randomNumber = -1
        isStarted = False
        currentError = 0
        while True:
            data = self.clientsocket.recv(1024)
            if "TRY" in data:
                if isStarted:
                    if currentError > totalErrorCount:
                        isStarted = False
                        protocol = "END" #hamle bitti
                    else:
                        try:
                            g = int(data.split(" ")[1])
                            result = guess(randomNumber,g)
                            if result == -1:
                                currentError += 1
                                protocol = "LTH " + str(currentError)
                                
                            elif result == 0:
                                currentError += 1
                                protocol = "GTH " + str(currentError)
                                
                            else:
                                protocol = "WIN"
                                isStarted = False
                        except:
                            protocol = "PRR"
                else:
                    protocol = "GRR"
                    
            elif "QUI" in data:
                protocol = "BYE"
                protocol = protocol +  "\r\n"
                self.clientsocket.send(protocol.encode('ascii'))
                self.clientsocket.close()
                break
            elif "STA" in data:
                if not isStarted:
                    isStarted = True
                    currentError = 0
                    randomNumber = random.randint(1, 99)
                    protocol = "RDY " + str(totalErrorCount)
                else:
                    currentError = 0
                    randomNumber = random.randint(1, 99)
                    protocol = "RDY "+ str(totalErrorCount)
            elif "TIC" in data:
                protocol = "TOC"
            
            else:
                protocol = "ERR"

            protocol = protocol +  "\r\n"
            self.clientsocket.send(protocol.encode('ascii'))

serversocket = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"

port = int(sys.argv[1])

print("socket started")

serversocket.bind((host, port))

serversocket.listen(5)
totalErrorCount = random.randint(5, 11)


def guess(n,guess):
    if guess < n:
        return -1
    elif guess > n:
        return 0
    else:
        return 1

protocol = ""
threads = []
while True:
    clientsocket,addr = serversocket.accept()
    print("Baglanti %s" % str(addr))
    worker = Worker(uuid.uuid1(),clientsocket)
    worker.start()
    threads.append(worker)


