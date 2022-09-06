import json
import cherrypy

class Configuration(object):
    def __init__(self, input_file = "catalog.json"):
        self.services = None
        self.rest=None
        with open(input_file, "r") as jsonfile:
            self.content = json.load(jsonfile)
            self.services = self.content["services"]
            self.valid_ids=[]
            self.valid_STypes =[]
    
            
    def service_reader(self):
        for service in self.services:
            self.valid_STypes.append(service)
            for id_ in self.services[service]:
                self.valid_ids.append(id_["service_id"])
        return self.valid_STypes,self.valid_ids   
     
    def service_validator(self,*services):
        Err_id = "Invalid Service_ID"
        Err_service = "Invalid Service_Type"
        Err_range = "Bad Request"
        self.service_reader()
        services=list(services[0])
        service_len =len(services)
        if service_len in range(1,3):
            if services[0] in self.valid_STypes:
                valid_st = self.services[services[0]]
                if service_len==1:                    
                    return valid_st
                elif service_len == 2:
                    if services[1] in self.valid_ids:                      
                      for i in range(len(valid_st)):
                        if valid_st[i]["service_id"] == services[1]:
                            return valid_st[i]
                    else:
                        return Err_id
            else:
                return Err_service
        else:
            return Err_range

@cherrypy.expose
class Web_Services(object):
    def __init__(self):
        self.config = Configuration()
        pass
    
    def GET(self,*uri):
        err = "Bad request, type '/services' to see the list of valid services"
        if uri:
            if uri[0] =="services":
                if len(uri)==1:
                    return json.dumps(self.config.services)
                elif len(uri)>=2:
                    return json.dumps(self.config.service_validator(uri[1:]))
            else:
                return err     
        return err
    
    def POST(self, *uri, **params):
        return True


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(Web_Services(), '/catalog', conf)
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.server.socket_port = 8585
    cherrypy.engine.start()
    cherrypy.engine.block()
