import cherrypy
import random
import datetime
import json

class Motion(object):
    exposed = True
    def __init__(self):
        pass
    
    def GET(self, *uri, **params):
        result = []
        try:
            if uri[0] == "motion":
                motion = self.motionCreator()
                driver = self.driverID()
                result = {**motion,**driver}
                result = json.dumps(result)
            else:
               result = None
        except Exception as e:
            result = str(e)
            
        if result:
            return result
        else:
            return json.dumps({"result" : "Bad Request"})
    
    #driver behavior simulation
    def motionCreator(self):
        status = random.choices(["Normal","Sleepy"],[.5,.5])[0]
        time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        payload = {"Status": status , "TimeStamp" : time}
        return payload
    
    #driver id
    def driverID(self):
        with open('driverID.json', 'r') as file:
            payload = json.load(file)
            return payload


if __name__ == '__main__':
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                  'tools.sessions.on': True}
            }
    cherrypy.tree.mount(Motion(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
