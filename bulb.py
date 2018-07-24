from yeelight import *

class MagicBulb():
    def __init__(self,bulb_ip,turn_on=True):
        self.turn_on = turn_on
        if self.turn_on:
            self.bulb_ip = bulb_ip
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
    def sendBulbData(self,color):
        if self.turn_on:
            self.bulb.set_rgb(color[0],color[1],color[2])
    def exitBulb(self,color):
        if self.turn_on:
            self.bulb.set_brightness(100)
            self.bulb.set_rgb(color[0],color[1],color[2])
            print "exited from bulb"
        return True  