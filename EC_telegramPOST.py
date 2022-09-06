import requests
import json

class TG_handler():
    def __init__(self):
        self.counter = 0
        
    def receiver(self,status, address):
        self.driverStatus = status
        self.address = address
        self.name = self.driverStatus['Name']
        self.status = self.driverStatus['Status'] 
        self.phone = self.driverStatus['Phone']
        self.timeStamp = self.driverStatus['TimeStamp']
        self.decider()
        
    def decider(self):        
        if self.status == "Sleepy":
            self.counter += 1
            if self.counter == 3:
                self.sendAlert()
            else:
                pass
        else:
            self.counter = 0
        print(f'Consecutive "Sleepy" status: {self.counter}\n')      
    
    def send_GET(self,URL):
        request = requests.get(URL)
        response = json.loads(request.text)
        return response
    
    def sendAlert(self):
        response = None
        try:
            data = {"Name": self.name, "Status": self.status,"Phone": self.phone, 
                    "timeStamp":self.timeStamp}
            data = json.dumps(data)
            catalog_address = self.address+"/services/REST/telegram_POST"
            service_address = self.send_GET(catalog_address)["URL"]
            r = requests.post(url = service_address , data = data) 
            response = json.loads(r.text)
            print('Triggering alert and resetting the counter...')
            self.counter=0
        except Exception as e:
            print(e)
        if response:
            print("success\n")
        else:
            print("connection failed\n")
             
        