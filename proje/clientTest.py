import socket
import time
import threading

state = True


class SocketListener(threading.Thread):
    def __init__(self, socket, name):
        threading.Thread.__init__(self)

        self.socket = socket
        self.name = name

    def run(self):
        print("Listener Started :::: " + self.name)
        while True:
            d = self.socket.recv(1024)
            print("RESPONSE%%%% \t\t" + self.name + " ::: " + d.decode())
            if d.decode()[:3] == "BYE":
                break


def ic(socket, instruction, description=""):
    endoflinetoken = "<%%$%%>"
    return {"socket": socket, "instruction": instruction + endoflinetoken, "description": description}


def messagesHandler(messages):
    for message in messages:
        print("CLIENT>>> \t\t " + message["instruction"])
        print("CLIENT**** \t\t" + message["description"])
        message["socket"].send(message["instruction"].encode("ascii"))
        time.sleep(0.5)


user1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user1.connect(("127.0.0.1", 3001))
listener1 = SocketListener(user1, "user-1")
listener1.start()
user2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user2.connect(("127.0.0.1", 3001))
listener2 = SocketListener(user2, "user-2")
listener2.start()
user3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user3.connect(("127.0.0.1", 3001))
listener3 = SocketListener(user3, "user-3")
listener3.start()

messages = []

messages.append(ic(user1, " ", "Hatali mesaj authentication"))
messages.append(ic(user1, "NIC alperen:404", "Kullanici 1 girisi"))
messages.append(ic(user1, "PCH 404:405", "pin degistirme"))
messages.append(ic(user1, "PCH 403:404", "hatali pin degistirme"))
messages.append(ic(user1, "NRM MYROOOM", "Oda yaratma"))
messages.append(ic(user1, "NRM MYROOOM", "Hatali Oda yaratma"))
messages.append(ic(user1, "NRM MY2ROOM ", "Oda yaratma"))
messages.append(ic(user2, "NIC user2:505", "Yeni kullanici girisi"))
messages.append(ic(user2, "RLS", "Odalari listeler"))
messages.append(ic(user2, "RIN MYROOOM", "User 2 Odaya katilim"))
messages.append(ic(user2, "ULS MYROOOM", "MYROOM ODASINDA BULUNAN KULLANICILAR"))
messages.append(ic(user2, "GNL MYROOOM:Merhaba dunya", "Kullanici 2 Myroom odasina mesaj atar"))
messages.append(ic(user3, "NIC user3:666", "Yeni kullanici girisi"))
messages.append(ic(user3, "PRV user3:hello user2 ben user 3", "OZEL MESAJ"))
messages.append(ic(user3, "RIN MYROOOM", "User 3 Odaya katilim"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))

messages.append(ic(user1, "MAD user3:MYROOOM",
                   "kullani1 kullanici 3 u  Myroomda yonetici yapar"))


messages.append(ic(user3, "KCK MYROOOM:user2",
                   "kullanici 3 kullanici 2 yi myroomdan atar"))



messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))

messages.append(ic(user2, "RIN MYROOOM", "User 2 Odaya katilim"))

messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))


messages.append(ic(user3, "BAN MYROOOM:user2",
                   "kullanici 3 kullanici 2 yi myroomdan banlar"))

messages.append(ic(user2, "RIN MYROOOM", "User 2 Odaya katilim"))


messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))
messages.append(ic(user2, "GNL MYROOOM:ECHOECHOECHOECHOECGHOECHOECGOECHOECHO",
                   "Kullanici 2 Myroom odasina spam mesaj yollamaya baslar"))

messages.append(ic(user1, "RMV MYROOOM",
                   "kullanici 1 myroom odasini siler"))

messagesHandler(messages)
messages = []

# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))
# messages.append(ic(user1, " ", ""))

messages.append(ic(user1, "PCH 405:404", "Testi yeniden calistirildiginda pini dogru girmesi icin"))
messages.append(ic(user1, "QUI", "cikis"))
messages.append(ic(user2, "QUI", "cikis"))
messages.append(ic(user3, "QUI", "cikis"))

messagesHandler(messages)
state = False

user1.close()
user2.close()
user3.close()
