#!/usr/bin/python3
import socket
import queue
import threading
from datetime import datetime

print(datetime.now())


class Room:
    def __init__(self, name, creator):
        self.name = name
        self.creator = creator
        self.adminStore = UserStore()
        self.userStore = UserStore()
        self.blockedUserStore = UserStore()
        self.adminStore.addUser(creator)
        self.userStore.addUser(creator)

    def addUser(self, user):
        if self.blockedUserStore.isUserExist(user):
            raise PermissionError
        else:
            self.userStore.addUser(user)

    def sendMessage(self, message, username):
        for user in self.userStore.userList:
            user.queue.put("OGM " + self.name + ":" + username + ":" + message)

    def userNameMapper(self, user):
        return user.name

    def getUserNames(self):
        return list(map(self.userNameMapper, self.userStore.userList))


class User:
    def __init__(self, queue):
        self.queue = queue
        self.pin = None
        self.name = None
        self.state = "OFFLINE"

    def setName(self, name):
        self.name = name

    def setPin(self, pin):
        self.pin = pin

    def setState(self, state):
        self.state = state


class UserStore:
    def __init__(self):
        self.userList = []

    def addUser(self, user):
        if not self.isUserExist(user):
            self.userList.append(user)

    def isUserExist(self, user):
        return user in self.userList

    def removeUser(self, user):
        if self.isUserExist(user):
            self.userList.pop(self.userList.index(user))

    def getUserByName(self, username):
        for user in self.userList:
            if user.name == username:
                return user
        return None


class RoomStore:
    def __init__(self):
        self.roomList = []

    def addRoom(self, room):
        if self.getRoomByName(room.name) is None:
            self.roomList.append(room)
        else:
            raise ValueError

    def isRoomExist(self, room):
        return room in self.roomList

    def removeRoom(self, room):
        if self.isUserExist(room):
            self.roomList.pop(self.roomList.index(room))

    def getRoomByName(self, roomName):
        for room in self.roomList:
            if room.name == roomName:
                return room
        return None

    def roomNamesMapper(self, room):
        return room.name

    def getRoomNames(self):
        return list(map(self.roomNamesMapper, self.roomList))


class ReadThread(threading.Thread):
    def __init__(self, conn, queue, loggerQueue, userStore, roomStore, client):
        threading.Thread.__init__(self)
        self.conn = conn
        self.queue = queue
        self.logger = loggerQueue
        self.roomStore = roomStore
        self.userStore = userStore
        self.user = User(queue)
        self.client = client
        self.validInstructions = ["NIC", "PCH", "NRM", "RLS", "RIN", "GNL", "PRV", "BAN", "RUT", "RMV", "KCK", "ULS",
                                  "MLS"]
        self.unauthenticatedInstructions = ["NIC"]
        self.endOfLineToken = "<%%$%%>"

    def run(self):
        print("Read Thread Started")
        self.logger.put(self.client + " read thread started")
        while True:
            data = self.conn.recv(1024)
            data = data.decode("utf-8").strip()
            if self.endOfLineToken not in data:
                self.queue.put("ERR eolError")
            else:
                data = data.split(self.endOfLineToken)[0]
                if "QUI" in data[:3]:
                    self.user.setState("OFFLINE")
                    self.queue.put("QUI")
                    break
                self.validationChecker(data)

    def validationChecker(self, data):
        if data[:3] not in self.validInstructions:
            self.queue.put("ERR invalidInstruction")
        else:
            self.authenticationChecker(data)

    def authenticationChecker(self, data):
        if self.user.state == "OFFLINE":
            if data[:3] not in self.unauthenticatedInstructions:
                self.queue.put("ERR unauthenticatedUserError")
            else:
                self.parser(data)
        else:
            self.parser(data)

    def nicHandler(self, body):
        name = body.split(":")[0]
        pin = body.split(":")[1]
        if self.user.state == "OFFLINE":
            storedUser = self.userStore.getUserByName(name)
            if storedUser is None:
                self.user.setState("ONLINE")
                self.user.setName(name)
                self.user.setPin(pin)
                self.userStore.addUser(self.user)
                self.queue.put("WEL " + name)
            else:
                if storedUser.state == "ONLINE":
                    # self.queue.put("RES")
                    self.queue.put("ERR authenticationDeniedUserHasAlreadyLogIn")
                else:
                    if storedUser.pin == pin:
                        storedUser.setState("ONLINE")
                        storedUser.queue = self.queue
                        self.user = storedUser
                        self.queue.put("WEL " + name)
                    else:
                        # self.queue.put("RES")
                        self.queue.put("ERR invalidPIN")
        else:
            # self.queue.put("RES")
            self.queue.put("ERR authenticationDeniedUserHasAlreadyLogIn")

    def pchHandler(self, body):
        old = body.split(":")[0]
        new = body.split(":")[1]
        if self.user.pin == old:
            self.user.setPin(new)
            self.queue.put("OKP")
        else:
            # self.queue.put("INP")
            self.queue.put("ERR pinChangeRequestDeniedOldPinHasNotMatched")

    def nrmHandler(self, body):
        room = Room(body, self.user)
        try:
            self.roomStore.addRoom(room)
            self.queue.put("OKR " + body)
        except:
            self.queue.put("ERR roomNameIsAlreadyExist")

    def rlsHandler(self):
        roomnames = ":".join(self.roomStore.getRoomNames())
        self.queue.put("RLS " + roomnames)

    def rinHandler(self, body):
        room = self.roomStore.getRoomByName(body)
        try:
            room.addUser(self.user)
            self.queue.put("OKI " + body)
        except:
            self.queue.put("ERR permissionDeniedBannedFromRoom")

    def gnlHandler(self, body):
        room = body.split(":")[0]
        message = ":".join(body.split(":")[1:])
        room.sendMessage(message, self.user.name)

    def prvHandler(self, body):
        username = body.split(":")[0]
        message = ":".join(body.split(":")[1:])
        user = self.userStore.getUserByName(username)
        if user is None:
            self.queue.put("ERR invalidUser")
        else:
            user.queue.put("OPM " + self.user.name + ":" + message)

    def banHandler(self, body):
        roomname = body.split(":")[0]
        username = body.split(":")[1]

        room = self.roomStore.getRoomByName(roomname)
        if room.adminStore.isUserExist(self.user):
            user = room.userStore.getUserByName(username)
            if user is None:
                self.queue.put("ERR userNotFound")
            else:
                if user != room.creator:
                    room.userStore.removeUser(user)
                    room.adminStore.removeUser(user)
                    room.blockedUserStore.addUser(user)
                    user.queue.put("OBN " + roomname + ":" + user.name)
                    self.queue.put("OBN " + roomname + ":" + user.name)
                else:
                    self.queue.put("ERR permissionDeniedUserIsACreator")
        else:
            self.queue.put("ERR permissionDenied")

    def rutHandler(self, body):
        room = self.roomStore.getRoomByName(body)
        room.adminStore.removeUser(self.user)
        room.userStore.removeUser(self.user)
        self.queue.put("BYR " + body)

    def rmvHandler(self, body):
        room = self.roomStore.getRoomByName(body)
        for user in room.userStore:
            user.queue.put("BYR " + body)
        self.roomStore.removeRoom(room)

    def kckHandler(self, body):
        roomname = body.split(":")[0]
        username = body.split(":")[1]

        room = self.roomStore.getRoomByName(roomname)
        if room.adminStore.isUserExist(self.user):
            user = room.userStore.getUserByName(username)
            if user is None:
                self.queue.put("ERR userNotFound")
            else:
                if user != room.creator:
                    room.userStore.removeUser(user)
                    room.adminStore.removeUser(user)
                    user.queue.put("OCK " + roomname + ":" + user.name)
                    self.queue.put("OCK " + roomname + ":" + user.name)
                else:
                    self.queue.put("ERR permissionDeniedUserIsACreator")
        else:
            self.queue.put("ERR permissionDenied")

    def ulsHandler(self, body):
        room = self.roomStore.getRoomByName(body)
        usernames = ":".join(room.getUserNames())
        self.queue.put("ULS " + usernames)

    def mlsHandler(self):
        roomNames = []
        for room in self.roomStore.roomList:
            if room.userStore.isUserExist(self.user):
                roomNames.append(room.name)
        roomNames = ":".join(roomNames)
        self.queue.put("MLS " + roomNames)

    def madHandler(self,body):
        username = body.split(":")[0]
        roomname = body.split(":")[1]

        room = self.roomStore.getRoomByName(roomname)
        if room.adminStore.isUserExist(self.user):
            user = room.userStore.getUserByName(username)
            if user is None:
                self.queue.put("ERR userNotFound")
            else:
                room.adminStore.addUser(user)
                self.queue.put("MAD "+username+":"+roomname)
                user.queue.put("MAD "+username+":"+roomname)
        else:
            self.queue.put("ERR permissionDenied")

    def parser(self, data):
        instruction = data[:3]
        body = data[4:]
        if instruction == "NIC":
            self.nicHandler(body)
        if instruction == "PCH":
            self.pchHandler(body)
        if instruction == "NRM":
            self.nrmHandler(body)
        if instruction == "RLS":
            self.rlsHandler()
        if instruction == "RIN":
            self.rinHandler(body)
        if instruction == "GNL":
            self.gnlHandler(body)
        if instruction == "PRV":
            self.prvHandler(body)
        if instruction == "BAN":
            self.banHandler(body)
        if instruction == "RUT":
            self.rutHandler(body)
        if instruction == "RMV":
            self.rmvHandler(body)
        if instruction == "KCK":
            self.kckHandler(body)
        if instruction == "ULS":
            self.ulsHandler(body)
        if instruction == "MLS":
            self.mlsHandler()
        if instruction == "MAD":
            self.madHandler(body)


class WriteThread(threading.Thread):
    def __init__(self, conn, queue, loggerQueue, userStore, roomStore, client):
        threading.Thread.__init__(self)
        self.conn = conn
        self.queue = queue
        self.queue.put("**Connected**")
        self.logger = loggerQueue
        self.userStore = userStore
        self.roomStore = roomStore
        self.client = client

    def run(self):
        print("Write Thread Started")
        self.logger.put(self.client + " write thread started")
        while True:
            data = self.queue.get()
            if data[:3] == "QUI":
                self.conn.send("BYE".encode('ascii'))
                self.logger.put(self.client + " closing")
                self.conn.close()
                break
            if data[:3] == "ERR":
                self.logger.put(self.client + " " + data)
            data = data + "\n\r"
            self.conn.send(data.encode('ascii'))
            self.logger.put(self.client + " data sent")


class LoggerThread(threading.Thread):
    def __init__(self, loggerQueue):
        threading.Thread.__init__(self)
        self.logger = loggerQueue

    def run(self):
        print("Logger Thread Started")
        while True:
            data = self.logger.get()
            print("logger")
            data = self.info(data)
            #            print(data)
            f = open("./messages.log", "a")
            f.write(data)
            f.close()

    def info(self, info):
        now = datetime.now()
        return "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] :: " + info + "\n"


serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"

port = 3001

print("socket started")

serversocket.bind((host, port))

serversocket.listen(5)

logQueue = queue.Queue()

loggerThread = LoggerThread(logQueue)
loggerThread.start()

userStore = UserStore()
roomStore = RoomStore()

while True:
    clientsocket, addr = serversocket.accept()
    print("Baglanti %s" % str(addr))

    # her baglanti icin 1 kuyruk ve 2 thread olustur
    # readThread
    # writeThread
    # threadQueue

    cliQueue = queue.Queue()
    readThread = ReadThread(clientsocket, cliQueue, logQueue, userStore, roomStore, str(addr))
    readThread.start()

    writeThread = WriteThread(clientsocket, cliQueue, logQueue, userStore, roomStore, str(addr))
    writeThread.start()
