import cherrypy
import json

class TSGET(object):
    exposed = True
    def __init__(self):
        pass
    
    def GET(self, *uri):
        if uri[0] == "getstatus":
            with open ('status.json','r') as outfile:
                payload = json.load(outfile)
            return json.dumps(payload)
        else:
            return "Bad request"


if __name__ == '__main__':
    conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                  'tools.sessions.on': True}
            }
    cherrypy.tree.mount(TSGET(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8181})
    cherrypy.engine.start()
    cherrypy.engine.block()