import json

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

