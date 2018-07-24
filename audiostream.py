import pyaudio
import numpy as np
import struct

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

    def getData(self):
        data = self.stream.read(self.CHUNK)
        data_int = np.array(struct.unpack(str(2*self.CHUNK) + 'B',data),dtype='b')+128
        return data_int      
    def exitStream(self):
        print "stream stopped"
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()  
        return True      