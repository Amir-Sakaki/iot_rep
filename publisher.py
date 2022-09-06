import paho.mqtt.client as mqtt
import time
import json
import requests

class CatalogConfigReader(object):
    def __init__(self, type=None, fileName="publisher.json"):
        self.details = None
        self.address = None
        with open(fileName, "r") as jsonfile:
            self.details = json.load(jsonfile)
            self.address = self.details["catalog_address"]
            self.client_id = self.details["client_id"]
            
class publisher():
    def __init__(self):
        self.address = CatalogConfigReader().address
        self.broker = ''
        self.port = ''
        self.topic = ''
        self.client_id = CatalogConfigReader().client_id
        self.config()
        self.client = mqtt.Client(self.client_id,False)
        self.client.on_connect = self.myOnConnect
        
    def config(self):
        print('Contacting Service Catalog...')
        while True:
            try:
                #extract initial configuration of the broker
                URL = self.address+"/services/MQTT/mqtt_driverStatus"
                request = requests.get(URL)
                response = json.loads(request.text)
                self.broker = response["broker_address"]
                self.port = response["broker_port"]
                self.topic = response["topic"]
                break
            except Exception as e:
                #Retry to reconnect
                print(e)
                time.sleep(5)
                pass        
         
    def start(self):
        self.client.connect(self.broker,self.port)
        self.client.loop_start()
        
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect(self.broker,self.port)
    
    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print(f'Connected to {self.broker} with code {rc}')
        
    def send_GET(self,URL):
        request = requests.get(URL)
        response = json.loads(request.text)
        return response
    
    def publish_status(self): 
        print('Reading driver status...')
        catalog_address = self.address + "/services/REST/motion"
        service_address = self.send_GET(catalog_address)["URL"]
        response = self.send_GET(service_address)
        self.client.publish(self.topic,json.dumps(response),2)
        print(f'Published:{response}\n')
        
        
if __name__ == "__main__":
    #create Publisher instance 
    TimePublisher = publisher()
    TimePublisher.start()
    
    #run publisher
    while True:
        TimePublisher.publish_status()
        time.sleep(3)
            
    TimePublisher.stop()