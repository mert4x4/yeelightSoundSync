import pyaudio
import numpy as np
import time
from yeelight import *
import json
import struct
import socket
import threading

class MagicBulb():
    def __init__(self,bulb_ip,turn_on=True):
        self.turn_on = turn_on
        if self.turn_on:
            self.bulb_ip = bulb_ip
            self.turn_on = turn_on
            self.bulb = Bulb(bulb_ip)
    def setBulb(self):
        if self.turn_on:
            print "setting bulbs music mode on..."
            self.bulb.turn_on()
            self.bulb.set_brightness(100)
            self.bulb.set_rgb(255,255,255)
            self.bulb.start_music()
            print "music mode:",self.bulb.music_mode
        return True
    def sendBulbData(self,r,g,b):
        if self.turn_on:
            self.bulb.set_rgb(r, g, b)
    def exitBulb(self,color):
        if self.turn_on:
            self.bulb.set_brightness(100)
            self.bulb.set_rgb(color[0],color[1],color[2])
            print "exited from bulb"
        return True  

class AudioStream():
    def __init__(self,CHUNK=2048,RATE=44100,DEVICE_INDEX=1):
        self.CHUNK = CHUNK
        self.RATE = RATE
        self.DEVICE_INDEX = DEVICE_INDEX
 
        print "pyaudio stream is starting..."
        self.p=pyaudio.PyAudio()
        print "your device: ",self.p.get_device_info_by_index(DEVICE_INDEX)
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,frames_per_buffer=self.CHUNK, input_device_index=self.DEVICE_INDEX)
        print "stream started"    

    def getdata(self):
        data = self.stream.read(self.CHUNK)
        data_int = np.array(struct.unpack(str(2*self.CHUNK) + 'B',data),dtype='b')+128
        return data_int      
    def exitStream(self):
        print "stream stopped"
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()  
        return True       

class Server():
    def __init__(self,server_ip,server_port):
        self.s = socket.socket()
        self.ServerOn = True
        HOST = server_ip
        PORT = server_port
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        print("TCP Server Created")
    def listen(self):
        c, addr = self.s.accept()
        data = str(c.recv(1024))
        c.close()
        print data
        return data
    
    
class Settings():
    def __init__(self,filename='config.json'):
        self.filename=filename
        self.JsonData = []
        print("reading config.json ...")
        with open(filename) as json_data_file:
            self.JsonData = json.load(json_data_file)
        print "JsonData: ",self.JsonData
    def GetData(self):
        return self.JsonData

def main_musicSync():      
    global LampMode
    while True:
        if LampMode == 0:
            bulb = MagicBulb(bulb_ip = SettingsData.GetData()['bulb_ip'],turn_on=1)
            bulb.setBulb()
            stream = AudioStream(1024,48000,SettingsData.GetData()['device_index']) 
            LampMode = 1       
        if LampMode == 1: 
            r=stream.getdata()[0]
            g=stream.getdata()[512]
            b=stream.getdata()[1023]
            bulb.sendBulbData(r,g,b)
        if LampMode == 2:
            bulb.exitBulb((255,255,255))
            stream.exitStream()
            LampMode = 3

def main_server():
    server = Server(SettingsData.GetData()['server_ip'],SettingsData.GetData()['server_port'])
    global LampMode
    while True:
        data = server.listen()
        if data == 'close':
            if LampMode !=3:
                LampMode = 2
        if data == 'open':
            if LampMode != 1:
                LampMode = 0


if __name__ == '__main__':
    LampMode = 0
    SettingsData = Settings('config.json')
    p1 = threading.Thread(target=main_musicSync).start()
    p2 = threading.Thread(target=main_server).start()

