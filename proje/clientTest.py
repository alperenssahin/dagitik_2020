import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 3001))

messages = [" ",
            "NIC alperen:403<%%$%%>",
            "PCH 403:404<%%$%%>",
            "PCH 403:404<%%$%%>",
            "NRM MYROOOM<%%$%%>",
            "NRM MYROOOM<%%$%%>",
            "NRM MYROOOM2<%%$%%>",
            "NRM MYROOOM3<%%$%%>",
            "RLS<%%$%%>",
            "QUI<%%$%%>"]

data = sock.recv(1024)
print(data.decode("utf-8").strip())
try:
    for message in messages:
        print(message)
        print("========================")
        message += message + "\r\n"
        sock.send(message.encode("ascii"))
        data = sock.recv(1024)
        print(data.decode("utf-8").strip())
        print("*************************\n\n")
finally:
    print("socket closing")
    sock.close()
