#!/usr/bin/python3


# ONEMLI !!!!!!!!!!!!!!
# Sunucuyu kodlamaya pdf'e bakarak kodladigim icin kendi protokolumu olusturmak gafletine dustum
# Sali aksami senaryayu teams uzerinde gordum. Kodu senaryoya uyduracak vaktim olmadigi icin degistiremiyorum. Calisan bir demoyu video olarak teams'e de yukledim
import socket
import sys
import queue
import threading
from datetime import datetime
print(datetime.now())
class ReadThread(threading.Thread):
    def __init__(self,conn,queue,loggerQueue,fihrist,client):
        threading.Thread.__init__(self)
        self.conn = conn
        self.queue = queue
        self.logger = loggerQueue
        self.fihrist = fihrist
        self.username = ""
        self.client = client
        
    def run(self):
        print("Read Thread Started")
        self.logger.put(self.client + " read thread started")
        while True:
            data = self.conn.recv(1024)
            data = data.decode("utf-8").strip()
            if "CLOSE" in data:
                self.queue.put("CLOSE")
                break
            self.parser(data)
    
    def parser(self,data):
        data = data.replace('\n','')
        data = data.replace('\r','')
        if "NIC" == data.split(" ")[0]:
            self.username = data.split(" ")[1]
            self.fihrist[self.username] = self.queue
            self.logger.put(self.username + " user created")
            for user in self.fihrist.keys():
                self.fihrist[user].put("JOIN " + self.username)
        else:
            if self.username != "":
                dArray = data.split(" ")
                if "TO" == data.split(" ")[0]:
                    try:
                        self.fihrist[dArray[1]].put("MSG FROM:"+ self.username +" "+dArray[2])
                        self.logger.put(self.username + " user is sending message to "+dArray[1])
                    except:
                        self.queue.put("ERR invalidMessageFormat")
                        self.logger.put(self.username + " user is sending message error")
                elif "ALL" == data.split(" ")[0]:
                    try:
                        for user in self.fihrist.keys():
                            self.fihrist[user].put("MSGALL FROM:" + self.username +" "+ dArray[1])
                    except:
                        self.queue.put("ERR inValidAllMessageFormat")
                        self.logger.put(self.username + " user is sending all message error")
                else:
                    self.queue.put("ERR inValidProtocol")
                    self.logger.put(self.username + " user sent a Invalid protocol message")
            else:
                self.queue.put("ERR undefinedUsername")
                self.logger.put("Error undefined username")
        

class WriteThread(threading.Thread):
    def __init__(self,conn,queue,loggerQueue,fihrist,client):
        threading.Thread.__init__(self)
        self.conn = conn
        self.queue = queue
        self.logger = loggerQueue
        self.fihrist = fihrist
        self.client = client
    def run(self):
        print("Write Thread Started")
        self.logger.put(self.client + " write thread started")
        while True:
            data = self.queue.get()
            if data == "CLOSE":
                self.conn.send("connection closed".encode('ascii'))
                self.logger.put(self.client + " closing")
                break
            data = data+"\n\r"
            self.conn.send(data.encode('ascii'))
            self.logger.put(self.client + " data sent")
            
class LoggerThread(threading.Thread):
    def __init__(self,loggerQueue):
        threading.Thread.__init__(self)
        self.logger = loggerQueue
    def run(self):
        print("Logger Thread Started")
        while True:
            data = self.logger.get()
            print("logger")
            data = self.info(data)
#            print(data)
            f = open("./messages.log","a")
            f.write(data)
            f.close()
    
    def info(self,info):
        now = datetime.now()
        return "[" +now.strftime("%d/%m/%Y %H:%M:%S")+"] :: " + info + "\n"

serversocket = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"

port = 3001

print("socket started")

serversocket.bind((host, port))

serversocket.listen(5)

logQueue = queue.Queue()
fihrist = {}

loggerThread = LoggerThread(logQueue)
loggerThread.start()

while True:
    clientsocket,addr = serversocket.accept()
    print("Baglanti %s" % str(addr))
    
    #her baglanti icin 1 kuyruk ve 2 thread olustur
    #readThread
    #writeThread
    #threadQueue
    
    cliQueue = queue.Queue()
    readThread = ReadThread(clientsocket,cliQueue,logQueue,fihrist,str(addr))
    readThread.start()

    writeThread = WriteThread(clientsocket,cliQueue,logQueue,fihrist,str(addr))
    writeThread.start()
    
   
    
    
    
