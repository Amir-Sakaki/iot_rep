import urllib.request
import json
import requests
import threading

            
class ThingSpeak():
    def __init__(self):
        with open("Thingspeak.json", "r") as input_data:
            input_data = json.load(input_data)
            self.address = input_data["catalog_address"]
            self.URL = input_data["URL"]
            self.KEY = input_data["KEY"]

    def Get_Request(self,URL):
        received = requests.get(URL)
        return received.json()        
    
    def Driver_status(self):
        catalog_address = self.address + "/services/REST/thingSpeak_GET"
        service_address = self.Get_Request(catalog_address)
        service_URL = service_address["URL"]
        response = self.Get_Request(service_URL)
        status = response["Status"]
        binary_status = None
        if status == "Normal":
            binary_status = 0
        else:
            binary_status = 1   
        return binary_status
        
    def Driving_Pattern(self):
        threading.Timer(3, self.Driving_Pattern).start() 
        binary_status = self.Driver_status()
        HEADER = '&field1={}'.format(binary_status)
        NEW_URL = self.URL + self.KEY + HEADER
        print(NEW_URL)
        data = urllib.request.urlopen(NEW_URL)
        print(data)

        
if __name__ == '__main__':
    ThingSpeak().Driving_Pattern()
