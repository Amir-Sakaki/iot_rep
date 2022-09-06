import paho.mqtt.client as mqtt
import time
import json
import requests
import EC_telegramPOST

class CatalogConfigReader(object):
    def __init__(self, type=None, fileName="EC_subscriber.json"):
        self.details = None
        self.address = None
        with open(fileName, "r") as jsonfile:
            self.details = json.load(jsonfile)
            self.address = self.details["catalog_address"]
            self.clientID = self.details["client_id"]
            
class Subscriber(object):
    def __init__(self):
        self.address = CatalogConfigReader().address
        self.broker = ''
        self.topic = ''
        self.port = ''
        self.clientID = CatalogConfigReader().clientID
        self.config()

        # create an instance of paho.mqtt.client
        self._paho_mqtt = mqtt.Client(self.clientID, False) 

        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
        
        self.tgpost = EC_telegramPOST.TG_handler() 
                
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


    def start (self):
        #manage connection to broker
        self._paho_mqtt.connect(self.broker, self.port)
        self._paho_mqtt.loop_start()
        # subscribe for a topic
        self._paho_mqtt.subscribe(self.topic, 2)

    def stop (self):
        self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
        print ("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
        # A new message is received
        statusJson = json.loads(msg.payload)
        with open ('status.json','w') as outfile:
            json.dump(statusJson,outfile,indent=4)
        print(statusJson)
        self.tgpost.receiver(statusJson,self.address)        
    
if __name__ == "__main__":
    #subscribtion start
    subscribe = Subscriber()
    subscribe.start()

    while True:
        time.sleep(3)

    subscribe.stop()