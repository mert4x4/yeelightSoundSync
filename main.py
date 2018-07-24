
from server import *
from bulb import *
from settings import *
from audiostream import *
import threading

LampMode = 0
SettingsData = Settings('config.json')

def main_musicSync():      
    global LampMode
    while LampMode !=5:
        if LampMode == 0:
            bulb = MagicBulb(bulb_ip = SettingsData.GetData()['bulb_ip'],turn_on=1)
            bulb.setBulb()
            stream = AudioStream(1024,48000,SettingsData.GetData()['device_index']) 
            LampMode = 1       
        if LampMode == 1: 
            rgb=stream.getData()[0],stream.getData()[512],stream.getData()[1023]  
            bulb.sendBulbData(rgb)
        if LampMode == 2:
            bulb.exitBulb((255,255,255))
            stream.exitStream()
            LampMode = 3
        if LampMode == 5:
            bulb.exitBulb((255,255,255))
            stream.exitStream()
            

def main_server():
    server = Server(SettingsData.GetData()['server_ip'],SettingsData.GetData()['server_port'])
    global LampMode
    while LampMode !=5:
        data = server.listen()
        if data == 'close':
            if LampMode !=3:
                LampMode = 2
        if data == 'open':
            if LampMode != 1:
                LampMode = 0
        if data == 'exit':
            LampMode = 5


if __name__ == '__main__':
    p1 = threading.Thread(target=main_musicSync).start()
    p2 = threading.Thread(target=main_server).start()